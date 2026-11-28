#!/usr/bin/env python3
import argparse
import difflib
import json
import os
import random
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd

from .overrides import SCALAR_KEYS, build_overrides, describe_overrides, effective_config, has_overrides
from .source import read_source
from .explain import Explainer, knobs_line, parse_top
from .team_optimizer import optimize_teams, teams_output_dir


def players_with_inf(team_name, codes):
    """[(name, 'inf:<code>')] for players whose Inf status is one of `codes` (case-insensitive), from player_demographics.csv."""
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
    return [(str(n), f"inf:{i}") for n, i in zip(hit['Name'], inf[hit.index])]


def _fold(name):
    """Casefolded, accent-free form of a name (single place to swap in smarter name matching)."""
    text = unicodedata.normalize('NFKD', str(name))
    return ''.join(c for c in text if not unicodedata.combining(c)).casefold().strip()


def names_match(a, b):
    return _fold(a) == _fold(b)


def _norm_words(name):
    """Accent-free, casefolded, whitespace-collapsed form of a name."""
    return ' '.join(_fold(name).split())


def resolve_names(team_name, queries, flag):
    """Map user-typed names to canonical squad names; exits listing every unknown/ambiguous name."""
    path = Path("data") / team_name / "interim" / "player_demographics.csv"
    if not path.exists():
        print(f"Error: {path} not found; cannot resolve {flag} names. Run the parse step first.")
        exit(1)
    squad = list(dict.fromkeys(pd.read_csv(path)['Name'].astype(str)))
    normed = {n: _norm_words(n) for n in squad}
    resolved, changed, errors = [], [], []
    for q in queries:
        nq = _norm_words(q)
        hits = [n for n in squad if normed[n] == nq]
        if not hits and nq:
            hits = [n for n in squad if f" {nq} " in f" {normed[n]} "]
        if len(hits) == 1:
            if hits[0] not in resolved:
                resolved.append(hits[0])
            if hits[0].casefold() != q.strip().casefold():
                changed.append(f"'{q}' -> {hits[0]}")
        elif hits:
            errors.append(f"{flag}: '{q}' is ambiguous, pass the full name: {', '.join(hits)}")
        else:
            close = difflib.get_close_matches(nq, list(normed.values()), n=3, cutoff=0.5)
            sugg = [n for c in close for n in squad if normed[n] == c]
            hint = f" Closest: {', '.join(sugg)}" if sugg else ""
            errors.append(f"{flag}: no player matches '{q}'.{hint}")
    if errors:
        print('\n'.join(f"Error: {e}" for e in errors))
        exit(1)
    if changed:
        print(f"{flag}: {', '.join(changed)}")
    return resolved


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
    """[(name, reason)] to exclude: players at `levels`, minus protected/already-excluded, optionally a random
    fraction. Reason is 'load:<level> <min>/<max>', prefixed with 'sample ' when a fraction was drawn."""
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
    prefix = 'sample ' if fraction is not None else ''
    return [(r['Name'], f"{prefix}load:{r['MatchLoad']} {r['MatchLoadMinutes']}/{r['MatchLoadMinutesMax']}")
            for r in pool]


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
    return [(r['Name'], 'top-load') for r in top]


