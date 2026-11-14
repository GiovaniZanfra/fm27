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
    

class SweeperKeeper(Role):
    def __init__(self):
        super().__init__("Sweeper Keeper",
            tier1=["Command Of Area", "Kicking", "One On Ones", "Reflexes", "Rushing Out", "Anticipation", "Composure", "Concentration", "Positioning", "Agility"],
            tier2=["Aerial Reach", "Communication", "First Touch", "Handling", "Passing", "Throwing", "Decisions", "Vision", "Acceleration"]
        )

class Goalkeeper(Role):
    def __init__(self):
        super().__init__("GoalKeeper",
            tier1=["Aerial Reach", "Command Of Area", "Communication", "Handling", "Kicking", "Reflexes", "Concentration", "Positioning", "Agility"],
            tier2=["One On Ones", "Throwing", "Anticipation", "Decisions"]
        )

# -----------------------------
# DEFENSIVE / WINGS ROLES
# -----------------------------
class WingBack(Role):
    def __init__(self):
        super().__init__("Wing Back",
            tier1=["Crossing", "Marking", "Tackling", "Team Work", "Work Rate", "Acceleration", "Pace", "Stamina"],
            tier2=["Dribbling", "First Touch", "Passing", "Technique", "Anticipation", "Concentration", "Decisions", "Off The Ball", "Positioning", "Agility", "Balance"]
        )

class PlaymakingWingBack(Role):
    def __init__(self):
        super().__init__("Playmaking Wing Back",
            tier1=["First Touch", "Passing", "Tackling", "Technique", "Composure", "Decisions", "Team Work", "Vision", "Acceleration"],
            tier2=["Crossing", "Dribbling", "Marking", "Anticipation", "Concentration", "Off The Ball", "Positioning", "Work Rate", "Agility", "Pace", "Stamina"]
        )

class InvertedWingBack(Role):
    def __init__(self):
        super().__init__("Inverted Wing Back",
            tier1=["First Touch", "Passing", "Tackling", "Technique", "Composure", "Decisions", "Team Work"],
            tier2=["Marking", "Technique", "Anticipation", "Concentration", "Off The Ball", "Positioning", "Vision", "Work Rate", "Acceleration", "Agility", "Stamina"]
        )

class SegundoVolante(Role):
    def __init__(self):
        super().__init__("Segundo Volante",
            tier1=["Marking", "Passing", "Tackling", "Off The Ball", "Positioning", "Work Rate", "Pace", "Stamina"],
            tier2=["Finishing", "First Touch", "Long Shots", "Anticipation", "Composure", "Concentration", "Decisions", "Acceleration", "Balance", "Strength"]
        )

class InsideWingBack(Role):
    def __init__(self):
        super().__init__("Inside Wing Back",
            tier1=["Passing", "Tackling", "Anticipation", "Composure", "Decisions", "Positioning", "Team Work", "Acceleration"],
            tier2=["First Touch", "Marking", "Technique", "Concentration", "Work Rate", "Agility", "Pace", "Stamina"]
        )

class FullBack(Role):
    def __init__(self):
        super().__init__("Full Back",
            tier1=["Marking", "Tackling", "Anticipation", "Concentration", "Positioning", "Team Work", "Acceleration"],
            tier2=["Crossing", "Dribbling", "Passing", "Technique", "Decisions", "Work Rate", "Agility", "Pace", "Stamina"]
        )


class InvertedFullBack(Role):
    def __init__(self):
        super().__init__("Inverted Full Back",
            tier1=["Heading", "Marking", "Tackling", "Positioning", "Strength"],
            tier2=["Dribbling", "First Touch", "Passing", "Technique", "Agression", "Anticipation", "Bravery", "Composure", "Concentration", "Decisions", "Work Rate", "Agility", "Jumping Reach", "Pace"]
        )

class InsideFullBack(Role):
    def __init__(self):
        super().__init__("Inside Full Back",
            tier1=["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Strength"],
            tier2=["Dribbling", "Aggression", "Bravery", "Composure", "Concentration", "Decisions", "Work Rate", "Acceleration", "Agility", "Jumping Reach", "Pace", "Stamina"]
        )

# -----------------------------
# WIDE ATTACKERS / WINGERS
# -----------------------------
class Winger(Role):
    def __init__(self):
        super().__init__("Winger",
            tier1=["Crossing", "Dribbling", "Technique", "Team Work", "Acceleration", "Agility", "Pace"],
            tier2=["First Touch", "Passing", "Anticipation", "Flair", "Off The Ball", "Work Rate", "Balance", "Stamina"]
        )

