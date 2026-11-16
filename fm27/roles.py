from typing import Iterable

import pandas as pd


class Role:
    """
    Role base class.
    - tier1 attributes get weight_t1
    - tier2 attributes get weight_t2
    - score(player) returns weighted mean across present attributes
    - player can be a dict or a pandas.Series
    """
    def __init__(self, name: str, tier1: Iterable[str], tier2: Iterable[str],
                 weight_t1: float = 3, weight_t2: float = 2):
        self.name = name
        self.weights = {}
        for a in tier1:
            self.weights[a] = weight_t1
        for a in tier2:
            if a not in self.weights:
                self.weights[a] = weight_t2

    def score(self, player):
        """
        player: dict-like (or pandas.Series)
        Returns the weighted mean: sum(w * val) / sum(w for present attrs).
        Ignores attributes that are missing or NaN.
        If no attributes are present, returns 0.0.
        """
        num = 0.0
        den = 0.0
        for attr, w in self.weights.items():
            # works for dict and pd.Series
            try:
                val = player.get(attr, None)
            except Exception:
                # fallback if player is not dict-like
                val = getattr(player, attr, None)

            if val is None:
                continue
            if pd.isna(val):
                continue
            try:
                v = float(val)
            except Exception:
                # handle ranged attributes like "7-10" → midpoint 8.5
                try:
                    parts = str(val).split('-')
                    v = (float(parts[0]) + float(parts[1])) / 2
                except Exception:
                    continue

            num += w * v
            den += w

        if den == 0:
            return 0.0
        return num / den

# =====================================================================
# FM27 roles
#
# Each entry: (name, tier1, tier2). Score column = name with spaces -> "_"
# plus "_Score"; configs refer to a role by that underscored name
# (e.g. "Ball_Playing_Centre_Back", "Covering_Centre_Back_OOP").
# In-possession roles have plain names; every out-of-possession role ends in
# " OOP". A role listed under several positions in the game (e.g. Winger in
# M and AM) has the same tiers everywhere, so it is defined once.
# =====================================================================

OTB = "Off The Ball"