def write_manifest(team_name, formation_file, args, overrides, config, exclusions, seed, teams_saved, teams_detail=None):
    """data/<team>/teams/[<formation>/]run.json: what this run used, next to the CSVs it produced."""
    source = read_source(team_name)
    cwd = Path.cwd()
    try:
        config_file = str(Path(formation_file).resolve().relative_to(cwd))
    except ValueError:
        config_file = str(formation_file)
    manifest = {
        'run_at': datetime.now().astimezone().isoformat(timespec='seconds'),
        'team': team_name,
        'export': source.get('label', 'unknown') if source else 'unknown',
        'config_file': config_file,
        'overrides': overrides,
        'effective_config': {k: v for k, v in config.items() if k != 'formation'},
        'exclusions': exclusions,
        'keep': args.keep or [],
        'keep_gk': bool(args.keep_gk),
        'seed': seed if args.sample is not None else None,
        'teams_saved': teams_saved,
        # slot score of each player in teams 1-2, split into its parts (same numbers as --explain)
        'teams_detail': teams_detail or [],
        'argv': sys.argv,
    }
    if os.environ.get('FM27_RUN_CMD'):
        manifest['run_team_cmd'] = os.environ['FM27_RUN_CMD']
    out = teams_output_dir(team_name, formation_file, args.by_formation) / 'run.json'
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    p = argparse.ArgumentParser()

    p.add_argument('team')
    p.add_argument('formation')
    p.add_argument('--age-penalty', type=float)
    p.add_argument('--age-threshold', type=int)
    p.add_argument('--set', nargs='+', metavar='KEY=VALUE', dest='set_items',
                   help=f"Override config scalars for this run ({', '.join(SCALAR_KEYS)})")
    p.add_argument('--mult', nargs='+', metavar='NAME=WEIGHT',
                   help="Set/override multipliers for this run (weight 0 removes; e.g. 'Last 5 Games=0.1')")
    p.add_argument('--no-mult', action='store_true', help='Clear all config multipliers before applying --mult')
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
    p.add_argument('--explain', nargs='+', metavar='NAME',
                   help='After picking the teams, break down the slot score of these players (2 names = head-to-head)')
    p.add_argument('--top', nargs='+', metavar='POS',
                   help='After picking the teams, rank the candidates for these positions (e.g. AMC ST 5; N defaults to 5)')
    p.add_argument('--brief', action='store_true', help='Only the lines that matter (no "Salvei" line)')

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

    if args.exclude:
        args.exclude = resolve_names(team_name, args.exclude, '--exclude')
    if args.keep:
        args.keep = resolve_names(team_name, args.keep, '--keep')
    if args.explain:
        args.explain = resolve_names(team_name, args.explain, '--explain')
    exclusions = []  # [{'name', 'reason'}] in the order applied; first reason wins for a repeated name
    excluded = []  # casefolded names, what the optimizer receives

    def exclude(pairs):
        for name, reason in pairs:
            if name.casefold() not in excluded:
                excluded.append(name.casefold())
                exclusions.append({'name': name, 'reason': reason})

    exclude((n, '-r') for n in (args.exclude or []))
    if args.inf:
        exclude(players_with_inf(team_name, args.inf))

    if args.sample is not None and not 0 <= args.sample <= 1:
        p.error('--sample must be between 0 and 1')
    if args.sample is not None and not args.load:
        p.error('--sample needs --load')

    demo = load_table(team_name) if (args.load or args.top_load) else None
    seed = None
    if args.load:
        seed = args.seed if args.seed is not None else random.SystemRandom().randrange(2**31)
        if args.sample is not None:
            print(f"--sample seed: {seed}")
        exclude(players_by_load(
            demo, args.load, excluded, args.keep, args.keep_gk, args.sample, random.Random(seed)))

    try:
        overrides = build_overrides(args.set_items, args.mult, args.no_mult, args.age_penalty, args.age_threshold)
    except ValueError as e:
        p.error(str(e))
    with open(formation_file, "r") as f:
        base_config = json.load(f)
    config = effective_config(base_config, overrides)  # in memory only; the file is never rewritten
    if has_overrides(overrides):
        line = describe_overrides(base_config, config)
        if line:
            print(line)
    print(knobs_line(Path(formation_file).name, config))

    def run(excl):
        return optimize_teams(
            team_name,
            formation_file,
            config=config,
            strict_mult_keys=set(overrides['mult']),
            excluded_players=excl,
            by_formation=args.by_formation,
            quiet=args.brief,
        )

    teams = run(excluded)
    if args.top_load and teams:
        exclude(players_by_top_load(
            demo, teams[0]['Name'].tolist(), args.top_load, excluded, args.keep, args.keep_gk))
        teams = run(excluded)
    if not teams:
        return
    explainer = Explainer(team_name, config, teams, exclusions, set(overrides['mult']))
    write_manifest(team_name, formation_file, args, overrides, config, exclusions, seed, len(teams),
                   explainer.team_detail(teams))
    # --explain/--top: run_team.py prints explain.txt after the teams table; run directly, print it here
    out = []
    if args.explain:
        out.append(explainer.explain(args.explain))
    if args.top:
        positions, n = parse_top(args.top)
        out.append(explainer.top(positions, n))
    if out:
        path = teams_output_dir(team_name, formation_file, args.by_formation) / 'explain.txt'
        path.write_text('\n\n'.join(out) + '\n', encoding='utf-8')
        if not os.environ.get('FM27_RUN_CMD'):
            print('\n\n'.join(out))
    else:
        (teams_output_dir(team_name, formation_file, args.by_formation) / 'explain.txt').unlink(missing_ok=True)


if __name__ == "__main__":
    main()