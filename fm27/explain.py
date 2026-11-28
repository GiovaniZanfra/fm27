"""--explain / --top / the knob line: why the optimizer picked whom, from TeamOptimizer.components.

Every number printed here comes from TeamOptimizer.components, the same function the optimizer
ranks on, so an explanation can never drift from the lineup it explains."""
from pathlib import Path

import pandas as pd

from .display import pos_rank, role_sigla, slot_siglas
from .team_optimizer import METRIC_COLUMN_MAP, PositionRequirement, TeamOptimizer, load_scoring

FORM_COLS = {'Av_Rat_Normalized', 'Last_5_Games_Rating_Normalized'}
REPO = Path(__file__).resolve().parents[1]


def mult_label(col):
    """'Positioning_Normalized' -> 'Positioning', 'Av_Rat_Normalized' -> 'Av Rat'."""
    for name, mapped in METRIC_COLUMN_MAP.items():
        if mapped == col and col not in ('Av_Rat_Normalized',):
            return name
    return col[:-len('_Normalized')].replace('_', ' ') if col.endswith('_Normalized') else col


def _g(v):
    return f"{v:g}"


def knobs_line(config_name, config):
    """One line with the hyperparameters this run actually used."""
    age_p = float(config.get('age_penalty') or 0)
    age = f"idade {_g(age_p)}" + (f" acima de {config.get('age_threshold', 30)}" if age_p else "")
    fat = float(config.get('fatigue_penalty') or 0)
    parts = [f"config {config_name}", f"ip_weight {_g(float(config.get('ip_weight', 0.5)))}", age,
             f"fadiga {_g(fat)}" + ("/90min" if fat else "")]
    if config.get('arabic_penalty'):
        parts.append(f"arabic {_g(float(config['arabic_penalty']))}")
    mults = config.get('multipliers') or {}
    parts.append("mult " + (', '.join(f"{k} {_g(float(w))}" for k, w in mults.items()) if mults else "nenhum"))
    return "pesos: " + " | ".join(parts)


