"conda activate fm24" -- this conda env is able to run the optimization script

New exports are ingested automatically by run_team.py and the newest one is parsed (the run prints `export: <label>`). `--no-ingest` / `--no-parse` skip it; `--date <label>` picks an older one.

"python run_team.py corinthians --by-formation --config relogio.json --inf Inj Unr Ine Int Sus" -- removes every player whose Inf status is one of these codes (case-insensitive). Loa, Wnt, Wtg, Rst, FtT and Fgn are informational: never exclude them

"python run_team.py corinthians --date <label> --by-formation --config callup.json -r 'player one' 'player two'" -- uses that export and creates a team without these players. Names are matched without accents/case, full or one whole word; unknown or ambiguous names stop the run

"python run_team.py corinthians --by-formation --config relogio.json --inf Inj Unr Ine Int Sus --load heavy very-heavy --keep-gk --keep Gio --sample 0.5" -- also removes half (random, seed printed; --seed N repeats it) of the heavy/very heavy match load players, except goalkeepers and Gio. "--top-load 4 --keep-gk" instead removes the 4 first-team players with most minutes

"python run_team.py corinthians --by-formation --config relogio.json --set ip_weight=0.7 age_penalty=0.3 --mult 'Last 5 Games=0.1' 'Flair=0'" -- one-off config tweaks, in memory only (0 removes a multiplier; --no-mult = attributes only). Prints an `overrides:` line

Every run writes teams/<config>/run.json (export, effective config, exclusions with reasons, seed, command) and removes stale team_K files.

"game_data/roles.json" -- valid role names for configs: use the "harness" name with spaces turned into underscores (role / role_oop) and check "positions" for the slot. For out-of-possession roles the slot is the one in the out-of-possession shape.
