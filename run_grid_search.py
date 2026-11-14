import itertools
import json
import os
import random
from pathlib import Path

import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

REPO = Path(__file__).resolve().parent
os.chdir(REPO)  # optimize_teams uses relative paths

from fm26.team_optimizer import optimize_teams

TEAM = "chelsea"
BASE_CONFIG = REPO / "configs" / TEAM / "4222.json"
TEMP_CONFIG = REPO / "configs" / TEAM / "_grid_temp.json"
OUTPUT_XLSX = REPO / "data" / TEAM / "grid_search_results.xlsx"

# Parameter grids
age_penalties   = [round(x * 0.1, 1) for x in range(1, 6)]   # 0.1 … 0.5
age_thresholds  = list(range(29, 35))                           # 29 … 34
transfer_values = [round(x * 0.2, 1) for x in range(1, 6)]   # 0.2 … 1.0
av_rats         = [round(x * 0.2, 1) for x in range(0, 6)]   # 0.0 … 1.0

random.seed(42)
sampled = random.sample(
    list(itertools.product(age_penalties, age_thresholds, transfer_values, av_rats)),
    20,
)


def run_config(config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    with TEMP_CONFIG.open("w") as f:
        json.dump(config, f, indent=4)
    teams = optimize_teams(
        team_name=TEAM,
        formation_file=str(TEMP_CONFIG),
        by_formation=False,
        max_teams=2,
    )
    first  = teams[0] if len(teams) > 0 else pd.DataFrame(columns=["Name", "Position", "Role", "Score"])
    second = teams[1] if len(teams) > 1 else pd.DataFrame(columns=["Name", "Position", "Role", "Score"])
    return first, second


def delta(baseline_names: set, combo_names: set) -> tuple[str, str]:
    entered = combo_names - baseline_names
    left    = baseline_names - combo_names
    return (
        ", ".join(sorted(entered)) if entered else "—",
        ", ".join(sorted(left))    if left    else "—",
    )


def apply_excel_style(ws):
    """Bold header, freeze top row, auto-width columns."""
    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(bold=True, color="FFFFFF")

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", wrap_text=True)

    ws.freeze_panes = "A2"

    for col_idx, col_cells in enumerate(ws.columns, 1):
        max_len = max((len(str(c.value or "")) for c in col_cells), default=8)
        ws.column_dimensions[get_column_letter(col_idx)].width = min(max_len + 2, 40)


def main():
    with BASE_CONFIG.open() as f:
        base_config = json.load(f)

    results = []

    # ── Baseline ─────────────────────────────────────────────────────────────
    print("[00] Baseline (default config)...")
    f1, s1 = run_config(base_config)
    results.append({
        "id": "baseline",
        "age_penalty":   base_config["age_penalty"],
        "age_threshold": base_config["age_threshold"],
        "TV":            base_config["multipliers"]["Transfer Value"],
        "AvRat":         base_config["multipliers"]["Av Rat"],
        "first":  f1,
        "second": s1,
    })
    baseline_first_names  = set(f1["Name"])
    baseline_second_names = set(s1["Name"])

    # ── Grid combos ──────────────────────────────────────────────────────────
    for i, (age_pen, age_thr, tv, av_rat) in enumerate(sampled, 1):
        print(f"[{i:02d}] age_pen={age_pen}  thr={age_thr}  TV={tv}  AvRat={av_rat}")
        cfg = json.loads(json.dumps(base_config))
        cfg["age_penalty"]               = age_pen
        cfg["age_threshold"]             = age_thr
        cfg["multipliers"]["Transfer Value"] = tv
        cfg["multipliers"]["Av Rat"]     = av_rat

        f1, s1 = run_config(cfg)
        results.append({
            "id": f"combo_{i:02d}",
            "age_penalty":   age_pen,
            "age_threshold": age_thr,
            "TV":            tv,
            "AvRat":         av_rat,
            "first":  f1,
            "second": s1,
        })

    if TEMP_CONFIG.exists():
        TEMP_CONFIG.unlink()

    # ── Summary sheet ────────────────────────────────────────────────────────
    summary_rows = []
    for r in results:
        f_names = set(r["first"]["Name"])
        s_names = set(r["second"]["Name"])
        f_avg = r["first"]["Score"].astype(float).mean()  if not r["first"].empty  else None
        s_avg = r["second"]["Score"].astype(float).mean() if not r["second"].empty else None
        p_in,  p_out  = delta(baseline_first_names,  f_names)
        sp_in, sp_out = delta(baseline_second_names, s_names)

        summary_rows.append({
            "ID":                r["id"],
            "Age Penalty":       r["age_penalty"],
            "Age Threshold":     r["age_threshold"],
            "Transfer Value":    r["TV"],
            "Av Rating":         r["AvRat"],
            "1st Avg Score":     round(f_avg, 3) if f_avg is not None else "",
            "2nd Avg Score":     round(s_avg, 3) if s_avg is not None else "",
            "1st IN  (vs base)": p_in,
            "1st OUT (vs base)": p_out,
            "2nd IN  (vs base)": sp_in,
            "2nd OUT (vs base)": sp_out,
        })

    summary_df = pd.DataFrame(summary_rows)

    # ── Side-by-side team sheets ─────────────────────────────────────────────
    def build_side_by_side(results, team_key: str) -> pd.DataFrame:
        baseline_df = results[0][team_key]
        data = {
            "Position": baseline_df["Position"].tolist(),
            "Role":     baseline_df["Role"].tolist(),
        }
        for r in results:
            df = r[team_key]
            if df.empty:
                data[r["id"]] = [""] * len(baseline_df)
            else:
                data[r["id"]] = [
                    f"{row['Name']}  ({float(row['Score']):.2f})"
                    for _, row in df.iterrows()
                ]
        return pd.DataFrame(data)

    first_sheet  = build_side_by_side(results, "first")
    second_sheet = build_side_by_side(results, "second")

    # ── Write Excel ──────────────────────────────────────────────────────────
    OUTPUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
        summary_df.to_excel(writer,    sheet_name="Summary",      index=False)
        first_sheet.to_excel(writer,   sheet_name="First Teams",  index=False)
        second_sheet.to_excel(writer,  sheet_name="Second Teams", index=False)

        for sheet_name in ("Summary", "First Teams", "Second Teams"):
            apply_excel_style(writer.sheets[sheet_name])

        # Highlight cells in First/Second Teams that differ from baseline
        for sheet_name, df in (("First Teams", first_sheet), ("Second Teams", second_sheet)):
            ws = writer.sheets[sheet_name]
            baseline_col_idx = 3  # column index of "baseline" (1-based, after Position+Role)
            highlight = PatternFill("solid", fgColor="FFE699")
            for row_idx in range(2, len(df) + 2):
                baseline_val = ws.cell(row=row_idx, column=baseline_col_idx).value or ""
                baseline_player = baseline_val.split("(")[0].strip()
                for col_idx in range(baseline_col_idx + 1, baseline_col_idx + len(results) + 1):
                    cell = ws.cell(row=row_idx, column=col_idx)
                    cell_player = (cell.value or "").split("(")[0].strip()
                    if cell_player and cell_player != baseline_player:
                        cell.fill = highlight

    print(f"\nSalvo em: {OUTPUT_XLSX}")
    print(f"  → {len(results)} combinações  |  3 abas: Summary / First Teams / Second Teams")
    print("  → Células amarelas = jogador diferente do baseline")


if __name__ == "__main__":
    main()
