import re
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


def _num(raw):
    """float(raw), or None for NaN / non-numeric."""
    try:
        val = float(raw)
    except (TypeError, ValueError):
        return None
    return None if pd.isna(val) else val


class TeamOptimizer:
    """Optimizes team selection based on player scores and required positions."""

    def __init__(self, scores_df: pd.DataFrame, positions_df: pd.DataFrame, exclude_players: List[str] = None,
                 age_penalty: float = 0.0, age_threshold: int = 30,
                 multipliers: Dict[str, float] = None, arabic_penalty: float = 0.0,
                 ip_weight: float = 0.5, fatigue_penalty: float = 0.0):
        self.scores_df = scores_df
        self.positions_df = positions_df
        self.selected_players = set()
        self.age_penalty = float(age_penalty or 0.0)
        self.age_threshold = int(age_threshold or 0)
        self.multipliers = multipliers or {}
        self.arabic_penalty = float(arabic_penalty or 0.0)
        # Points off per 90 minutes played in the Match Load window (last 14 days); goalkeepers exempt.
        self.fatigue_penalty = float(fatigue_penalty or 0.0)
        # Weight of the in-possession role when a slot also has an OOP role.
        self.ip_weight = float(ip_weight)
        if not 0.0 <= self.ip_weight <= 1.0:
            raise ValueError(f"ip_weight must be between 0 and 1, got {self.ip_weight}")
        if exclude_players:
            self.selected_players.update(exclude_players)
        # Row lookup by name (names are unique: the parser numbers homonyms).
        self._rows = scores_df.drop_duplicates('Name').set_index('Name', drop=False)
        self._pos = positions_df.drop_duplicates('Name').set_index('Name')

    def check_requirements(self, requirements: List[PositionRequirement]):
        for req in requirements:
            for col in (req.get_score_column(), req.get_oop_score_column()):
                if col and col not in self.scores_df.columns:
                    raise ValueError(f"Score column '{col}' not found in scores file (check the role name).")
            if req.position not in self.positions_df.columns:
                raise ValueError(f"Position column '{req.position}' not found in positions file.")

    def components(self, name: str, req: PositionRequirement) -> dict | None:
        """The slot score of `name` in `req`, split into its parts; None if he can't play that position.

        This is the only place a slot score is computed: optimize_team ranks on `total`, and
        --explain / --top print these same parts. Keys: ip, oop (None without an OOP role),
        blend, age, arabic, fatigue, mult {column: weight * z}, total."""
        if name not in self._rows.index or name not in self._pos.index:
            return None
        if self._pos.at[name, req.position] != True:  # noqa: E712 (column may hold numpy bools)
            return None
        row = self._rows.loc[name]
        ip = row[req.get_score_column()]
        oop_col = req.get_oop_score_column()
        oop = row[oop_col] if oop_col else None
        blend = self.ip_weight * ip + (1 - self.ip_weight) * oop if oop_col else ip
        total = blend
        age = arabic = fatigue = 0.0
        if self.age_penalty and 'Age' in row.index:
            age_val = _num(row['Age'])
            if age_val is not None:
                age = -self.age_penalty * max(0, age_val - self.age_threshold) + 0.0  # + 0.0: no '-0.00'
                total = total + age
        if self.arabic_penalty and 'Club' in row.index:
            club_val = row['Club']
            if isinstance(club_val, str) and club_val.lower().startswith('al-'):
                arabic = -self.arabic_penalty
                total = total + arabic
        if self.fatigue_penalty and 'MatchLoadMinutes' in row.index and str(row.get('IsGK')).casefold() != 'true':
            minutes = _num(row['MatchLoadMinutes'])
            if minutes:
                fatigue = -self.fatigue_penalty * minutes / 90
                total = total + fatigue
        mult = {}
        for col, weight in self.multipliers.items():
            if not weight or col not in row.index:
                continue
            mult[col] = weight * (_num(row[col]) or 0.0)
            total = total + mult[col]
        return {'ip': float(ip), 'oop': None if oop is None else float(oop), 'blend': float(blend),
                'age': age, 'arabic': arabic, 'fatigue': fatigue, 'mult': mult, 'total': float(total)}

    def optimize_team(self, requirements: List[PositionRequirement]) -> pd.DataFrame:
        """
        Globally optimize team selection to maximize total score using Hungarian algorithm.
        Args:
            requirements: List of position requirements
        Returns:
            DataFrame with selected players and their scores. A slot nobody can fill gets
            'No eligible player' (the caller stops building teams there).
        """
        self.check_requirements(requirements)
        excluded = {p.lower() for p in self.selected_players}
        available_scores_df = self.scores_df[~self.scores_df['Name'].str.lower().isin(excluded)]
        available_players = available_scores_df['Name'].tolist()
        n_positions = len(requirements)
        n_players = len(available_players)

        # Build cost matrix (negative scores for maximization, ineligible assignments get large positive)
        cost_matrix = np.full((n_positions, n_players), 1e9)  # Default to ineligible
        adjusted_scores = np.full((n_positions, n_players), np.nan)
        for i, req in enumerate(requirements):
            for j, player_name in enumerate(available_players):
                parts = self.components(player_name, req)
                if parts is not None:
                    cost_matrix[i, j] = -parts['total']
                    adjusted_scores[i, j] = parts['total']
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
    # case-insensitive fallback ('av rat' -> 'Av Rat', 'last 5 games' -> 'Last 5 Games')
    folded = key.casefold()
    for name, col in METRIC_COLUMN_MAP.items():
        if name.casefold() == folded and col in available_cols:
            return col
    by_fold = {c.casefold(): c for c in available_cols}
    for candidate in (f"{key}_Normalized", f"{key.replace(' ', '_')}_Normalized"):
        if candidate.casefold() in by_fold:
            return by_fold[candidate.casefold()]
    return None


