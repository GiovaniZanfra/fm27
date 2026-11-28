"""The slot score is built in one place (TeamOptimizer.components): the lineup, --explain, --top and
run.json all read it, so these tests pin that the parts add up and that every reader sees the same total."""
import os

import pandas as pd
import pytest

from fm27.explain import Explainer
from fm27.team_optimizer import PositionRequirement, TeamOptimizer, optimize_teams

PLAYERS = ["Keeper", "Old Pro", "Kid", "Tired Star", "Bench Guy"]
FORMATION = [
    {"position": "GK", "role": "Goalkeeper", "role_oop": "Goalkeeper_OOP"},
    {"position": "DC", "role": "Centre_Back", "role_oop": "Covering_Centre_Back_OOP"},
    {"position": "ST", "role": "Centre_Forward"},
]
CONFIG = {
    "ip_weight": 0.7, "age_penalty": 0.2, "age_threshold": 29, "fatigue_penalty": 0.3,
    "multipliers": {"Positioning": 0.15, "Av Rat": 0.3, "Flair": -0.08},
    "formation": FORMATION,
}


def frames():
    scores = pd.DataFrame({
        "Name": PLAYERS,
        "Goalkeeper_Score": [15.0, 5.0, 4.0, 6.0, 5.5],
        "Goalkeeper_OOP_Score": [14.0, 5.0, 4.0, 6.0, 5.5],
        "Centre_Back_Score": [5.0, 13.0, 11.5, 12.0, 10.0],
        "Covering_Centre_Back_OOP_Score": [5.0, 12.0, 12.5, 11.0, 10.5],
        "Centre_Forward_Score": [3.0, 10.0, 12.0, 14.0, 11.0],
        "Age": [27, 34, 18, 26, 30],
        "MatchLoadMinutes": [360, 90, 14, 270, None],
        "IsGK": [True, False, False, False, False],
        "Positioning_Normalized": [0.5, 1.2, -0.4, 0.1, -1.0],
        "Av_Rat_Normalized": [0.4, -0.2, 0.0, 2.1, -0.5],
        "Flair_Normalized": [-1.0, 0.3, 1.5, 0.9, 0.0],
    })
    positions = pd.DataFrame({
        "Name": PLAYERS,
        "GK": [True, False, False, False, False],
        "DC": [False, True, True, True, True],
        "ST": [False, True, True, True, True],
    })
    return scores, positions


def optimizer():
    scores, positions = frames()
    mults = {"Positioning_Normalized": 0.15, "Av_Rat_Normalized": 0.3, "Flair_Normalized": -0.08}
    return TeamOptimizer(scores, positions, [], age_penalty=0.2, age_threshold=29, multipliers=mults,
                         ip_weight=0.7, fatigue_penalty=0.3)


def test_parts_add_up_to_total():
    opt = optimizer()
    for name in PLAYERS:
        for slot in FORMATION:
            req = PositionRequirement(slot["position"], slot["role"], slot.get("role_oop"))
            c = opt.components(name, req)
            if c is None:
                continue
            parts = c["blend"] + c["age"] + c["arabic"] + c["fatigue"] + sum(c["mult"].values())
            assert parts == pytest.approx(c["total"], abs=1e-12)


def test_known_values():
    c = optimizer().components("Old Pro", PositionRequirement("DC", "Centre_Back", "Covering_Centre_Back_OOP"))
    assert c["blend"] == pytest.approx(0.7 * 13.0 + 0.3 * 12.0)
    assert c["age"] == pytest.approx(-0.2 * 5)
    assert c["fatigue"] == pytest.approx(-0.3 * 90 / 90)
    assert c["mult"]["Av_Rat_Normalized"] == pytest.approx(0.3 * -0.2)


def test_goalkeeper_exempt_from_fatigue_and_ineligible_is_none():
    opt = optimizer()
    assert opt.components("Keeper", PositionRequirement("GK", "Goalkeeper", "Goalkeeper_OOP"))["fatigue"] == 0.0
    assert opt.components("Keeper", PositionRequirement("ST", "Centre_Forward")) is None
    no_load = opt.components("Bench Guy", PositionRequirement("ST", "Centre_Forward"))
    assert no_load["fatigue"] == 0.0  # no Match Load data: no penalty


def test_lineup_score_is_components_total():
    opt = optimizer()
    reqs = [PositionRequirement(s["position"], s["role"], s.get("role_oop")) for s in FORMATION]
    team = opt.optimize_team(reqs)
    for row in team.itertuples(index=False):
        req = PositionRequirement(row.Position, row.Role, row.Role_OOP or None)
        assert row.Score == optimizer().components(row.Name, req)["total"]  # exact, same code path


def test_explain_and_run_json_match_the_saved_teams(tmp_path, monkeypatch):
    """End to end through the files: teams on disk, run.json detail and --top read the same totals."""
    scores, positions = frames()
    team = "t"
    (tmp_path / "data" / team / "scores").mkdir(parents=True)
    (tmp_path / "data" / team / "interim").mkdir(parents=True)
    scores.drop(columns=["Age", "MatchLoadMinutes", "IsGK", "Positioning_Normalized", "Av_Rat_Normalized",
                         "Flair_Normalized"]).to_csv(tmp_path / "data" / team / "scores" / f"{team}_scores.csv", index=False)
    positions.to_csv(tmp_path / "data" / team / "interim" / "positions.csv", index=False)
    scores[["Name", "Age", "MatchLoadMinutes", "IsGK"]].to_csv(
        tmp_path / "data" / team / "interim" / "player_demographics.csv", index=False)
    scores[["Name", "Positioning_Normalized", "Av_Rat_Normalized", "Flair_Normalized"]].to_csv(
        tmp_path / "data" / team / "interim" / "performance.csv", index=False)
    monkeypatch.chdir(tmp_path)

    teams = optimize_teams(team, "x.json", config=CONFIG, by_formation=True, quiet=True)
    assert teams
    explainer = Explainer(team, CONFIG, teams, [])
    for team_df, detail in zip(teams, explainer.team_detail(teams)):
        for row, d in zip(team_df.itertuples(index=False), detail):
            assert d["name"] == row.Name
            assert d["components"]["total"] == pytest.approx(row.Score, abs=1e-3)
    top = explainer.top(["ST"], 5)
    assert teams[0].loc[teams[0]["Position"] == "ST", "Name"].iloc[0] in top
