#!/usr/bin/env python3
"""Manager-fit scoring for a squad or a scouting pool.

Reads data/<team>/interim/*.csv (run the parse step first) and scores every
player against one manager's identity, using the same formulas as the tier
lists in data/<team>/analysis/.

    python .claude/skills/fm26-assistant-manager/scripts/manager_fit.py giovani sporting
    python .claude/skills/fm26-assistant-manager/scripts/manager_fit.py keller inter_scout --vs internacional --top 20
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[4]

PHYSICAL = ["Acceleration", "Agility", "Balance", "Jumping Reach", "Pace", "Stamina", "Strength"]
POSITIONS = ["GK", "DC", "DR", "DL", "WBR", "WBL", "DM", "MC", "MR", "ML", "AMC", "AMR", "AML", "ST"]
FULLBACKS = ("DR", "DL", "WBR", "WBL")
WIDE = ("MR", "ML", "AMR", "AML")
TIERS = [(15, "S"), (13, "A"), (11, "B"), (9, "C"), (7, "D")]


def wmean(p, weights):
    return sum(w * p[a] for a, w in weights.items())


def mean(p, attrs):
    return sum(p[a] for a in attrs) / len(attrs)


def by_pos(pos, table, default=None):
    for keys, val in table:
        if pos in keys:
            return val
    return default


# Each profile returns (primary, secondary, overall_before_penalty, gates, buy_gates).
# A gate is (label, passed, penalty_multiplier). `gates` reproduce the tier lists;
# `buy_gates` are the stricter hard gates from context/managers.md, used when signing.

def giovani(p, pos):
    pos_attr = "Off The Ball" if pos == "ST" else "Positioning"
    mental = (0.30 * p[pos_attr] + 0.25 * p["Decisions"] + 0.20 * p["Team Work"]
              + 0.15 * p["Concentration"] + 0.10 * p["Anticipation"])
    physical = mean(p, PHYSICAL)
    floor = by_pos(pos, [(("DC", "DM"), 14), (FULLBACKS, 13), (("ST",), 13), (("GK",), None)], 12)
    gates = [
        ("Decisões<12", p["Decisions"] >= 12, 0.85),
        ("Teamwork<12", p["Team Work"] >= 12, 0.85),
        ("Concentração<12", p["Concentration"] >= 12, 0.85),
        ("Determinação<10", p["Determination"] >= 10, 0.85),
        ("Flair>13", p["Flair"] <= 13, 0.85),
    ]
    if floor is not None:
        gates.append((f"Pos/OTB<{floor}", p[pos_attr] >= floor, 0.85))
    return mental, physical, 0.70 * mental + 0.30 * physical, gates, gates


def keller(p, pos):
    physical = wmean(p, {"Pace": 0.40, "Work Rate": 0.35, "Stamina": 0.25})
    mental = wmean(p, {"Aggression": 0.35, "Determination": 0.30, "Bravery": 0.20, "Anticipation": 0.15})
    floor = by_pos(pos, [(("GK",), None), (("DC", "DM", "MC"), 11), (FULLBACKS, 13),
                         (("AMC",), 12), (WIDE, 13), (("ST",), 12)])
    gates = [
        ("WorkRate<11", p["Work Rate"] >= 11, 0.85),
        ("Stamina<11", p["Stamina"] >= 11, 0.85),
        ("Determinação<10", p["Determination"] >= 10, 0.85),
        ("Bravura<9", p["Bravery"] >= 9, 0.85),
    ]
    if floor is not None:
        gates.append((f"Pace<{floor}", p["Pace"] >= floor, 0.85))
    buy_floor = by_pos(pos, [(("GK",), None), (("DC",) + FULLBACKS, 14), (WIDE + ("ST",), 15),
                             (("DM", "MC", "AMC"), 12)])
    buy = [
        ("Stamina<13", p["Stamina"] >= 13, 1),
        ("WorkRate<13", p["Work Rate"] >= 13, 1),
        ("Agressão<12", p["Aggression"] >= 12, 1),
        ("Bravura<12", p["Bravery"] >= 12, 1),
    ]
    if buy_floor is not None:
        buy.append((f"Pace<{buy_floor}", p["Pace"] >= buy_floor, 1))
    return physical, mental, 0.70 * physical + 0.30 * mental, gates, buy


def duarte(p, pos):
    mental = wmean(p, {"Vision": 0.30, "Flair": 0.25, "Technique": 0.20, "Dribbling": 0.15, "Acceleration": 0.10})
    physical = mean(p, PHYSICAL)
    floor = by_pos(pos, [(("AMC",), 14), (WIDE + ("MC",), 13), (("DC", "DM") + FULLBACKS, 12)])
    gates = [
        ("Técnica<11", p["Technique"] >= 11, 0.85),
        ("Drible<10", p["Dribbling"] >= 10, 0.85),
        ("Compostura<11", p["Composure"] >= 11, 0.85),
    ]
    if floor is not None:
        gates.append((f"Visão<{floor}", p["Vision"] >= floor, 0.85))
    gates.append(("Posicionamento>15", p["Positioning"] <= 15, 0.90))
    return mental, physical, 0.70 * mental + 0.30 * physical, gates, gates


def casca(p, pos):
    aerial = wmean(p, {"Heading": 0.45, "Jumping Reach": 0.35, "Strength": 0.20})
    discipline = wmean(p, {"Team Work": 0.40, "Concentration": 0.35, "Positioning": 0.25})
    floor = by_pos(pos, [(("DC", "GK"), 13), (("DM", "ST"), 12), (FULLBACKS, 10)], 9)
    gates = [
        ("Teamwork<12", p["Team Work"] >= 12, 0.85),
        ("Concentração<12", p["Concentration"] >= 12, 0.85),
        ("Determinação<10", p["Determination"] >= 10, 0.85),
        ("Flair>13", p["Flair"] <= 13, 0.85),
        (f"Aéreo<{floor}", max(p["Heading"], p["Jumping Reach"]) >= floor, 0.85),
    ]
    return aerial, discipline, 0.70 * aerial + 0.30 * discipline, gates, gates


PROFILES = {
    "giovani": (giovani, "Mental", "Físico"),
    "keller": (keller, "Físico", "Mental"),
    "duarte": (duarte, "Mental", "Físico"),
    "casca": (casca, "Aéreo", "Disciplina"),
}


def to_num(val):
    """Attribute value → float; masked ranges like '7-10' become the midpoint."""
    try:
        return float(val)
    except (TypeError, ValueError):
        try:
            lo, hi = str(val).split("-")
            return (float(lo) + float(hi)) / 2
        except ValueError:
            return float("nan")


def tier_of(overall):
    for cut, tier in TIERS:
        if overall >= cut:
            return tier
    return "E"


def load(team):
    interim = REPO / "data" / team / "interim"
    if not (interim / "attributes.csv").exists():
        sys.exit(f"No interim data for '{team}'. Run: python parse_raw_data.py {team} [date]")
    attr_raw = pd.read_csv(interim / "attributes.csv")
    attr = attr_raw.copy()
    attr_cols = [c for c in attr.columns if c not in ("Name", "UID")]
    attr[attr_cols] = attr[attr_cols].map(to_num)
    # a masked attribute is one that only parsed because of the range fallback
    masked = attr_raw[attr_cols].apply(lambda col: pd.to_numeric(col, errors="coerce")).isna() & attr[attr_cols].notna()
    attr["Masked"] = masked.sum(axis=1)
    df = attr.merge(pd.read_csv(interim / "positions.csv"), on=["Name", "UID"])
    demo = pd.read_csv(interim / "player_demographics.csv")
    keep = [c for c in ("Name", "UID", "Age", "Club", "Salary", "TransferValue") if c in demo.columns]
    df = df.merge(demo[keep], on=["Name", "UID"], how="left")
    perf_path = interim / "performance.csv"
    if perf_path.exists():
        perf = pd.read_csv(perf_path)
        keep = [c for c in ("Name", "UID", "Av_Rat", "Last_5_Games_Rating") if c in perf.columns]
        df = df.merge(perf[keep], on=["Name", "UID"], how="left")
    return df


def score(df, manager, pos=None):
    """Score every player. Each one is judged at `pos` if given (players who can't
    play there are dropped), otherwise at their most favourable natural position."""
    fn, primary_label, secondary_label = PROFILES[manager]
    rows = []
    for _, p in df.iterrows():
        natural = [c for c in POSITIONS if c in p.index and pd.notna(p[c]) and bool(p[c])]
        if pos and pos not in natural:
            continue
        results = []
        for cand in [pos] if pos else (natural or ["MC"]):
            primary, secondary, base, gates, buy_gates = fn(p, cand)
            penalty = 1.0
            for _, passed, mult in gates:
                if not passed:
                    penalty *= mult
            results.append((base * penalty, cand, primary, secondary, gates, buy_gates))
        overall, cand, primary, secondary, gates, buy_gates = max(results, key=lambda r: r[0])
        worst = min(results, key=lambda r: r[0])
        rows.append({
            "Name": p["Name"],
            "Club": p.get("Club"),
            "Age": p.get("Age"),
            "Pos": cand,
            "AllPos": "/".join(natural),
            "Tier": tier_of(overall),
            "Overall": round(overall, 2),
            primary_label: round(primary, 2),
            secondary_label: round(secondary, 2),
            "Fails": ", ".join(label for label, passed, _ in gates if not passed),
            "BuyGateFails": ", ".join(label for label, passed, _ in buy_gates if not passed),
            # weakest natural position, when the gates bite harder there
            "WorstPos": f"{worst[1]} {worst[0]:.2f}" if overall - worst[0] > 0.005 else "",
            "Value": p.get("TransferValue"),
            "Salary": p.get("Salary"),
            "AvRat": p.get("Av_Rat"),
            "Last5": p.get("Last_5_Games_Rating"),
            "Masked": int(p.get("Masked", 0)),
        })
    return pd.DataFrame(rows).sort_values("Overall", ascending=False).reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manager", choices=sorted(PROFILES))
    ap.add_argument("team", help="folder under data/ (a squad or a scouting pool)")
    ap.add_argument("--vs", metavar="SQUAD", help="squad folder to rank each player against, by position")
    ap.add_argument("--pos", help="judge everyone at this position (e.g. DC, AMR); drops players who can't play it")
    ap.add_argument("--max-age", type=int)
    ap.add_argument("--top", type=int, help="show only the first N rows")
    ap.add_argument("--csv", help="also write the full table to this path")
    args = ap.parse_args()

    pos = args.pos.upper() if args.pos else None
    out = score(load(args.team.lower()), args.manager, pos)
    if out.empty:
        sys.exit("No players match.")

    if args.vs:
        squad = score(load(args.vs.lower()), args.manager, pos)
        ranks, displaced = [], []
        for _, r in out.iterrows():
            rivals = squad[(squad["Name"] != r["Name"])
                           & squad["AllPos"].str.split("/").apply(lambda ps: r["Pos"] in ps)]
            ranks.append(f"{(rivals['Overall'] > r['Overall']).sum() + 1}/{len(rivals) + 1}")
            worse = rivals[rivals["Overall"] <= r["Overall"]]
            displaced.append(worse.iloc[0]["Name"] if len(worse) else "")
        out["RankInSquad"] = ranks
        out["WouldDisplace"] = displaced

    if args.max_age:
        out = out[pd.to_numeric(out["Age"], errors="coerce") <= args.max_age]
    if args.csv:
        out.to_csv(args.csv, index=False)
        print(f"Saved {len(out)} rows to {args.csv}")
    if args.top:
        out = out.head(args.top)

    # hide columns that carry no information for this run
    if not out["Masked"].any():
        out = out.drop(columns="Masked")
    if (out["BuyGateFails"] == out["Fails"]).all():
        out = out.drop(columns="BuyGateFails")
    if not out["WorstPos"].any():
        out = out.drop(columns="WorstPos")
    with pd.option_context("display.max_rows", None, "display.width", 250, "display.max_colwidth", 40):
        print(out.to_string(index=False))


if __name__ == "__main__":
    main()