def teams_output_dir(team_name: str, formation_file, by_formation: bool = False) -> Path:
    """Folder the team CSVs of a run are saved in."""
    out = Path("data") / team_name / "teams"
    return out / Path(formation_file).stem if by_formation else out


def remove_stale_teams(output_dir: Path, saved: int) -> List[str]:
    """Delete team files numbered above `saved` (first_team=1, second_team=2, team_K=K) left by older runs."""
    removed = []
    for path in sorted(output_dir.glob("*.csv")):
        m = re.fullmatch(r"team_(\d+)", path.stem)
        idx = {"first_team": 1, "second_team": 2}.get(path.stem) or (int(m.group(1)) if m else None)
        if idx and idx > saved:
            path.unlink()
            removed.append(path.name)
    return removed


def load_scoring(team_name: str, config: dict, strict_mult_keys=(), warn: bool = True):
    """Scores + positions of a parsed team and the TeamOptimizer settings of `config`.

    Returns (scores_df, positions_df, settings, requirements); `settings` are TeamOptimizer kwargs.
    Multiplier keys in `strict_mult_keys` that match no column are an error instead of a warning."""
    data_dir = Path("data")
    scores_df = pd.read_csv(data_dir / team_name / "scores" / f"{team_name}_scores.csv")
    positions_df = pd.read_csv(data_dir / team_name / "interim" / "positions.csv")

    # demographics (age, club, match load)
    demographics_path = data_dir / team_name / "interim" / "player_demographics.csv"
    if demographics_path.exists():
        try:
            demo_df = pd.read_csv(demographics_path)
            rename_map = {}
            for want in ("Age", "Club"):
                col = next((c for c in demo_df.columns if c.lower() == want.lower()), None)
                if col:
                    rename_map[col] = want
            extra = [c for c in ("MatchLoadMinutes", "IsGK") if c in demo_df.columns]
            demo_subset = demo_df[["Name", *rename_map, *extra]].rename(columns=rename_map)
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

    cfg_age_threshold = config.get("age_threshold")
    settings = {
        "age_penalty": float(config.get("age_penalty") or 0.0),
        "age_threshold": int(cfg_age_threshold) if cfg_age_threshold is not None else 30,
        "arabic_penalty": float(config.get("arabic_penalty") or 0.0),
        "fatigue_penalty": float(config.get("fatigue_penalty") or 0.0),
        "ip_weight": float(config.get("ip_weight", 0.5)),
    }

    # resolve multiplier keys → actual column names
    available_cols = set(scores_df.columns)
    resolved_multipliers: Dict[str, float] = {}
    for key, weight in (config.get("multipliers") or {}).items():
        col = _resolve_multiplier_col(key, available_cols)
        if col:
            resolved_multipliers[col] = weight
        elif key in strict_mult_keys:
            usable = sorted(k[:-len("_Normalized")].replace("_", " ") for k in available_cols
                            if k.endswith("_Normalized"))
            print(f"Error: --mult '{key}' matches no column. Available keys: "
                  f"{', '.join(list(METRIC_COLUMN_MAP) + usable)}")
            exit(1)
        elif warn:
            print(f"Warning: multiplier key '{key}' has no matching column, skipping.")
    settings["multipliers"] = resolved_multipliers

    return scores_df, positions_df, settings, parse_formation(config["formation"])


def optimize_teams(
    team_name: str,
    formation_file: str,
    max_teams: int = None,
    excluded_players: list[str] = None,
    by_formation: bool = False,
    config: dict = None,
    strict_mult_keys=(),
    quiet: bool = False,
) -> List[pd.DataFrame]:
    """Build teams 1..N for a formation and save them as CSVs. `config` is the effective config dict
    (defaults to loading `formation_file`, which is still used for the output folder name).
    Each further team is picked from whoever is left; it stops at the first slot nobody can fill."""
    output_dir = teams_output_dir(team_name, formation_file, by_formation)
    output_dir.mkdir(parents=True, exist_ok=True)

    if config is None:
        with open(formation_file, "r") as f:
            config = json.load(f)
    scores_df, positions_df, settings, requirements = load_scoring(team_name, config, strict_mult_keys)

    teams: List[pd.DataFrame] = []
    excluded = {n.casefold() for n in (excluded_players or [])}

    def filename_for_index(i: int) -> Path:
        if i == 1:
            return output_dir / "first_team.csv"
        if i == 2:
            return output_dir / "second_team.csv"
        return output_dir / f"team_{i}.csv"

    stop = None
    while max_teams is None or len(teams) < max_teams:
        optimizer = TeamOptimizer(scores_df, positions_df, list(excluded), **settings)
        team_df = optimizer.optimize_team(requirements)
        if team_df is None or team_df.empty or "Name" not in team_df.columns:
            break
        missing = team_df[team_df["Name"].eq("No eligible player")]
        if not missing.empty:
            stop = ', '.join(missing["Position"].tolist())
            break

        team_df.to_csv(filename_for_index(len(teams) + 1), index=False)
        teams.append(team_df)
        excluded.update(n.casefold() for n in team_df["Name"].tolist() if isinstance(n, str))

    if teams:
        if not quiet:
            tail = f" (time {len(teams) + 1} sem jogador para {stop})" if stop else ""
            print(f"Salvei {len(teams)} times em: {output_dir}{tail}")
        removed = remove_stale_teams(output_dir, len(teams))
        if removed and not quiet:
            print(f"Removed stale files from older runs: {', '.join(removed)}")
    else:
        print("Não foi possível formar nenhum time completo." + (f" Sem jogador para {stop}." if stop else ""))

    return teams
