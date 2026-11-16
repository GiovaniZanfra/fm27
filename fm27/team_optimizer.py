import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

# Maps human-friendly config keys to pre-normalized column names in performance.csv.
# For raw attribute names (e.g. "Stamina") the resolver tries "{key}_Normalized" directly.
METRIC_COLUMN_MAP: Dict[str, str] = {
    "Transfer Value": "TransferValue_Normalized",
    "Last 5 Games":   "Last_5_Games_Rating_Normalized",
    "Trn Rating":     "Training_Rate_Normalized",
    "Av Rating":      "Av_Rat_Normalized",
}


@dataclass
class PositionRequirement:
    """A slot in the formation: position, in-possession role and optional out-of-possession role."""
    position: str               # e.g. 'DL', 'DC', 'MC'
    role: str                   # in possession, e.g. 'Ball_Playing_Centre_Back'
    role_oop: str | None = None  # out of possession, e.g. 'Covering_Centre_Back_OOP'

    def get_score_column(self) -> str:
        """Score column of the in-possession role."""
        return f"{self.role.replace(' ', '_')}_Score"

    def get_oop_score_column(self) -> str | None:
        """Score column of the out-of-possession role, if the slot has one."""
        if not self.role_oop:
            return None
        return f"{self.role_oop.replace(' ', '_')}_Score"


class TeamOptimizer:
    """Optimizes team selection based on player scores and required positions."""

    def __init__(self, scores_df: pd.DataFrame, positions_df: pd.DataFrame, exclude_players: List[str] = None,
                 age_penalty: float = 0.0, age_threshold: int = 30,
                 multipliers: Dict[str, float] = None, arabic_penalty: float = 0.0,
                 ip_weight: float = 0.5):
        self.scores_df = scores_df
        self.positions_df = positions_df
        self.selected_players = set()
        self.age_penalty = float(age_penalty or 0.0)
        self.age_threshold = int(age_threshold or 0)
        self.multipliers = multipliers or {}
        self.arabic_penalty = float(arabic_penalty or 0.0)
        # Weight of the in-possession role when a slot also has an OOP role.
        self.ip_weight = float(ip_weight)
        if not 0.0 <= self.ip_weight <= 1.0:
            raise ValueError(f"ip_weight must be between 0 and 1, got {self.ip_weight}")
        if exclude_players:
            self.selected_players.update(exclude_players)
        
    def optimize_team(self, requirements: List[PositionRequirement]) -> pd.DataFrame:
        """
        Globally optimize team selection to maximize total score using Hungarian algorithm.
        Args:
            requirements: List of position requirements
        Returns:
            DataFrame with selected players and their scores
        """
        # Filter out excluded players
        available_scores_df = self.scores_df[
            ~self.scores_df['Name'].str.lower().isin([p.lower() for p in self.selected_players])
        ].copy()
        available_positions_df = self.positions_df[self.positions_df['Name'].isin(available_scores_df['Name'])].copy()
        available_players = available_scores_df['Name'].tolist()
        n_positions = len(requirements)
        n_players = len(available_players)

        # Build cost matrix (negative scores for maximization, ineligible assignments get large positive)
        cost_matrix = np.full((n_positions, n_players), 1e9)  # Default to ineligible
        adjusted_scores = np.full((n_positions, n_players), np.nan)
        for i, req in enumerate(requirements):
            score_col = req.get_score_column()
            oop_col = req.get_oop_score_column()
            pos_col = req.position  # e.g., 'DL', 'DR', etc.
            for col in (score_col, oop_col):
                if col and col not in available_scores_df.columns:
                    raise ValueError(f"Score column '{col}' not found in scores file (check the role name).")
            if pos_col not in available_positions_df.columns:
                raise ValueError(f"Position column '{pos_col}' not found in positions file.")
            for j in range(n_players):
                player_name = available_players[j]
                score = available_scores_df.loc[available_scores_df['Name'] == player_name, score_col].values[0]
                if oop_col:
                    oop_score = available_scores_df.loc[available_scores_df['Name'] == player_name, oop_col].values[0]
                    score = self.ip_weight * score + (1 - self.ip_weight) * oop_score
                pos_val = available_positions_df.loc[available_positions_df['Name'] == player_name, pos_col].values[0]
                if pos_val == True:
                    if self.age_penalty and 'Age' in available_scores_df.columns:
                        age_val = available_scores_df.loc[available_scores_df['Name'] == player_name, 'Age'].values[0]
                        try:
                            age_val = float(age_val) if not pd.isna(age_val) else None
                        except Exception:
                            age_val = None
                        if age_val is not None:
                            score = score - self.age_penalty * max(0, age_val - self.age_threshold)
                    if self.arabic_penalty and 'Club' in available_scores_df.columns:
                        club_val = available_scores_df.loc[available_scores_df['Name'] == player_name, 'Club'].values[0]
                        if isinstance(club_val, str) and club_val.lower().startswith('al-'):
                            score = score - self.arabic_penalty
                    for col, weight in self.multipliers.items():
                        if not weight or col not in available_scores_df.columns:
                            continue
                        raw = available_scores_df.loc[available_scores_df['Name'] == player_name, col].values[0]
                        try:
                            val = float(raw) if not pd.isna(raw) else 0.0
                        except Exception:
                            val = 0.0
                        score = score + weight * val
                    cost_matrix[i, j] = -score
                    adjusted_scores[i, j] = score
        # Solve assignment problem
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        selected = []
        for pos_idx, player_idx in zip(row_ind, col_ind):
            req = requirements[pos_idx]
            player = available_scores_df.iloc[player_idx]
            cost = cost_matrix[pos_idx, player_idx]
            adjusted_score = adjusted_scores[pos_idx, player_idx]
            # Only assign if cost is not the ineligible sentinel
            if cost >= 1e8:
                print(f"WARNING: No eligible player for position {req.position} ({req.role})!")
                selected.append({
                    'Name': 'No eligible player',
                    'Position': req.position,
                    'Role': req.role,
                    'Role_OOP': req.role_oop or '',
                    'Score': None
                })
                continue
            selected.append({
                'Name': player['Name'],
                'Position': req.position,
                'Role': req.role,
                'Role_OOP': req.role_oop or '',
                'Score': float(adjusted_score) if not pd.isna(adjusted_score) else None
            })
            self.selected_players.add(player['Name'])

        return pd.DataFrame(selected)


