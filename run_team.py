#!/usr/bin/env python3
"""Convenience runner for the full pipeline."""

import argparse
import csv
import os
import shlex
import subprocess
import sys
from pathlib import Path

from fm27.display import abbr as _abbr, pos_rank as _pos_rank, role_abbreviations as _role_abbreviations
from fm27.overrides import build_overrides
from fm27.source import export_label


# With --brief, only these lines of the parse/score steps are shown (everything is shown if a step fails).
BRIEF_KEEP = ('export:', 'error', 'traceback')


def run_cmd(cmd, brief=False, echo=True):
    if not brief:
        if echo:
            print(f"Running: {cmd}")
        res = subprocess.run(cmd, shell=True)
    else:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = (res.stdout + res.stderr).splitlines()
        for line in lines if res.returncode else [l for l in lines if l.strip().casefold().startswith(BRIEF_KEEP)]:
            print(line)
    if res.returncode != 0:
        print(f"Command failed: {cmd} (exit {res.returncode})")
        return False
    return True


def ingest_new_exports(team):
    """Copy new FM exports into data/ (one summary line). Never fatal: warns and carries on with what is in data/."""
    try:
        import ingest_export
        copied, skipped = ingest_export.ingest_pending()
    except (Exception, SystemExit) as e:
        print(f"ingest: WARNING {e}; continuing with what is in data/")
        return
    mine = [dst for _, dst in copied if dst.parent.parent.name == team]
    others = len(copied) - len(mine)
    msg = f"{len(mine)} new for {team}" + (f" (latest {mine[-1].stem})" if mine else "")
    if others:
        msg += f", {others} for other teams"
    if skipped:
        msg += f", {len(skipped)} skipped (python ingest_export.py shows why)"
    print(f"ingest: {msg}")


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


def print_teams(repo: Path, team: str, formation: str = None, brief: bool = False):
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

    if not brief:
        _pretty_print_table(display(frows), title='First Team')
        _pretty_print_table(display(srows), title='Second Team')
        return
    # one table: slot, then team 1 and team 2 side by side (rows are in config order in both files)
    pairs = sorted(zip(frows, srows + [{}] * (len(frows) - len(srows))), key=lambda fs: _pos_rank(fs[0].get('Position')))
    rows = []
    for f, s2 in pairs:
        a = display([f])[0]
        b = display([s2])[0] if s2 else {'Name': '', 'Score': '', 'Best': ''}
        rows.append({'Pos': a['Pos'], 'Role': a['Role'],
                     'Time 1': a['Name'], 'Sc1': a['Score'], 'Best1': a['Best'] if a['Best'] != a['Role'] else '',
                     'Time 2': b['Name'], 'Sc2': b['Score'], 'Best2': b['Best'] if b['Best'] != a['Role'] else ''})
    _pretty_print_table(rows)


HELP_EXAMPLES = """\
examples:
  # match: unavailable players out, half of the heavy-load ones drawn out (not goalkeepers or Gio)
  python run_team.py corinthians --config relogio.json --by-formation --inf Inj Unr Ine Int Sus \\
      --load heavy very-heavy --keep-gk --keep Gio --sample 0.5

  # same lineup, now without two more players (no re-parse; same export)
  python run_team.py corinthians --config relogio.json --by-formation --no-parse --no-calc \\
      --inf Inj Unr Ine Int Sus -r garro 'yuri alberto'

  # rest the 4 first-team players with most minutes in the last 14 days
  python run_team.py corinthians --config relogio.json --by-formation --inf Inj Unr Ine Int Sus \\
      --top-load 4 --keep-gk

  # one-off tweaks for this match only (the config file is not changed)
  python run_team.py corinthians --config relogio.json --by-formation \\
      --set ip_weight=0.75 age_penalty=0.2 --mult 'Last 5 Games=0.1'

  # attributes only, no form or age adjustments
  python run_team.py corinthians --config relogio.json --by-formation --no-mult --set age_penalty=0

  # short output for a match: export, exclusions, weights used, teams 1 and 2 side by side
  python run_team.py corinthians --config relogio.json --by-formation --brief --inf Inj Unr Ine Int Sus

  # why Lingard and not Dieguinho, and who else fights for the AMC (same flags as the lineup asked about)
  python run_team.py corinthians --config relogio.json --by-formation --no-parse --no-calc \\
      --inf Inj Unr Ine Int Sus --explain lingard dieguinho --top AMC

  # tilt close calls towards rested players: 0.3 points off per 90 min played in the last 14 days
  python run_team.py corinthians --config relogio.json --by-formation --set fatigue_penalty=0.3

Each run prints the export it used and a `pesos:` line with the hyperparameters it applied, and writes
data/<team>/teams/<config>/run.json (export, effective config, every exclusion with its reason, seed,
command, and each slot score of teams 1-2 split into its parts).
"""