class Explainer:
    """Scores every player in every slot of the formation, with no exclusions."""

    def __init__(self, team_name, config, teams, exclusions, strict_mult_keys=()):
        scores_df, positions_df, self.settings, self.requirements = load_scoring(team_name, config, strict_mult_keys, warn=False)
        self.opt = TeamOptimizer(scores_df, positions_df, [], **self.settings)
        self.names = scores_df['Name'].astype(str).tolist()
        self.excluded = {e['name']: e['reason'] for e in exclusions}
        self.where = {}  # name -> 'T1 AMC'
        self.holders = {}  # (team index, slot index) -> (name, score)
        for t, team_df in enumerate(teams, start=1):
            for k, row in enumerate(team_df.itertuples(index=False)):
                self.where.setdefault(row.Name, f"T{t} {row.Position}")
                self.holders[(t, k)] = (row.Name, row.Score)

    # slots ---------------------------------------------------------------
    def slots(self, positions=None):
        """[(slot index, requirement)] in display order, identical slots listed once."""
        seen, out = set(), []
        for k, req in enumerate(self.requirements):
            key = (req.position, req.role, req.role_oop)
            if key in seen or (positions and req.position not in positions):
                continue
            seen.add(key)
            out.append((k, req))
        return sorted(out, key=lambda kr: (pos_rank(kr[1].position), kr[0]))

    def slot_title(self, k, req):
        held = []
        for t in (1, 2):
            if (t, k) in self.holders:
                name, score = self.holders[(t, k)]
                held.append(f"T{t} {name} {score:.2f}")
        return f"{req.position} {slot_siglas(REPO, req.role, req.role_oop)}" + (f"  ({' · '.join(held)})" if held else "")

    def status(self, name):
        if name in self.excluded:
            return f"excluído ({self.excluded[name]})"
        return self.where.get(name, "fora dos times")

    # rows ----------------------------------------------------------------
    def role_rows(self, req):
        """[(label, getter)] for the slot-dependent part: role scores and their blend."""
        rows = [(f"com bola {role_sigla(REPO, req.role, 'ip')}", lambda c: f"{c['ip']:.2f}")]
        if req.role_oop:
            w = self.settings['ip_weight']
            rows.append((f"sem bola {role_sigla(REPO, req.role_oop, 'oop')}", lambda c: f"{c['oop']:.2f}"))
            rows.append((f"mistura {_g(w)}/{_g(round(1 - w, 4))}", lambda c: f"{c['blend']:.2f}"))
        rows.append(("+ ajustes", lambda c: f"{c['total'] - c['blend']:+.2f}"))
        rows.append(("Total", lambda c: f"{c['total']:.2f}"))
        return rows

    def adjustment_rows(self):
        """[(label, getter)] for the parts that are the same in every slot (age, fatigue, multipliers)."""
        s = self.settings
        rows = []
        if s['age_penalty']:
            rows.append((f"idade {_g(s['age_penalty'])}/ano >{s['age_threshold']}", lambda c: f"{c['age']:+.2f}"))
        if s['fatigue_penalty']:
            rows.append((f"fadiga {_g(s['fatigue_penalty'])}/90min", lambda c: f"{c['fatigue']:+.2f}"))
        if s['arabic_penalty']:
            rows.append(("arabic", lambda c: f"{c['arabic']:+.2f}"))
        for col, weight in s['multipliers'].items():
            if weight:
                rows.append((f"{mult_label(col)} {_g(weight)}",
                             lambda c, col=col, weight=weight:
                             f"{c['mult'].get(col, 0.0):+.2f} (z {c['mult'].get(col, 0.0) / weight:+.1f})"))
        rows.append(("soma", lambda c: f"{c['total'] - c['blend']:+.2f}"))
        return rows

    # output ----------------------------------------------------------------
    def _block(self, names, comps, rows):
        table = [["", *names]]
        for label, get in rows:
            table.append([label, *("—" if c is None else get(c) for c in comps)])
        if len(names) == 2 and all(comps):
            table[0].append("diferença")
            for r in table[1:]:
                a, b = (_lead_number(x) for x in r[1:3])
                r.append("" if a is None or b is None else f"{a - b:+.2f}")
        return _render(table)

    def explain(self, names):
        lines = ["explain: " + " · ".join(f"{n} → {self.status(n)}" for n in names)]
        slots = [(k, req, [self.opt.components(n, req) for n in names]) for k, req in self.slots()]
        slots = [(k, req, comps) for k, req, comps in slots if any(c is not None for c in comps)]
        if not slots:
            lines.append("nenhum deles joga em alguma posição desta formação")
            return "\n".join(lines)
        # adjustments do not depend on the slot: take each player's first slot he can play
        first = [next((comps[i] for _, _, comps in slots if comps[i] is not None), None) for i in range(len(names))]
        adj = self.adjustment_rows()
        if len(adj) > 1:
            lines += ["", "ajustes (iguais em qualquer posição)"]
            lines += self._block(names, first, adj)
        for k, req, comps in slots:
            lines += ["", self.slot_title(k, req)]
            lines += self._block(names, comps, self.role_rows(req))
        return "\n".join(lines)

    def top(self, positions, n):
        lines = []
        for k, req in self.slots(positions):
            cand = []
            for name in self.names:
                if name in self.excluded:
                    continue
                c = self.opt.components(name, req)
                if c is not None:
                    cand.append((name, c))
            cand.sort(key=lambda nc: -nc[1]['total'])
            if not cand:
                continue
            best = cand[0][1]['total']
            s = self.settings
            head = ["#", "Nome", "Total", "Δ1º", "mistura"]
            if s['age_penalty']:
                head.append("idade")
            if s['fatigue_penalty']:
                head.append("fadiga")
            head += ["atributos", "forma", "onde"]
            table = [head]
            for i, (name, c) in enumerate(cand[:n], start=1):
                attrs = sum(v for col, v in c['mult'].items() if col not in FORM_COLS)
                form = sum(v for col, v in c['mult'].items() if col in FORM_COLS)
                row = [str(i), name, f"{c['total']:.2f}", f"{c['total'] - best:+.2f}", f"{c['blend']:.2f}"]
                if s['age_penalty']:
                    row.append(f"{c['age']:+.2f}")
                if s['fatigue_penalty']:
                    row.append(f"{c['fatigue']:+.2f}")
                row += [f"{attrs:+.2f}", f"{form:+.2f}", self.where.get(name, "-")]
                table.append(row)
            if lines:
                lines.append("")
            lines.append(f"top {n} {self.slot_title(k, req)}")
            lines.extend(_render(table, left=(1, len(head) - 1)))
        if not lines:
            return f"--top: nenhuma posição {' '.join(positions)} nesta formação"
        if self.excluded:
            lines.append(f"(sem os {len(self.excluded)} excluídos deste run)")
        return "\n".join(lines)

    def team_detail(self, teams, upto=2):
        """[[{pos, name, role, role_oop, components}]] for teams 1..upto (for run.json)."""
        out = []
        for team_df in teams[:upto]:
            rows = []
            for r in team_df.itertuples(index=False):
                req = PositionRequirement(r.Position, r.Role, r.Role_OOP if isinstance(r.Role_OOP, str) and r.Role_OOP else None)
                c = self.opt.components(r.Name, req)
                if c is not None:
                    c = {**{k: (round(v, 3) if isinstance(v, float) else v) for k, v in c.items() if k != 'mult'},
                         'mult': {mult_label(col): round(v, 3) for col, v in c['mult'].items()}}
                rows.append({'pos': r.Position, 'name': r.Name, 'role': r.Role, 'role_oop': r.Role_OOP or None,
                             'components': c})
            out.append(rows)
        return out


def _lead_number(text):
    try:
        return float(str(text).split()[0])
    except (ValueError, IndexError):
        return None


def _render(table, left=(0,)):
    """Plain aligned table; columns in `left` are left-aligned, the rest right-aligned."""
    widths = [max(len(str(r[i])) for r in table) for i in range(len(table[0]))]
    out = []
    for j, r in enumerate(table):
        cells = [str(v).ljust(widths[i]) if i in left else str(v).rjust(widths[i]) for i, v in enumerate(r)]
        out.append("  ".join(cells).rstrip())
        if j == 0:
            out.append("  ".join("-" * w for w in widths))
    return out


def parse_top(tokens):
    """['AMC', 'ST', '3'] -> (['AMC', 'ST'], 3); default N is 5."""
    positions, n = [], 5
    for t in tokens:
        if t.isdigit():
            n = int(t)
        else:
            positions.append(t.upper())
    return positions, n