def parse_formation(formation_data: List[Dict[str, str]]) -> List[PositionRequirement]:
    """
    Parse formation data into position requirements.
    
    Args:
        formation_data: List of dicts with position, role and optional role_oop
            (e.g., [{"position": "DL", "role": "Full_Back", "role_oop": "Pressing_Full_Back_OOP"}, ...])
        
    Returns:
        List of PositionRequirement objects
    """
    requirements = []
    
    for pos_data in formation_data:
        requirements.append(PositionRequirement(
            position=pos_data["position"],
            role=pos_data["role"],
            role_oop=pos_data.get("role_oop"),
        ))
    
    return requirements


def _resolve_multiplier_col(key: str, available_cols: set) -> str | None:
    mapped = METRIC_COLUMN_MAP.get(key)
    if mapped and mapped in available_cols:
        return mapped
    for candidate in (f"{key}_Normalized", f"{key.replace(' ', '_')}_Normalized"):
        if candidate in available_cols:
            return candidate
    return None


def optimize_teams(
    team_name: str,
    formation_file: str,
    max_teams: int = None,
    age_penalty: float = 0.0,
    age_threshold: int = 30,
    excluded_players: list[str] = None,
    by_formation: bool = False,
    arabic_penalty: float = None,
) -> List[pd.DataFrame]:

    data_dir = Path("data")
    scores_path = data_dir / team_name / "scores" / f"{team_name}_scores.csv"
    output_dir = data_dir / team_name / "teams"
    if by_formation:
        output_dir = output_dir / Path(formation_file).stem
    output_dir.mkdir(parents=True, exist_ok=True)

    scores_df = pd.read_csv(scores_path)
    positions_path = data_dir / team_name / "interim" / "positions.csv"
    positions_df = pd.read_csv(positions_path)

    # demographics (age, club)
    demographics_path = data_dir / team_name / "interim" / "player_demographics.csv"
    if demographics_path.exists():
        try:
            demo_df = pd.read_csv(demographics_path)
            age_col = next((c for c in demo_df.columns if c.lower() == "age"), None)
            club_col = next((c for c in demo_df.columns if c.lower() == "club"), None)
            demo_cols = ["Name"]
            rename_map = {}
            if age_col:
                demo_cols.append(age_col)
                rename_map[age_col] = "Age"
            if club_col:
                demo_cols.append(club_col)
                rename_map[club_col] = "Club"
            demo_subset = demo_df[demo_cols].rename(columns=rename_map)
            scores_df = scores_df.merge(demo_subset, on="Name", how="left")
        except Exception:
            print(f"Warning: failed to read demographics from {demographics_path}")

    # merge all _Normalized columns from performance.csv
    performance_path = data_dir / team_name / "interim" / "performance.csv"
    if performance_path.exists():
        try:
            perf_df = pd.read_csv(performance_path)
            norm_cols = [c for c in perf_df.columns if c.endswith('_Normalized')]
            if norm_cols:
                for c in norm_cols:
                    perf_df[c] = pd.to_numeric(perf_df[c], errors='coerce').fillna(0.0)
                scores_df = scores_df.merge(perf_df[['Name'] + norm_cols], on='Name', how='left')
                for c in norm_cols:
                    if c in scores_df.columns:
                        scores_df[c] = scores_df[c].fillna(0.0)
        except Exception:
            print(f"Warning: failed to read performance data from {performance_path}")

    # config
    with open(formation_file, "r") as f:
        config = json.load(f)

    formation_data = config["formation"]

    cfg_age_penalty = config.get("age_penalty")
    cfg_age_threshold = config.get("age_threshold")
    cfg_arabic_penalty = config.get("arabic_penalty")
    ip_weight = float(config.get("ip_weight", 0.5))

    if age_penalty is None:
        age_penalty = float(cfg_age_penalty) if cfg_age_penalty is not None else 0.0
    if age_threshold is None:
        age_threshold = int(cfg_age_threshold) if cfg_age_threshold is not None else 30
    if arabic_penalty is None:
        arabic_penalty = float(cfg_arabic_penalty) if cfg_arabic_penalty is not None else 0.0

    # resolve multiplier keys → actual column names
    raw_multipliers = config.get("multipliers", {})
    available_cols = set(scores_df.columns)
    resolved_multipliers: Dict[str, float] = {}
    for key, weight in raw_multipliers.items():
        col = _resolve_multiplier_col(key, available_cols)
        if col:
            resolved_multipliers[col] = weight
        else:
            print(f"Warning: multiplier key '{key}' has no matching column, skipping.")

    requirements = parse_formation(formation_data)

    teams: List[pd.DataFrame] = []

    excluded = set()
    if excluded_players:
        excluded.update(n.casefold() for n in excluded_players)

    team_idx = 1

    def filename_for_index(i: int) -> Path:
        if i == 1:
            return output_dir / "first_team.csv"
        if i == 2:
            return output_dir / "second_team.csv"
        return output_dir / f"team_{i}.csv"

    while True:
        optimizer = TeamOptimizer(
            scores_df,
            positions_df,
            list(excluded),
            age_penalty=age_penalty,
            age_threshold=age_threshold,
            multipliers=resolved_multipliers,
            arabic_penalty=arabic_penalty,
            ip_weight=ip_weight,
        )

        team_df = optimizer.optimize_team(requirements)

        if team_df is None or team_df.empty:
            break
        if "Name" not in team_df.columns:
            break
        if team_df["Name"].eq("No eligible player").any():
            break

        out_path = filename_for_index(team_idx)
        team_df.to_csv(out_path, index=False)
        teams.append(team_df)

        # adiciona jogadores usados ao exclude
        selected_names = [
            n.casefold()
            for n in team_df["Name"].tolist()
            if isinstance(n, str)
        ]
        excluded.update(selected_names)

        team_idx += 1
        if max_teams is not None and team_idx > max_teams:
            break

    if teams:
        print(f"Salvei {len(teams)} times em: {output_dir}")
    else:
        print("Não foi possível formar nenhum time completo.")

    return teams