class WideMidfielder(Role):
    def __init__(self):
        super().__init__("Wide Midfielder",
            tier1=["Crossing", "Passing", "Technique", "Decisions", "Team Work", "Work Rate", "Pace", "Stamina"],
            tier2=["Dribbling", "First Touch", "Anticipation", "Composure", "Off The Ball", "Vision", "Acceleration", "Agility"]
        )

class InsideWinger(Role):
    def __init__(self):
        super().__init__("Inside Winger",
            tier1=["Dribbling", "First Touch", "Technique", "Composure", "Team Work", "Acceleration", "Agility"],
            tier2=["Crossing", "Long Shots", "Passing", "Anticipation", "Flair", "Off The Ball", "Vision", "Work Rate", "Balance", "Pace", "Stamina"]
        )

class InvertedWinger(Role):
    def __init__(self):
        super().__init__("Inverted Winger",
            tier1=["Crossing", "Dribbling", "Passing", "Technique", "Acceleration", "Agility"],
            tier2=["First Touch", "Long Shots", "Anticipation", "Composure", "Decisions", "Flair", "Off The Ball", "Vision", "Work Rate", "Balance", "Pace", "Stamina"]
        )

class PlaymakingWinger(Role):
    def __init__(self):
        super().__init__("Playmaking Winger",
            tier1=["Crossing", "Dribbling", "First Touch", "Passing", "Technique", "Composure", "Decisions", "Off The Ball", "Team Work", "Vision", "Acceleration"],
            tier2=["Anticipation", "Flair", "Work Rate", "Agility", "Pace", "Stamina"]
        )

class WideForward(Role):
    def __init__(self):
        super().__init__("Wide Forward",
            tier1=["Dribbling", "First Touch", "Technique", "Anticipation", "Off The Ball", "Acceleration", "Agility", "Pace"],
            tier2=["Crossing", "Finishing", "Passing", "Composure", "Flair", "Work Rate", "Balance", "Stamina"]
        )

# -----------------------------
# INSIDE / FORWARDS / STRIKERS
# -----------------------------
class InsideForward(Role):
    def __init__(self):
        super().__init__("Inside Forward",
            tier1=["Dribbling", "First Touch", "Technique", "Anticipation", "Composure", "Off The Ball", "Acceleration", "Agility"],
            tier2=["Crossing", "Finishing", "Long Shots", "Passing", "Flair", "Vision", "Work Rate", "Balance", "Pace", "Stamina"]
        )

class FalseNine(Role):
    def __init__(self):
        super().__init__("False Nine",
            tier1=["Dribbling", "First Touch", "Passing", "Technique", "Composure", "Decisions", "Off The Ball", "Team Work", "Vision", "Acceleration"],
            tier2=["Finishing", "Anticipation", "Flair", "Agility", "Balance"]
        )

class ChannelForward(Role):
    def __init__(self):
        super().__init__("Channel Forward",
            tier1=["Dribbling", "Finishing", "First Touch", "Technique", "Off The Ball", "Composure", "Work Rate", "Acceleration"],
            tier2=["Crossing", "Heading", "Passing", "Anticipation", "Decisions", "Agility", "Balance", "Pace", "Stamina"]
        )

class DeepLyingForward(Role):
    def __init__(self):
        super().__init__("Deep Lying Forward",
            tier1=["Finishing", "First Touch", "Technique", "Composure", "Off The Ball", "Strength"],
            tier2=["Dribbling", "Passing", "Anticipation", "Decisions", "Team Work", "Vision", "Balance"]
        )

class CentreForward(Role):
    def __init__(self):
        super().__init__("Centre Forward",
            tier1=["Finishing", "First Touch", "Heading", "Technique", "Composure", "Off The Ball", "Acceleration", "Strength"],
            tier2=["Dribbling", "Passing", "Anticipation", "Decisions", "Agility", "Balance", "Jumping Reach", "Pace"]
        )

class CompleteForward(Role):
    def __init__(self):
        super().__init__("Complete Forward",
            tier1=["Dribbling", "Finishing", "First Touch", "Heading", "Technique", "Anticipation", "Composure", "Off The Ball", "Acceleration", "Agility", "Strength"],
            tier2=["Long Shots", "Passing", "Decisions", "Team Work", "Vision", "Work Rate", "Balance", "Jumping Reach", "Pace", "Stamina"]
        )

class CompleteWingBack(Role):
    def __init__(self):
        super().__init__("Complete Wing Back",
            tier1=["Dribbling", "Crossing", "Technique", "Work Rate", "Team Work", "Off The Ball", "Acceleration", "Stamina"],
            tier2=["First Touch", "Marking", "Passing", "Tackling", "Decisions", "Anticipation", "Flair", "Positioning", "Balance", "Agility", "Pace"]
        )

