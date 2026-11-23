"conda activate fm24" -- this conda env is able to run the optimization script

"python run_team.py corinthians --date sep2023 --by-formation --config callup.json -r 'player one' 'player two'" -- this for instance takes the sep2023 html from data/corinthians, uses configs/corinthians/callup.json and creates a team removing these players


"game_data/roles.json" -- valid role names for configs: use the "harness" name with spaces turned into underscores (role / role_oop) and check "positions" for the slot. For out-of-possession roles the slot is the one in the out-of-possession shape.
