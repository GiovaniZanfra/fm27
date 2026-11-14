import pickle
import random
import itertools

# Fixed values (not swept)
LAST_5_GAMES = 0.5
TRN_RAT = 0.0
ARABIC_PENALTY = 0.0

# Parameter grids
age_penalties = [round(x * 0.1, 1) for x in range(1, 6)]      # 0.1, 0.2, 0.3, 0.4, 0.5
age_thresholds = list(range(29, 35))                             # 29, 30, 31, 32, 33, 34
transfer_values = [round(x * 0.2, 1) for x in range(1, 6)]     # 0.2, 0.4, 0.6, 0.8, 1.0
av_rats = [round(x * 0.2, 1) for x in range(0, 6)]             # 0.0, 0.2, 0.4, 0.6, 0.8, 1.0

all_combinations = list(itertools.product(age_penalties, age_thresholds, transfer_values, av_rats))
print(f"Full grid size: {len(all_combinations)} combinations")

random.seed(42)
sampled = random.sample(all_combinations, 20)

grid = []
for age_pen, age_thr, tv, av_rat in sampled:
    grid.append({
        "age_penalty": age_pen,
        "age_threshold": age_thr,
        "arabic_penalty": ARABIC_PENALTY,
        "multipliers": {
            "Transfer Value": tv,
            "Av Rat": av_rat,
            "Last 5 Games": LAST_5_GAMES,
            "Trn Rat": TRN_RAT,
        },
    })

output_path = "grid_search_params.pkl"
with open(output_path, "wb") as f:
    pickle.dump(grid, f)

print(f"Saved {len(grid)} combinations to {output_path}")
print("\nSample combinations:")
for i, combo in enumerate(grid):
    print(f"  [{i:02d}] age_pen={combo['age_penalty']} thr={combo['age_threshold']} "
          f"TV={combo['multipliers']['Transfer Value']} AvRat={combo['multipliers']['Av Rat']}")