class Poacher(Role):
    def __init__(self):
        super().__init__("Poacher",
            tier1=["Finishing", "Heading", "Anticipation", "Composure", "Concentration", "Off The Ball", "Acceleration"],
            tier2=["First Touch", "Technique", "Decisions", "Agility", "Balance"]
        )

class TargetForward(Role):
    def __init__(self):
        super().__init__("Target Forward",
            tier1=["Finishing", "Heading", "Aggression", "Bravery", "Composure", "Off The Ball", "Balance", "Jumping Reach", "Strength"],
            tier2=["First Touch", "Anticipation", "Decisions", "Team Work"]
        )

class AdvancedForward(Role):
    def __init__(self):
        super().__init__("Advanced Forward",
            tier1=["Dribbling", "Finishing", "First Touch", "Technique", "Composure", "Off The Ball", "Acceleration"],
            tier2=["Passing", "Anticipation", "Decisions", "Work Rate", "Agility", "Balance", "Pace", "Stamina"]
        )

class FreeRole(Role):
    def __init__(self):
        super().__init__("Free Role",
            tier1=["Dribbling", "First Touch", "Long Shots", "Passing", "Technique", "Composure", "Flair", "Off The Ball", "Vision"],
            tier2=["Crossing", "Finishing", "Anticipation", "Decisions", "Acceleration", "Agility"]
        )

class SecondStriker(Role):
    def __init__(self):
        super().__init__("Second Striker",
            tier1=["Finishing", "First Touch", "Anticipation", "Composure", "Off The Ball", "Acceleration"],
            tier2=["Dribbling", "Long Shots", "Passing", "Technique", "Concentration", "Decisions", "Work Rate", "Agility", "Pace", "Stamina"]
        )

class PressingForward(Role):
    def __init__(self):
        super().__init__("Pressing Forward",
            tier1=["Aggression", "Anticipation", "Bravery", "Off The Ball", "Team Work", "Work Rate", "Acceleration", "Pace", "Stamina"],
            tier2=["Finishing", "First Touch", "Composure", "Concentration", "Decisions", "Agility", "Balance", "Strength"]
        )

# -----------------------------
# CREATORS / PLAYMAKERS / MIDFIELD
# -----------------------------
class AttackingMidfielder(Role):
    def __init__(self):
        super().__init__("Attacking Midfielder",
            tier1=["First Touch", "Long Shots", "Passing", "Technique", "Composure", "Flair", "Off The Ball"],
            tier2=["Crossing", "Dribbling", "Finishing", "Anticipation", "Decisions", "Vision", "Acceleration", "Agility"]
        )

class ChannelMidfielder(Role):
    def __init__(self):
        super().__init__("Channel Midfielder",
            tier1=["Crossing", "First Touch", "Passing", "Technique", "Composure", "Off The Ball", "Work Rate", "Acceleration"],
            tier2=["Dribbling", "Long Shots", "Anticipation", "Decisions", "Flair", "Vision", "Agility", "Pace", "Stamina"]
        )

class AdvancedPlaymaker(Role):
    def __init__(self):
        super().__init__("Advanced Playmaker",
            tier1=["First Touch", "Passing", "Technique", "Composure", "Decisions", "Off The Ball", "Team Work", "Vision"],
            tier2=["Crossing", "Dribbling", "Anticipation", "Flair", "Acceleration", "Agility"]
        )

class MidfieldPlaymaker(Role):
    def __init__(self):
        super().__init__("Midfield Playmaker",
            tier1=["First Touch", "Passing", "Technique", "Composure", "Decisions", "Off The Ball", "Team Work", "Vision"],
            tier2=["Dribbling", "Tackling", "Anticipation", "Flair", "Positioning", "Work Rate", "Agility", "Stamina"]
        )


class Regista(Role):
    def __init__(self):
        super().__init__("Regista",
            tier1=["First Touch", "Passing", "Technique", "Composure", "Decisions", "Flair", "Off The Ball", "Team Work", "Vision"],
            tier2=["Dribbling", "Long Shots", "Anticipation", "Balance"]
        )
    
class WideCentralMidfielder(Role):
    def __init__(self):
        super().__init__("Wide Central Midfielder",
            tier1=["First Touch", "Passing", "Tackling", "Decisions", "Team Work"],
            tier2=["Crossing", "Dribbling", "Technique", "Anticipation", "Composure", "Concentration", "Off The Ball", "Positioning", "Vision", "Work Rate", "Agility", "Stamina"]
        )

