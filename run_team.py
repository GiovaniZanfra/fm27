#!/usr/bin/env python3
"""Convenience runner for the full pipeline."""

import argparse
import csv
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

    def attach_best(rows):
        out = []
        for r in rows:
            r2 = dict(r)
            best = best_map.get(r2.get('Name') or '')
            for kind, label in (('ip', 'Best Role'), ('oop', 'Best OOP')):
                role, score = best[kind] if best else (None, None)
                r2[label] = role or ''
                r2[f'{label} Score'] = f"{score:.4g}" if score is not None else ''
            out.append(r2)
        return out

    frows = attach_best(frows)
    srows = attach_best(srows)

    _pretty_print_table(frows, title='First Team')
    _pretty_print_table(srows, title='Second Team')


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