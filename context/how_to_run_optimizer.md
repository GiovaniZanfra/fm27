"conda activate fm24" -- this conda env is able to run the optimization script

"python run_team.py sporting --date sep2023 --by-formation --config callup.json -r 'player one' 'player two'" -- this for instance takes the sep2023 html from data/sporting, uses configs/sporting/callup.json and creates a team removing these players
