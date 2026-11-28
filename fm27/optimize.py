#!/usr/bin/env python3
import argparse
import random
import re
import unicodedata
from pathlib import Path

import pandas as pd

from .team_optimizer import optimize_teams


def players_with_inf(team_name, codes):
    """Names whose Inf status is one of `codes` (case-insensitive), from player_demographics.csv."""
    path = Path("data") / team_name / "interim" / "player_demographics.csv"
    demo = pd.read_csv(path) if path.exists() else pd.DataFrame()
    if 'Inf' not in demo.columns:
        print(f"Error: no Inf column in {path}. Rerun the parse step (without --no-parse) "
              "on an export that has the Inf column.")
        exit(1)
    wanted = {c.strip().casefold() for c in codes}
    inf = demo['Inf'].fillna('').astype(str).str.strip()
    hit = demo[inf.str.casefold().isin(wanted)]
    if hit.empty:
        print(f"--inf {' '.join(codes)}: nobody excluded")
    else:
        listed = ', '.join(f"{n} ({i})" for n, i in zip(hit['Name'], inf[hit.index]))
        print(f"--inf {' '.join(codes)}: excluded {len(hit)}: {listed}")
    return hit['Name'].astype(str).tolist()


def _fold(name):
    """Casefolded, accent-free form of a name (single place to swap in smarter name matching)."""
    text = unicodedata.normalize('NFKD', str(name))
    return ''.join(c for c in text if not unicodedata.combining(c)).casefold().strip()


def names_match(a, b):
    return _fold(a) == _fold(b)


def _norm_level(level):
    return re.sub(r'[\s_-]+', ' ', str(level)).strip().casefold()


def load_table(team_name):
    """player_demographics.csv rows with match-load columns; errors out if the parse predates them."""
    path = Path("data") / team_name / "interim" / "player_demographics.csv"
    demo = pd.read_csv(path) if path.exists() else pd.DataFrame()
    if 'MatchLoad' not in demo.columns:
        print(f"Error: no MatchLoad column in {path}. Rerun the parse step (without --no-parse) "
              "on an export that has the Match Load column.")
        exit(1)
    demo = demo.copy()
    demo['IsGK'] = demo['IsGK'].astype(str).str.casefold().eq('true') if 'IsGK' in demo.columns else False
    demo['Name'] = demo['Name'].astype(str)
    return demo


def _fmt_load(row):
    level = row['MatchLoad'] if pd.notna(row['MatchLoad']) else '?'
    return f"{row['Name']} ({level} {row['MatchLoadMinutes']}/{row['MatchLoadMinutesMax']} min)"


def protected(row, keep, keep_gk):
    return (keep_gk and bool(row['IsGK'])) or any(names_match(row['Name'], k) for k in (keep or []))


def players_by_load(demo, levels, already, keep, keep_gk, fraction, rng):
    """Names to exclude: players at `levels`, minus protected/already-excluded, optionally a random fraction."""
    wanted = {_norm_level(l) for l in levels}
    done = {_fold(n) for n in already}
    pool = [r for _, r in demo.iterrows()
            if _norm_level(r['MatchLoad']) in wanted and _fold(r['Name']) not in done
            and not protected(r, keep, keep_gk)]
    label = f"--load {' '.join(levels)}"
    if fraction is not None:
        pool = rng.sample(pool, round(fraction * len(pool)))
        label += f" (sample {fraction:g})"
    print(f"{label}: excluded {len(pool)}" + (": " + ', '.join(_fmt_load(r) for r in pool) if pool else ""))
    return [r['Name'] for r in pool]


def players_by_top_load(demo, first_team_names, n, already, keep, keep_gk):
    """The `n` first-team players with the most minutes in the load window (tie: games), skipping protected ones."""
    done = {_fold(x) for x in already}
    in_team = {_fold(x) for x in first_team_names}
    cand = [r for _, r in demo.iterrows()
            if _fold(r['Name']) in in_team and _fold(r['Name']) not in done and not protected(r, keep, keep_gk)]
    cand.sort(key=lambda r: (-(r['MatchLoadMinutes'] if pd.notna(r['MatchLoadMinutes']) else -1),
                             -(r['MatchLoadGames'] if pd.notna(r['MatchLoadGames']) else -1)))
    top = cand[:n]
    print(f"--top-load {n} (first team): excluded {len(top)}" + (": " + ', '.join(_fmt_load(r) for r in top) if top else ""))
    return [r['Name'] for r in top]


def main():
    p = argparse.ArgumentParser()

    p.add_argument('team')
    p.add_argument('formation')
    p.add_argument('--age-penalty', type=float)
    p.add_argument('--age-threshold', type=int)
    p.add_argument('--exclude', nargs='+')
    p.add_argument('--inf', nargs='+', metavar='CODE',
                   help='Exclude players whose Inf column has any of these codes (e.g. Inj Unr Sus); case-insensitive')
    p.add_argument('--by-formation', action='store_true')
    p.add_argument('--load', nargs='+', metavar='LEVEL',
                   help='Load pool: players whose MatchLoad is one of these (light medium heavy very-heavy)')
    p.add_argument('--keep', nargs='+', metavar='NAME', help='Never excluded by load filters')
    p.add_argument('--keep-gk', action='store_true', help='Goalkeepers are never excluded by load filters')
    p.add_argument('--sample', type=float, metavar='FRACTION',
                   help='Randomly exclude this fraction (0-1) of the load pool instead of all of it')
    p.add_argument('--seed', type=int, help='Seed for --sample (random and printed if omitted)')
    p.add_argument('--top-load', type=int, metavar='N',
                   help='Re-run excluding the N highest-minutes players of the first team')
    p.add_argument('--of', choices=['first'], default='first', help='Team --top-load ranks (only first)')

    args = p.parse_args()

    team_name = args.team.lower()
    formation_file = args.formation

    formation_path = Path(formation_file)

    if not formation_path.exists():
        repo_root = Path(__file__).resolve().parents[1].parents[0]
        alt = repo_root / formation_file

        if alt.exists():
            formation_path = alt
            formation_file = str(formation_path)
        else:
            print(f"Error: Formation file '{formation_file}' not found (cwd={Path.cwd()})")
            print(f"Tried: {formation_file} and {alt}")
            exit(1)

    excluded = [n.casefold() for n in (args.exclude or [])]
    if args.inf:
        excluded += [n.casefold() for n in players_with_inf(team_name, args.inf)]

    if args.sample is not None and not 0 <= args.sample <= 1:
        p.error('--sample must be between 0 and 1')
    if args.sample is not None and not args.load:
        p.error('--sample needs --load')

    demo = load_table(team_name) if (args.load or args.top_load) else None
    if args.load:
        seed = args.seed if args.seed is not None else random.SystemRandom().randrange(2**31)
        if args.sample is not None:
            print(f"--sample seed: {seed}")
        excluded += [n.casefold() for n in players_by_load(
            demo, args.load, excluded, args.keep, args.keep_gk, args.sample, random.Random(seed))]

    def run(excl):
        return optimize_teams(
            team_name,
            formation_file,
            age_penalty=args.age_penalty,
            age_threshold=args.age_threshold,
            excluded_players=excl,
            by_formation=args.by_formation,
        )

    teams = run(excluded)
    if args.top_load and teams:
        excluded += [n.casefold() for n in players_by_top_load(
            demo, teams[0]['Name'].tolist(), args.top_load, excluded, args.keep, args.keep_gk)]
        run(excluded)


if __name__ == "__main__":
    main()