class CentralMidfielder(Role):
    def __init__(self):
        super().__init__("Central Midfielder",
            tier1=["First Touch", "Passing", "Tackling", "Decisions", "Team Work"],
            tier2=["Technique", "Anticipation", "Composure", "Concentration", "Off The Ball", "Positioning", "Vision", "Work Rate", "Stamina"]
        )

class DeepLyingPlaymaker(Role):
    def __init__(self):
        super().__init__("Deep Lying Playmaker",
            tier1=["First Touch", "Passing", "Technique", "Composure", "Decisions", "Team Work", "Vision"],
            tier2=["Marking", "Tackling", "Anticipation", "Concentration", "Off The Ball", "Positioning", "Work Rate", "Balance", "Stamina"]
        )

class BoxToBoxPlaymaker(Role):
    def __init__(self):
        super().__init__("Box To Box Playmaker",
            tier1=["First Touch", "Passing", "Technique", "Composure", "Decisions", "Off The Ball", "Team Work", "Vision", "Work Rate", "Stamina"],
            tier2=["Dribbling", "Long Shots", "Marking", "Tackling", "Anticipation", "Positioning", "Acceleration", "Agility", "Balance", "Pace"]
        )

class RoamingPlaymaker(Role):
    def __init__(self):
        super().__init__("Roaming Playmaker",
            tier1=["First Touch", "Passing", "Technique", "Anticipation", "Composure", "Decisions", "Off The Ball", "Team Work", "Vision", "Work Rate", "Acceleration", "Stamina"],
            tier2=["Dribbling", "Long Shots", "Concentration", "Positioning", "Agility", "Balance", "Pace"]
        )


class Mezzala(Role):
    def __init__(self):
        super().__init__("Mezzala",
            tier1=["Passing", "Technique", "Decisions", "Off The Ball", "Work Rate", "Acceleration"],
            tier2=["Dribbling", "First Touch", "Long Shots", "Tackling", "Anticipation", "Composure", "Vision", "Balance", "Stamina"]
        )

class Anchor(Role):
    def __init__(self):
        super().__init__("Anchor",
            tier1=["Marking", "Tackling", "Anticipation", "Concentration", "Decisions", "Positioning"],
            tier2=["Composure", "Team Work", "Strength"]
        )

class BoxToBoxMidfielder(Role):
    def __init__(self):
        super().__init__("Box To Box Midfielder",
            tier1=["Passing", "Tackling", "Off The Ball", "Team Work", "Work Rate", "Stamina"],
            tier2=["Dribbling", "Finishing", "First Touch", "Long Shots", "Technique", "Aggression", "Anticipation", "Composure", "Decisions", "Positioning", "Acceleration", "Balance", "Pace", "Strength"]
        )

class DefensiveMidfielder(Role):
    def __init__(self):
        # user gave two DM variants; create standard DM (first) and one with heading as DM_H
        super().__init__("Defensive Midfielder",
            tier1=["Tackling", "Anticipation", "Concentration", "Positioning", "Team Work"],
            tier2=["First Touch", "Marking", "Passing", "Aggression", "Composure", "Decisions", "Work Rate", "Stamina", "Strength"]
        )

class BallWinningMidfielder(Role):
    def __init__(self):
        # user gave two DM variants; create standard DM (first) and one with heading as DM_H
        super().__init__("Ball Winning Midfielder",
            tier1=["Tackling", "Agression", "Anticipation", "Team Work", "Work Rate", "Stamina"],
            tier2=["Marking", "Bravery", "Concentration", "Positioning", "Agility", "Pace", "Strength"]
        )

# -----------------------------
# CENTRE BACK VARIANTS
# -----------------------------
class BallPlayingCentreBack(Role):
    def __init__(self):
        super().__init__("Ball Playing Centre Back",
            tier1=["Heading", "Marking", "Passing", "Tackling", "Anticipation", "Composure", "Positioning", "Jumping Reach", "Strength"],
            tier2=["First Touch", "Technique", "Aggression", "Bravery", "Concentration", "Decisions", "Vision", "Pace"]
        )

class BallPlayingDefender(Role):
    def __init__(self):
        super().__init__("Ball Playing Defender",
            tier1=["Heading", "Marking", "Passing", "Tackling", "Anticipation", "Composure", "Positioning", "Jumping Reach", "Strength"],
            tier2=["First Touch", "Technique", "Aggression", "Bravery", "Concentration", "Decisions", "Vision", "Pace"]
        )

