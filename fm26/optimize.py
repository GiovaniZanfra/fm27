#!/usr/bin/env python3
import argparse
from pathlib import Path

from .team_optimizer import optimize_teams


def main():
    p = argparse.ArgumentParser()

    p.add_argument('team')
    p.add_argument('formation')
    p.add_argument('--age-penalty', type=float)
    p.add_argument('--age-threshold', type=int)
    p.add_argument('--exclude', nargs='+')
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