#!/usr/bin/env python3
"""Convenience runner for the full pipeline."""

import argparse
import csv
import re
import shlex
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"Command failed: {cmd} (exit {res.returncode})")
        return False
    return True


def _pretty_print_table(rows, title=None):
    if not rows:
        print(f"{title or ''}: (no rows)")
        return

    cols = list(rows[0].keys()) if isinstance(rows[0], dict) else []
    if not cols:
        print(title or '')
        return

    widths = {c: len(c) for c in cols}
    for r in rows:
        for c in cols:
            v = str(r.get(c, ''))
            widths[c] = max(widths[c], min(len(v), 60))

    if title:
        print(f"\n{title}")

    hdr = ' | '.join(c.ljust(widths[c]) for c in cols)
    sep = '-+-'.join('-' * widths[c] for c in cols)
    print(hdr)
    print(sep)

    for r in rows:
        line = ' | '.join((str(r.get(c, ''))[:60]).ljust(widths[c]) for c in cols)
        print(line)


# Display order: GK, then each line right to left.
POSITION_ORDER = ['GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL', 'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'ST']


def _pos_rank(pos):
    return POSITION_ORDER.index(pos) if pos in POSITION_ORDER else len(POSITION_ORDER)


def _norm_role(name):
    name = re.sub(r'[_\s]+OOP$', '', str(name).strip())
    return re.sub(r'[^a-z0-9]', '', name.lower())


def _role_abbreviations(repo: Path):
    """{'ip'|'oop': {normalized role name: sigla}} from the glossary (section 6) of managers_tactics.md."""
    out = {'ip': {}, 'oop': {}}
    path = repo / 'context' / 'managers_tactics.md'
    if not path.exists():
        return out
    kind = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('### 6.1'):
            kind = 'ip'
        elif line.startswith('### 6.2'):
            kind = 'oop'
        elif line.startswith('## ') or (line.startswith('### ') and kind and not line.startswith('### 6.')):
            kind = None
        elif kind:
            m = re.match(r'\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|', line)
            if m:
                out[kind][_norm_role(m.group(2))] = m.group(1)
    return out


def _abbr(abbr, role, kind):
    """Sigla for a role name ('Ball_Playing_Centre_Back' -> 'BPCB'); initials if not in the glossary."""
    if not role:
        return ''
    key = _norm_role(role)
    if key in abbr.get(kind, {}):
        return abbr[kind][key]
    words = re.sub(r'[_\s]+OOP$', '', str(role)).replace('_', ' ').replace('-', ' ').split()
    return ''.join(w[0].upper() for w in words)


def print_teams(repo: Path, team: str, formation: str = None):
    base = repo / 'data' / team / 'teams'
    if formation:
        base = base / formation
    first = base / 'first_team.csv'
    second = base / 'second_team.csv'

    def read_csv(path):
        if not path.exists():
            return []
        with path.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [r for r in reader]

    frows = read_csv(first)
    srows = read_csv(second)

    # compute best role & score per player from scores CSV
    scores_path = repo / 'data' / team / 'scores' / f"{team}_scores.csv"
    # best in-possession and best out-of-possession role per player
    best_map = {}
    if scores_path.exists():
        try:
            with scores_path.open(newline='', encoding='utf-8') as sf:
                for r in csv.DictReader(sf):
                    name = r.get('Name') or ''
                    best = {'ip': (None, None), 'oop': (None, None)}
                    for k, v in r.items():
                        if not k or not k.endswith('_Score'):
                            continue
                        try:
                            val = float(v) if v not in (None, '') else None
                        except Exception:
                            val = None
                        if val is None:
                            continue
                        role_name = k[:-6].replace('_', ' ').strip()
                        kind = 'oop' if role_name.endswith(' OOP') else 'ip'
                        if best[kind][1] is None or val > best[kind][1]:
                            best[kind] = (role_name, val)
                    if name:
                        best_map[name] = best
        except Exception:
            pass

    abbr = _role_abbreviations(repo)

    def display(rows):
        out = []
        for r in sorted(rows, key=lambda r: _pos_rank(r.get('Position'))):
            ip, oop = r.get('Role') or '', r.get('Role_OOP') or ''
            role = _abbr(abbr, ip, 'ip') + (f"/{_abbr(abbr, oop, 'oop')}" if oop else '')
            best = best_map.get(r.get('Name') or '')
            best_role = ''
            if best and best['ip'][0]:
                best_role = _abbr(abbr, best['ip'][0], 'ip')
                if best['oop'][0]:
                    best_role += f"/{_abbr(abbr, best['oop'][0], 'oop')}"
            try:
                score = f"{float(r.get('Score')):.2f}"
            except (TypeError, ValueError):
                score = r.get('Score') or ''
            out.append({'Pos': r.get('Position') or '', 'Name': r.get('Name') or '',
                        'Role': role, 'Score': score, 'Best': best_role})
        return out

    _pretty_print_table(display(frows), title='First Team')
    _pretty_print_table(display(srows), title='Second Team')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('team')
    p.add_argument('--no-parse', action='store_true')
    p.add_argument('--no-calc', action='store_true')
    p.add_argument('--config', help='Path to optimizer config file (formation JSON)')
    p.add_argument('-r', '--raw', nargs='+', help='Names to exclude')
    p.add_argument('--date', help='Date string for raw HTML file (e.g. jan2025, oct2024)')
    p.add_argument('--by-formation', action='store_true', help='Save teams in a subfolder named after the formation')
    args = p.parse_args()

    team = args.team
    repo = Path(__file__).resolve().parent

    print(f"team is {team}. repo is {repo}")

    # Steps
    steps = []

    if not args.no_parse:
        date_arg = f" {shlex.quote(args.date)}" if args.date else ""
        steps.append(f"python parse_raw_data.py {team}{date_arg}")

    if not args.no_calc:
        steps.append(f"python calculate_scores.py {team}")

    formation = args.config if args.config else f"configs/{team}/1.json"
    formation_str = f"{repo}/configs/{team}/{formation}"
    formation_q = shlex.quote(formation_str)

    raw_args = ''
    if args.raw:
        raw_args = '--exclude ' + ' '.join(shlex.quote(n) for n in args.raw)
    by_formation_arg = '--by-formation' if args.by_formation else ''
    print(formation_q)
    steps.append(f"python optimize_teams.py {team} {formation_q} {raw_args} {by_formation_arg}".rstrip())

    # Run pipeline
    for cmd in steps:
        ok = run_cmd(cmd)
        if not ok:
            print("Pipeline stopped due to error.")
            sys.exit(1)

    print("Pipeline completed successfully.")

    formation_stem = Path(formation).stem if args.by_formation else None
    try:
        print_teams(repo, team, formation=formation_stem)
    except Exception as e:
        print(f"Could not print teams: {e}")


if __name__ == '__main__':
    main()