class AdvancedCentreBack(Role):
    def __init__(self):
        super().__init__("Advanced Centre Back",
            tier1=["Technique", "Heading", "Marking", "Passing", "Tackling", "Anticipation", "Composure", "Positioning", "Jumping Reach", "Strength", "Team Work"],
            tier2=["First Touch", "Dribbling", "Aggression", "Bravery", "Concentration", "Decisions", "Vision", "Pace", "Stamina"]
        )

class NoNonsenseCentreBack(Role):
    def __init__(self):
        super().__init__("No Nonsense Centre Back",
            tier1=["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
            tier2=["Aggression", "Bravery", "Concentration", "Pace"]
        )

class CentreBack(Role):
    def __init__(self):
        super().__init__("Centre Back",
            tier1=["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
            tier2=["Aggression", "Bravery", "Concentration", "Pace", "Composure", "Decisions"]
        )

class CentralDefender(Role):
    def __init__(self):
        super().__init__("Central Defender",
            tier1=["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
            tier2=["Aggression", "Bravery", "Concentration", "Pace", "Composure", "Decisions"]
        )

class WideCentreBack(Role):
    def __init__(self):
        super().__init__("Wide Centre Back",
            tier1=["Heading", "Marking", "Tackling", "Anticipation", "Positioning", "Jumping Reach", "Strength"],
            tier2=["Aggression", "Bravery", "Concentration", "Pace", "Composure", "Decisions", "Dribbling", "Work Rate", "Acceleration", "Agility", "Stamina"]
        )

class OverlappingCentreBack(Role):
    def __init__(self):
        super().__init__("Overlapping Centre Back",
            tier1=["Crossing", "Heading", "Marking", "Tackling", "Anticipation", "Work Rate", "Jumping Reach", "Pace", "Stamina", "Strength"],
            tier2=["Dribbling", "Technique", "Aggression", "Bravery", "Composure", "Concentration", "Decisions", "Off The Ball", "Positioning", "Acceleration", "Agility"]
        )

class Carrilero(Role):
    def __init__(self):
        super().__init__("Carrilero",
            tier1=["First Touch", "Passing", "Tackling", "Decisions", "Positioning", "Team Work", "Stamina"],
            tier2=["Technique", "Antecipation", "Composure", "Concentration", "Off The Ball", "Vision", "Work Rate", "Agility"]
        )

class WideTargetForward(Role):
    def __init__(self):
        super().__init__("Wide Target Forward",
            tier1=["Heading", "Bravery", "Team Work", "Jumping Reach", "Strength"],
            tier2=["Crossing", "First Touch", "Anticipation", "Off The Ball", "Work Rate", "Balance", "Stamina"]
        )

class ShadowStriker(Role):
    def __init__(self):
        super().__init__("Shadow Striker",
            tier1=["Dribbling", "Finishing", "First Touch", "Anticipation", "Composure", "Off The Ball", "Acceleration"],
            tier2=["Passing", "Technique", "Concentration", "Decisions", "Work Rate", "Agility", "Balance", "Pace", "Stamina"]
        )

# -----------------------------
# UTIL: build list of roles easily
# -----------------------------
def build_all_roles():
    """Return a list of instantiated role objects (all classes above)."""
    return [
        SweeperKeeper(), Goalkeeper(), WingBack(), PlaymakingWingBack(), InvertedWingBack(), InsideWingBack(), FullBack(), InsideFullBack(), InvertedFullBack(),
        Winger(), WideMidfielder(), InsideWinger(), PlaymakingWinger(), WideForward(),
        InsideForward(), FalseNine(), ChannelForward(), DeepLyingForward(), CentreForward(),
        Poacher(), TargetForward(), FreeRole(), SecondStriker(), Regista(), SegundoVolante(),
        AttackingMidfielder(), ChannelMidfielder(), AdvancedPlaymaker(), MidfieldPlaymaker(), WideTargetForward(),
        WideCentralMidfielder(), CentralMidfielder(), DeepLyingPlaymaker(), BoxToBoxPlaymaker(), ShadowStriker(),
        BoxToBoxMidfielder(), DefensiveMidfielder(), BallWinningMidfielder(), PressingForward(),
        BallPlayingCentreBack(), AdvancedCentreBack(), NoNonsenseCentreBack(), CentreBack(), CompleteWingBack(),
        WideCentreBack(), OverlappingCentreBack(), Carrilero(), CentralDefender(), BallPlayingDefender(), InvertedWinger(), Mezzala(), CompleteForward(), RoamingPlaymaker(), Anchor(), AdvancedForward()
    ]