ROLE_DEFINITIONS = [
    # ---------------- GK ----------------
    # in possession
    ("Goalkeeper",
     ["Aerial Reach", "Command Of Area", "Communication", "Handling", "Reflexes", "Concentration", "Positioning", "Agility"],
     ["Kicking", "One On Ones", "Anticipation", "Decisions"]),
    ("No Nonsense Goalkeeper",
     ["Aerial Reach", "Command Of Area", "Communication", "Handling", "Reflexes", "Concentration", "Positioning", "Agility"],
     ["One On Ones", "Anticipation", "Decisions"]),
    ("Ball Playing Goalkeeper",
     ["Aerial Reach", "Command Of Area", "Communication", "Handling", "Kicking", "Reflexes", "Concentration", "Positioning", "Agility"],
     ["Eccentricity", "One On Ones", "Passing", "Throwing", "Anticipation", "Composure", "Decisions"]),
    # out of possession
    ("Sweeper Keeper OOP",
     ["Aerial Reach", "Command Of Area", "Communication", "Handling", "One On Ones", "Reflexes", "Rushing Out", "Anticipation", "Decisions", "Agility"],
     ["Eccentricity", "Concentration", "Positioning", "Acceleration"]),
    ("Goalkeeper OOP",
     ["Aerial Reach", "Command Of Area", "Communication", "Handling", "Reflexes", "Concentration", "Positioning", "Agility"],
     ["One On Ones", "Rushing Out", "Anticipation", "Decisions"]),
    ("Line Holding Goalkeeper OOP",
     ["Aerial Reach", "Command Of Area", "Communication", "Handling", "Reflexes", "Concentration", "Positioning", "Agility"],
     ["One On Ones", "Anticipation", "Decisions"]),

    # ---------------- D(C) ----------------
    ("Ball Playing Centre Back",
     ["Heading", "Marking", "Passing", "Tackling", "Anticipation", "Composure", "Positioning", "Jumping Reach", "Strength"],
     ["First Touch", "Technique", "Aggression", "Bravery", "Concentration", "Decisions", "Vision", "Pace"]),
    ("Advanced Centre Back",
     ["Heading", "Marking", "Passing", "Tackling", "Technique", "Anticipation", "Composure", "Decisions", "Positioning", "Team Work", "Jumping Reach", "Strength"],
     ["Dribbling", "First Touch", "Aggression", "Bravery", "Concentration", "Vision", "Pace", "Stamina"]),
    ("Overlapping Centre Back",
     ["Crossing", "Heading", "Marking", "Tackling", "Anticipation", "Work Rate", "Jumping Reach", "Pace", "Stamina", "Strength"],
     ["Dribbling", "Technique", "Aggression", "Bravery", "Composure", "Concentration", "Decisions", OTB, "Positioning", "Acceleration", "Agility"]),
    ("No Nonsense Centre Back",
     ["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
     ["Aggression", "Bravery", "Concentration", "Pace"]),
    ("Centre Back",
     ["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
     ["Aggression", "Bravery", "Composure", "Concentration", "Decisions", "Pace"]),
    ("Wide Centre Back",
     ["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
     ["Dribbling", "Aggression", "Bravery", "Composure", "Concentration", "Decisions", "Work Rate", "Acceleration", "Agility", "Pace", "Stamina"]),
    ("Centre Back OOP",
     ["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
     ["Aggression", "Bravery", "Composure", "Concentration", "Decisions", "Pace"]),
    ("Wide Centre Back OOP",
     ["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
     ["Aggression", "Bravery", "Concentration", "Decisions", "Acceleration", "Agility", "Pace"]),
    ("Stopping Wide Centre Back OOP",
     ["Heading", "Marking", "Tackling", "Aggression", "Anticipation", "Bravery", "Positioning", "Jumping Reach", "Strength"],
     ["Concentration", "Decisions", "Acceleration", "Agility", "Pace"]),
    ("Stopping Centre Back OOP",
     ["Heading", "Marking", "Tackling", "Aggression", "Anticipation", "Bravery", "Positioning", "Jumping Reach", "Strength"],
     ["Concentration", "Decisions", "Pace"]),
    ("Covering Wide Centre Back OOP",
     ["Heading", "Marking", "Tackling", "Anticipation", "Concentration", "Decisions", "Positioning", "Jumping Reach", "Pace", "Strength"],
     ["Bravery", "Acceleration", "Agility"]),
    ("Covering Centre Back OOP",
     ["Heading", "Marking", "Tackling", "Anticipation", "Concentration", "Decisions", "Positioning", "Jumping Reach", "Pace", "Strength"],
     ["Bravery", "Acceleration"]),

    # ---------------- D(R/L) ----------------
    ("Inside Full Back",
     ["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Strength"],
     ["Dribbling", "Aggression", "Bravery", "Composure", "Concentration", "Decisions", "Work Rate", "Acceleration", "Agility", "Jumping Reach", "Pace", "Stamina"]),
    ("Full Back",
     ["Marking", "Tackling", "Anticipation", "Concentration", "Positioning", "Team Work", "Acceleration"],
     ["Crossing", "Dribbling", "Passing", "Technique", "Decisions", "Work Rate", "Agility", "Pace", "Stamina"]),
    ("Holding Full Back OOP",
     ["Marking", "Tackling", "Anticipation", "Concentration", "Decisions", "Positioning", "Acceleration"],
     ["Team Work", "Agility", "Pace"]),
    ("Pressing Full Back OOP",
     ["Marking", "Tackling", "Aggression", "Anticipation", "Positioning", "Team Work", "Work Rate", "Acceleration"],
     ["Bravery", "Concentration", "Decisions", "Agility", "Pace", "Stamina"]),
    ("Full Back OOP",
     ["Marking", "Tackling", "Anticipation", "Positioning", "Team Work", "Acceleration"],
     ["Aggression", "Concentration", "Decisions", "Work Rate", "Agility", "Pace", "Stamina"]),

    # ---------------- D(R/L) and WB(R/L) ----------------
    ("Inside Wing Back",
     ["Passing", "Tackling", "Anticipation", "Composure", "Decisions", "Positioning", "Team Work", "Acceleration"],
     ["First Touch", "Marking", "Technique", "Concentration", "Work Rate", "Agility", "Pace", "Stamina"]),
    ("Playmaking Wing Back",
     ["First Touch", "Passing", "Tackling", "Technique", "Composure", "Decisions", "Team Work", "Vision", "Acceleration"],
     ["Crossing", "Dribbling", "Marking", "Anticipation", "Concentration", OTB, "Positioning", "Work Rate", "Agility", "Pace", "Stamina"]),
    ("Wing Back",
     ["Crossing", "Marking", "Tackling", "Team Work", "Work Rate", "Acceleration", "Pace", "Stamina"],
     ["Dribbling", "First Touch", "Passing", "Technique", "Anticipation", "Concentration", "Decisions", OTB, "Positioning", "Agility", "Balance"]),

    # ---------------- WB(R/L) ----------------
    ("Advanced Wing Back",
     ["Crossing", "Dribbling", "Technique", OTB, "Team Work", "Work Rate", "Acceleration", "Agility", "Pace", "Stamina"],
     ["First Touch", "Marking", "Passing", "Tackling", "Anticipation", "Decisions", "Flair", "Positioning", "Balance"]),
    ("Pressing Wing Back OOP",
     ["Marking", "Tackling", "Aggression", "Anticipation", "Positioning", "Team Work", "Work Rate", "Acceleration", "Stamina"],
     ["Bravery", "Concentration", "Decisions", "Agility", "Pace"]),
    ("Wing Back OOP",
     ["Marking", "Tackling", "Anticipation", "Positioning", "Team Work", "Acceleration", "Stamina"],
     ["Aggression", "Concentration", "Decisions", "Work Rate", "Agility", "Pace"]),
    ("Holding Wing Back OOP",
     ["Marking", "Tackling", "Anticipation", "Concentration", "Decisions", "Positioning", "Acceleration"],
     ["Team Work", "Agility", "Pace", "Stamina"]),

    # ---------------- DM ----------------
    ("Box To Box Midfielder",
     ["Passing", "Tackling", OTB, "Team Work", "Work Rate", "Stamina"],
     ["Dribbling", "Finishing", "First Touch", "Long Shots", "Technique", "Aggression", "Anticipation", "Composure", "Decisions", "Positioning", "Acceleration", "Balance", "Pace", "Strength"]),
    ("Deep Lying Playmaker",
     ["First Touch", "Passing", "Technique", "Composure", "Decisions", "Team Work", "Vision"],
     ["Marking", "Tackling", "Anticipation", "Concentration", OTB, "Positioning", "Work Rate", "Balance", "Stamina"]),
    ("Defensive Midfielder",
     ["Tackling", "Anticipation", "Concentration", "Positioning", "Team Work"],
     ["First Touch", "Marking", "Passing", "Aggression", "Composure", "Decisions", "Work Rate", "Stamina", "Strength"]),
    ("Half Back",
     ["Heading", "Marking", "Tackling", "Anticipation", "Concentration", "Positioning", "Team Work", "Jumping Reach", "Strength"],
     ["First Touch", "Passing", "Aggression", "Bravery", "Composure", "Decisions", "Work Rate", "Stamina"]),
    ("Box To Box Playmaker",
     ["First Touch", "Passing", "Technique", "Composure", "Decisions", OTB, "Team Work", "Vision", "Work Rate", "Stamina"],
     ["Dribbling", "Long Shots", "Marking", "Tackling", "Anticipation", "Positioning", "Acceleration", "Agility", "Balance", "Pace"]),
    ("Defensive Midfielder OOP",
     ["Tackling", "Anticipation", "Decisions", "Positioning", "Team Work", "Work Rate"],
     ["Marking", "Aggression", "Concentration", "Stamina", "Strength"]),
    ("Wide Covering Defensive Midfielder OOP",
     ["Marking", "Tackling", "Anticipation", "Decisions", "Positioning", "Team Work", "Work Rate", "Agility", "Stamina"],
     ["Aggression", "Concentration", "Pace", "Strength"]),
    ("Pressing Defensive Midfielder OOP",
     ["Tackling", "Aggression", "Anticipation", "Decisions", "Positioning", "Team Work", "Work Rate", "Stamina"],
     ["Marking", "Concentration", "Pace", "Strength"]),
    ("Screening Defensive Midfielder OOP",
     ["Marking", "Tackling", "Anticipation", "Concentration", "Decisions", "Positioning"],
     ["Team Work", "Work Rate", "Stamina", "Strength"]),
    ("Dropping Defensive Midfielder OOP",
     ["Marking", "Tackling", "Anticipation", "Concentration", "Decisions", "Positioning", "Team Work", "Work Rate", "Jumping Reach", "Strength"],
     ["Aggression", "Stamina"]),

    # ---------------- M(R/L) and AM(R/L) ----------------
    ("Playmaking Winger",
     ["Crossing", "Dribbling", "First Touch", "Passing", "Technique", "Composure", "Decisions", OTB, "Team Work", "Vision", "Acceleration"],
     ["Anticipation", "Flair", "Work Rate", "Agility", "Pace", "Stamina"]),
    ("Inside Winger",
     ["Dribbling", "First Touch", "Technique", "Composure", "Team Work", "Acceleration", "Agility"],
     ["Crossing", "Long Shots", "Passing", "Anticipation", "Flair", OTB, "Vision", "Work Rate", "Balance", "Pace", "Stamina"]),
    ("Winger",
     ["Crossing", "Dribbling", "Technique", "Team Work", "Acceleration", "Agility", "Pace"],
     ["First Touch", "Passing", "Anticipation", "Flair", OTB, "Work Rate", "Balance", "Stamina"]),

    # ---------------- M(R/L) ----------------
    ("Wide Midfielder",
     ["Crossing", "Passing", "Technique", "Decisions", "Team Work", "Work Rate", "Pace", "Stamina"],
     ["Dribbling", "First Touch", "Anticipation", "Composure", OTB, "Vision", "Acceleration", "Agility"]),
    ("Wide Midfielder OOP",
     ["Decisions", "Team Work", "Work Rate", "Acceleration"],
     ["Marking", "Aggression", "Anticipation", OTB, "Agility", "Pace", "Stamina"]),
    ("Wide Outlet Wide Midfielder OOP",
     ["Anticipation", "Concentration", "Decisions", OTB, "Team Work", "Pace"],
     ["Dribbling", "First Touch", "Marking", "Composure", "Acceleration", "Agility"]),
    ("Tracking Wide Midfielder OOP",
     ["Aggression", "Anticipation", "Decisions", "Team Work", "Work Rate", "Acceleration", "Stamina"],
     ["Marking", "Tackling", OTB, "Positioning", "Agility", "Pace"]),

    # ---------------- M(C) and AM(C) ----------------
    ("Advanced Playmaker",
     ["First Touch", "Passing", "Technique", "Composure", "Decisions", OTB, "Team Work", "Vision"],
     ["Crossing", "Dribbling", "Anticipation", "Flair", "Acceleration", "Agility"]),
    ("Attacking Midfielder",
     ["First Touch", "Long Shots", "Passing", "Technique", "Composure", "Flair", OTB],
     ["Crossing", "Dribbling", "Finishing", "Anticipation", "Decisions", "Vision", "Acceleration", "Agility"]),
    ("Channel Midfielder",
     ["Crossing", "First Touch", "Passing", "Technique", "Composure", OTB, "Work Rate", "Acceleration"],
     ["Dribbling", "Long Shots", "Anticipation", "Decisions", "Flair", "Vision", "Agility", "Pace", "Stamina"]),

    # ---------------- M(C) ----------------
    ("Midfield Playmaker",
     ["First Touch", "Passing", "Technique", "Composure", "Decisions", OTB, "Team Work", "Vision"],
     ["Dribbling", "Tackling", "Anticipation", "Flair", "Positioning", "Work Rate", "Agility", "Stamina"]),
    ("Central Midfielder",
     ["First Touch", "Passing", "Tackling", "Decisions", "Team Work"],
     ["Technique", "Anticipation", "Composure", "Concentration", OTB, "Positioning", "Vision", "Work Rate", "Stamina"]),
    ("Wide Central Midfielder",
     ["First Touch", "Passing", "Tackling", "Decisions", "Team Work"],
     ["Crossing", "Dribbling", "Technique", "Anticipation", "Composure", "Concentration", OTB, "Positioning", "Vision", "Work Rate", "Agility", "Stamina"]),
    ("Pressing Central Midfielder OOP",
     ["Tackling", "Aggression", "Anticipation", "Decisions", "Team Work", "Work Rate", "Stamina"],
     ["Marking", "Concentration", "Positioning", "Pace", "Strength"]),
    ("Central Midfielder OOP",
     ["Tackling", "Decisions", "Team Work", "Work Rate"],
     ["Marking", "Aggression", "Anticipation", "Concentration", "Positioning", "Stamina"]),
    ("Wide Covering Central Midfielder OOP",
     ["Marking", "Tackling", "Decisions", "Team Work", "Work Rate", "Agility", "Stamina"],
     ["Aggression", "Anticipation", "Concentration", "Positioning", "Pace"]),
    ("Screening Central Midfielder OOP",
     ["Marking", "Tackling", "Concentration", "Decisions", "Positioning"],
     ["Anticipation", "Team Work", "Work Rate", "Stamina"]),

    # ---------------- AM(R/L) ----------------
    ("Inside Forward",
     ["Dribbling", "First Touch", "Technique", "Anticipation", "Composure", OTB, "Acceleration", "Agility"],
     ["Crossing", "Finishing", "Long Shots", "Passing", "Flair", "Vision", "Work Rate", "Balance", "Pace", "Stamina"]),
    ("Wide Forward",
     ["Dribbling", "First Touch", "Technique", "Anticipation", OTB, "Acceleration", "Agility", "Pace"],
     ["Crossing", "Finishing", "Passing", "Composure", "Flair", "Work Rate", "Balance", "Stamina"]),
    ("Inside Outlet Winger OOP",
     ["Anticipation", "Concentration", "Decisions", OTB, "Team Work", "Balance"],
     ["Dribbling", "First Touch", "Marking", "Composure", "Acceleration", "Strength"]),
    ("Winger OOP",
     ["Anticipation", "Decisions", "Team Work", "Work Rate", "Acceleration"],
     ["Marking", "Aggression", OTB, "Agility", "Pace", "Stamina"]),
    ("Wide Outlet Winger OOP",
     ["Anticipation", "Concentration", "Decisions", OTB, "Team Work", "Pace"],
     ["Dribbling", "First Touch", "Marking", "Composure", "Acceleration", "Agility"]),
    ("Tracking Winger OOP",
     ["Aggression", "Anticipation", "Decisions", "Team Work", "Work Rate", "Acceleration", "Stamina"],
     ["Marking", "Tackling", OTB, "Positioning", "Agility", "Pace"]),

    # ---------------- AM(C) ----------------
    ("Free Role",
     ["Dribbling", "First Touch", "Long Shots", "Passing", "Technique", "Composure", "Flair", OTB, "Vision"],
     ["Crossing", "Finishing", "Anticipation", "Decisions", "Acceleration", "Agility"]),
    ("Second Striker",
     ["Finishing", "First Touch", "Anticipation", "Composure", OTB, "Acceleration"],
     ["Dribbling", "Long Shots", "Passing", "Technique", "Concentration", "Decisions", "Work Rate", "Agility", "Pace", "Stamina"]),
    ("Tracking Attacking Midfielder OOP",
     ["Aggression", "Anticipation", "Decisions", "Team Work", "Work Rate", "Stamina"],
     ["Marking", OTB]),
    ("Central Outlet Attacking Midfielder OOP",
     ["Anticipation", "Concentration", "Decisions", OTB, "Team Work", "Balance"],
     ["First Touch", "Marking", "Composure", "Strength"]),
    ("Attacking Midfielder OOP",
     ["Anticipation", "Decisions", "Work Rate"],
     ["Marking", "Aggression", OTB, "Team Work", "Stamina"]),
    ("Splitting Outlet Attacking Midfielder OOP",
     ["Anticipation", "Concentration", "Decisions", OTB, "Team Work", "Pace"],
     ["First Touch", "Marking", "Composure", "Acceleration"]),

    # ---------------- ST ----------------
    ("Target Forward",
     ["Finishing", "Heading", "Aggression", "Bravery", "Composure", OTB, "Balance", "Jumping Reach", "Strength"],
     ["First Touch", "Anticipation", "Decisions", "Team Work"]),
    ("Centre Forward",
     ["Finishing", "First Touch", "Heading", "Technique", "Composure", OTB, "Acceleration", "Strength"],
     ["Dribbling", "Passing", "Anticipation", "Decisions", "Agility", "Balance", "Jumping Reach", "Pace"]),
    ("Deep Lying Forward",
     ["Finishing", "First Touch", "Technique", "Composure", OTB, "Strength"],
     ["Dribbling", "Passing", "Anticipation", "Decisions", "Team Work", "Vision", "Balance"]),
    ("Poacher",
     ["Finishing", "Heading", "Anticipation", "Composure", "Concentration", OTB, "Acceleration"],
     ["First Touch", "Technique", "Decisions", "Balance"]),
    ("Channel Forward",
     ["Dribbling", "Finishing", "First Touch", "Technique", "Composure", OTB, "Work Rate", "Acceleration"],
     ["Crossing", "Heading", "Passing", "Anticipation", "Decisions", "Agility", "Balance", "Pace", "Stamina"]),
    ("False Nine",
     ["Dribbling", "First Touch", "Passing", "Technique", "Composure", "Decisions", OTB, "Team Work", "Vision", "Acceleration"],
     ["Finishing", "Anticipation", "Flair", "Agility", "Balance"]),
    ("Centre Forward OOP",
     ["Anticipation", "Decisions", "Work Rate"],
     ["Marking", "Aggression", OTB, "Team Work", "Stamina"]),
    ("Tracking Centre Forward OOP",
     ["Aggression", "Anticipation", "Decisions", "Team Work", "Work Rate", "Stamina"],
     ["Marking", OTB, "Positioning"]),
    ("Central Outlet Centre Forward OOP",
     ["Anticipation", "Concentration", "Decisions", OTB, "Team Work", "Balance"],
     ["First Touch", "Marking", "Composure", "Strength"]),
    ("Splitting Outlet Centre Forward OOP",
     ["Anticipation", "Concentration", "Decisions", OTB, "Team Work", "Pace"],
     ["First Touch", "Marking", "Composure", "Acceleration"]),
]


def build_all_roles():
    """Return one Role per entry in ROLE_DEFINITIONS."""
    names = [n for n, _, _ in ROLE_DEFINITIONS]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise ValueError(f"Duplicate role names: {sorted(dupes)}")
    return [Role(name, t1, t2) for name, t1, t2 in ROLE_DEFINITIONS]
