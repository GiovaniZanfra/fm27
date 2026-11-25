#!/usr/bin/env python3
import argparse
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

    optimize_teams(
        team_name,
        formation_file,
        age_penalty=args.age_penalty,
        age_threshold=args.age_threshold,
        excluded_players=excluded,
        by_formation=args.by_formation,
    )


if __name__ == "__main__":
    main()