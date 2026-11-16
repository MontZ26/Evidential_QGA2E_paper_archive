#!/bin/sh
# P23 freeze file (hashes) + verification. Run after calibration, selection, pilot, tests.
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad; P=$D/p23; F=$P/p23_freeze1.txt
{ echo "# P23 freeze $(date -u +%FT%TZ)"; for f in $P/Protocole_P23_v1_0.md $P/p23_calib.json $P/p23_params.json $P/p23_tests_results.json $P/p23_seedcheck.json $P/p23_pilot.json $P/code/p23.py $P/code/p23_calib.py $P/code/p23_select.py $P/code/p23_pilot.py $P/code/p23_run.py $P/code/p23_an.py $P/code/p23_tests.py $D/p15/p15_params.json; do sha256sum $f; done; } > $F
python3 -c "
import sys; sys.path.insert(0,'$D/p5'); import run_p1m as R; sys.exit(0 if R.verify_freeze('$F') else 1)" && echo "freeze OK"
