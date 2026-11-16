#!/bin/sh
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad; P=$D/p26; F=$P/p26_freeze1.txt
{ echo "# P26 freeze $(date -u +%FT%TZ)"; for f in $P/Protocole_P26_calendrier_de_concentration_v0_1.md $P/p26_calib.json $P/p26_params.json $P/p26_tests_results.json $P/p26_pilot.json $P/code/p26.py $P/code/p26_calib.py $P/code/p26_select.py $P/code/p26_pilot.py $P/code/p26_run.py $P/code/p26_an.py $P/code/p26_tests.py $P/code/p26_dryrun_an.py $D/p24/code/p24.py $D/p25b/p25b_final_analysis.json $D/p25b/code/p25b.py; do sha256sum $f; done; } > $F
python3 -c "
import sys; sys.path.insert(0,'$D/p5'); import run_p1m as R; sys.exit(0 if R.verify_freeze('$F') else 1)" && echo "freeze OK"