def main():
    sys.stdout.reconfigure(line_buffering=True)  # keep our lines ordered with the subprocesses' when piped
    p = argparse.ArgumentParser(
        description='Ingest new FM exports, parse the newest one, score every role and pick teams 1..N '
                    'for a formation config. Prints the first and second team in position order.',
        epilog=HELP_EXAMPLES, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('team', help='team folder in data/ and configs/ (e.g. corinthians, palmeiras, roma, bahia)')

    g = p.add_argument_group('data')
    g.add_argument('--date', metavar='LABEL',
                   help='parse data/<team>/raw/<LABEL>.html (e.g. 2026-11-27_21-19-10) instead of the newest export')
    g.add_argument('--no-ingest', action='store_true', help='do not pull new exports from the FM exports folder first')
    g.add_argument('--no-parse', action='store_true',
                   help='reuse the last parsed export (no ingest either); use when only flags or config changed')
    g.add_argument('--no-calc', action='store_true', help='reuse the last role scores (pair with --no-parse)')

    g = p.add_argument_group('config')
    g.add_argument('--config', help='formation config, a file name in configs/<team>/ (e.g. relogio.json); required')
    g.add_argument('--by-formation', action='store_true',
                   help='save teams in data/<team>/teams/<config name>/ (always pass it)')
    g.add_argument('--set', nargs='+', metavar='KEY=VALUE', dest='set_items',
                   help='override a config value for this run only: ip_weight, age_penalty, age_threshold, arabic_penalty, '
                        'fatigue_penalty (points off per 90 min in the last 14 days; goalkeepers exempt)')
    g.add_argument('--mult', nargs='+', metavar='NAME=WEIGHT',
                   help="set a multiplier for this run only, e.g. 'Last 5 Games=0.1' 'Flair=0' (0 removes it)")
    g.add_argument('--no-mult', action='store_true',
                   help='drop all config multipliers (attributes only), then apply any --mult')

    g = p.add_argument_group('exclusions')
    g.add_argument('-r', '--raw', nargs='+', metavar='NAME',
                   help="players to leave out; accents/case ignored, full name or one whole word ('kaio cesar', paulista)")
    g.add_argument('--inf', nargs='+', metavar='CODE',
                   help='leave out players with these Inf statuses; for a match: Inj Unr Ine Int Sus '
                        '(Loa Wnt Wtg Rst FtT Fgn are informational)')
    g.add_argument('--load', nargs='+', metavar='LEVEL',
                   help='leave out players at these match load levels: light medium heavy very-heavy')
    g.add_argument('--sample', type=float, metavar='FRACTION',
                   help='with --load, leave out only a random fraction (0-1) of them; the seed is printed')
    g.add_argument('--seed', type=int, help='repeat an earlier --sample draw')
    g.add_argument('--top-load', type=int, metavar='N',
                   help='rerun without the N first-team players with most minutes in the last 14 days')
    g.add_argument('--of', choices=['first'], default='first', help=argparse.SUPPRESS)
    g.add_argument('--keep', nargs='+', metavar='NAME', help='never left out by --load/--sample/--top-load')
    g.add_argument('--keep-gk', action='store_true', help='goalkeepers are never left out by --load/--sample/--top-load')

    g = p.add_argument_group('output')
    g.add_argument('--brief', action='store_true',
                   help='short output: export, weights, exclusions and one table with teams 1 and 2 side by side')
    g.add_argument('--explain', nargs='+', metavar='NAME',
                   help="break down these players' slot scores (role IP/OOP, blend, age, fatigue, each multiplier); "
                        "2 names = head-to-head. Repeat the previous run's flags (and --seed) so the lineup is the same")
    g.add_argument('--top', nargs='+', metavar='POS',
                   help='rank the candidates for these positions, e.g. --top AMC ST 3 (N defaults to 5)')
    args = p.parse_args()
    try:
        build_overrides(args.set_items, args.mult, args.no_mult)  # fail before parse/calc on a bad flag
    except ValueError as e:
        p.error(str(e))

    team = args.team
    repo = Path(__file__).resolve().parent

    if not args.brief:
        print(f"team is {team}. repo is {repo}")

    os.environ['FM27_RUN_CMD'] = shlex.join(sys.argv)  # recorded in run.json by the optimizer
    os.environ.setdefault('PYTHONWARNINGS', 'ignore::FutureWarning')  # pandas deprecation noise in the steps

    if not args.no_parse and not args.no_ingest:
        ingest_new_exports(team)

    # Steps
    steps = []

    if args.no_parse:
        print(f"export: {export_label(team)}")
    else:
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
    if args.inf:
        raw_args += ' --inf ' + ' '.join(shlex.quote(c) for c in args.inf)
    if args.load:
        raw_args += ' --load ' + ' '.join(shlex.quote(l) for l in args.load)
    if args.keep:
        raw_args += ' --keep ' + ' '.join(shlex.quote(n) for n in args.keep)
    if args.keep_gk:
        raw_args += ' --keep-gk'
    if args.sample is not None:
        raw_args += f' --sample {args.sample}'
    if args.seed is not None:
        raw_args += f' --seed {args.seed}'
    if args.top_load:
        raw_args += f' --top-load {args.top_load} --of {args.of}'
    if args.set_items:
        raw_args += ' --set ' + ' '.join(shlex.quote(i) for i in args.set_items)
    if args.mult:
        raw_args += ' --mult ' + ' '.join(shlex.quote(i) for i in args.mult)
    if args.no_mult:
        raw_args += ' --no-mult'
    if args.explain:
        raw_args += ' --explain ' + ' '.join(shlex.quote(n) for n in args.explain)
    if args.top:
        raw_args += ' --top ' + ' '.join(shlex.quote(t) for t in args.top)
    if args.brief:
        raw_args += ' --brief'
    by_formation_arg = '--by-formation' if args.by_formation else ''
    steps.append(f"python optimize_teams.py {team} {formation_q} {raw_args} {by_formation_arg}".rstrip())

    # Run pipeline
    for i, cmd in enumerate(steps):
        # the optimizer's own lines (exclusions, weights) always show; parse/score are filtered with --brief
        ok = run_cmd(cmd, brief=args.brief and i < len(steps) - 1, echo=not args.brief)
        if not ok:
            print("Pipeline stopped due to error.")
            sys.exit(1)

    if not args.brief:
        print("Pipeline completed successfully.")

    formation_stem = Path(formation).stem if args.by_formation else None
    try:
        print_teams(repo, team, formation=formation_stem, brief=args.brief)
    except Exception as e:
        print(f"Could not print teams: {e}")
    if args.explain or args.top:
        explain = repo / 'data' / team / 'teams' / (formation_stem or '') / 'explain.txt'
        if explain.exists():
            print()
            print(explain.read_text(encoding='utf-8').rstrip())


if __name__ == '__main__':
    main()