import os
import sys
from pathlib import Path

import pandas as pd

from .roles import build_all_roles


def calculate_team_scores(team_name: str):
    """Calculate role scores for a team and save the results.
    
    Args:
        team_name: Name of the team (lowercase)
    """
    # Set up paths
    data_dir = Path("data")
    team_interim_dir = data_dir / team_name / "interim"
    team_scores_dir = data_dir / team_name / "scores"
    
    # Ensure scores directory exists
    os.makedirs(team_scores_dir, exist_ok=True)
    
    # Read input files from interim folder
    attr_file = team_interim_dir / "attributes.csv"
    pos_file = team_interim_dir / "positions.csv"
    
    attr = pd.read_csv(attr_file)
    pos = pd.read_csv(pos_file)
    
    # Merge data
    df = attr.merge(pos, on=["Name", "UID"], how="inner")
    
    # Calculate scores
    roles = build_all_roles()
    
    for role in roles:
        col = role.name.replace(" ", "_") + "_Score"
        df[col] = df.apply(role.score, axis=1)
    
    # Keep only Name, UID and score columns
    score_cols = [role.name.replace(" ", "_") + "_Score" for role in roles]
    output_df = df[['Name', 'UID'] + score_cols]
    output_file = team_scores_dir / f"{team_name}_scores.csv"
    output_df.to_csv(output_file, index=False)
    print(f"Scores saved to {output_file}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m fm26.calculate <team_name>")
        print("Example: python -m fm26.calculate roma")
        sys.exit(1)
    
    team_name = sys.argv[1].lower()
    calculate_team_scores(team_name)