#!/usr/bin/env python3
"""Pull new FM exports from the Windows exports folder into data/<team>/raw/.

The FM plugin always writes to a fixed folder as "Squad YYYY-MM-DD HH-MM-SS.html",
so exports sort by file name. Each lands as
data/<team>/raw/YYYY-MM-DD_HH-MM-SS.html; the team comes from the export's "Club"
column (most common value), so the view must include it.

Every export not yet in data/ is ingested, each into its own club's folder, so
exporting several teams in a row is safe. It refuses instead of guessing: no Club
column, mixed clubs (a scouting list), or a club without a data/ folder are skipped
with a message. The script only copies: run_team.py parses.

Usage:
    python ingest_export.py                                   # all pending exports
    python ingest_export.py --list                            # newest exports and where they went
    python ingest_export.py --scout palmeiras --file 'Squad 2026-11-19 12-00-00.html'
    python ingest_export.py --team bahia --file '...html'     # view without Club column
"""
import argparse
import html
import os
import re
import shutil
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from fm27.source import latest_raw

EXPORTS_DIR = Path(os.environ.get(
    "FM_EXPORTS_DIR",
    "/mnt/c/Users/giova/Documents/Sports Interactive/Football Manager 27/exports",
))
REPO = Path(__file__).resolve().parent
DATA = REPO / "data"

CELL = re.compile(r"<t([hd])[^>]*>(.*?)</t[hd]>", re.S | re.I)
ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")


def slug(name: str) -> str:
    """'São Paulo' -> 'sao_paulo'."""
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    return "_".join(s.lower().replace("-", " ").split())


def club_matches(club: str, folder: str) -> bool:
    """'SC Corinthians Paulista' matches folder 'corinthians'; 'AS Roma' matches 'roma'."""
    return set(folder.split("_")) <= set(slug(club).split("_"))


def latest_exports(n: int = 1) -> list[Path]:
    return sorted(EXPORTS_DIR.glob("*.html"), key=lambda p: p.name)[-n:]


SQUAD_SHARE = 0.85  # a squad export must be at least this share one club


def clubs_in_export(path: Path) -> Counter | None:
    """Counts of the 'Club' column, or None if the view has no such column (regex parse: pandas.read_html is ~5s here)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = [[html.unescape(TAG.sub("", c)).strip() for _, c in CELL.findall(r)] for r in ROW.findall(text)]
    header = next((r for r in rows if "Club" in r), None)
    if header is None:
        return None
    i = header.index("Club")
    return Counter(r[i] for r in rows if r is not header and len(r) > i and r[i])


def label_of(src: Path) -> str:
    return src.stem.replace("Squad ", "").replace(" ", "_")


def already_ingested(label: str) -> Path | None:
    done = sorted(DATA.glob(f"*/raw/{label}.html"))
    return done[0] if done else None


def resolve_team(src: Path, team: str | None, scout: str | None) -> str:
    """Team folder for one export. Raises ValueError instead of guessing."""
    clubs = clubs_in_export(src)
    if scout:
        return f"{slug(scout)}_scout"
    if clubs is None:
        if team:
            return slug(team)
        raise ValueError("no 'Club' column in the view; add it, or pass --team/--scout with --file")
    if not clubs:
        raise ValueError("'Club' column is empty")
    club, n = clubs.most_common(1)[0]
    share = n / sum(clubs.values())
    if team:
        if not club_matches(club, slug(team)):
            raise ValueError(f"--team {team} but the export is {club} ({share:.0%}); refusing")
        return slug(team)
    if share < SQUAD_SHARE:
        raise ValueError(f"mixed clubs {dict(clubs.most_common(4))}: looks like a scouting list; "
                         f"use --scout <team> --file '{src.name}'")
    folders = [d.name for d in DATA.iterdir() if d.is_dir() and club_matches(club, d.name)]
    if len(folders) != 1:
        why = "no" if not folders else f"several ({folders})"
        raise ValueError(f"club {club} matches {why} data/ folder; pass --team <folder> --file '{src.name}'")
    return folders[0]


def ingest(src: Path, team: str) -> Path:
    raw_dir = DATA / team / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    dst = raw_dir / f"{label_of(src)}.html"
    shutil.copy2(src, dst)  # keeps the export time as mtime, so "newest" = newest export
    return dst


def ingest_sources(sources, team=None, scout=None):
    """Ingest each export; returns ([(src, dst)], [(src, reason)]). Never guesses: unresolvable exports are skipped."""
    copied, skipped = [], []
    for src in sources:
        try:
            dest_team = resolve_team(src, team, scout)
        except ValueError as e:
            skipped.append((src, str(e)))
            continue
        copied.append((src, ingest(src, dest_team)))
    return copied, skipped


def ingest_pending():
    """Ingest every export not yet in data/. Raises FileNotFoundError if the exports folder is missing."""
    if not EXPORTS_DIR.is_dir():
        raise FileNotFoundError(f"Exports folder not found: {EXPORTS_DIR} (set FM_EXPORTS_DIR)")
    return ingest_sources([p for p in sorted(EXPORTS_DIR.glob("*.html"), key=lambda p: p.name)
                           if not already_ingested(label_of(p))])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--team", help="team folder for --file (checked against the Club column)")
    ap.add_argument("--scout", metavar="TEAM", help="scouting list for TEAM -> data/TEAM_scout/ (needs --file)")
    ap.add_argument("--file", help="ingest only this export file name")
    ap.add_argument("--list", action="store_true", help="list the 5 newest exports and exit")
    args = ap.parse_args()

    if not EXPORTS_DIR.is_dir():
        sys.exit(f"Exports folder not found: {EXPORTS_DIR} (set FM_EXPORTS_DIR)")

    if args.list:
        for p in reversed(latest_exports(5)):
            done = already_ingested(label_of(p))
            print(f"{p.name}  ->  {done.relative_to(REPO) if done else 'not ingested'}")
        return

    if (args.team or args.scout) and not args.file:
        sys.exit("--team/--scout apply to one export: add --file '<name>.html' (see --list)")

    if args.file:
        sources = [EXPORTS_DIR / args.file]
        if not sources[0].exists():
            sys.exit(f"Not found: {sources[0]}")
    else:
        sources = [p for p in sorted(EXPORTS_DIR.glob("*.html"), key=lambda p: p.name)
                   if not already_ingested(label_of(p))]

    copied, skipped = ingest_sources(sources, args.team, args.scout)
    for src, dst in copied:
        print(f"{src.name} -> {dst.relative_to(REPO)}")
    for src, why in skipped:
        print(f"SKIPPED {src.name}: {why}")
    failed = len(skipped)

    # Latest raw file per team, so the caller knows what --date to use.
    print("latest per team:")
    for raw in sorted(DATA.glob("*/raw")):
        newest = latest_raw(raw)
        if newest:
            print(f"  {raw.parent.name}: {newest.stem}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
