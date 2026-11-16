#!/bin/sh
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad; P=$D/p25; F=$P/p25_freeze1.txt
{ echo "# P25 freeze $(date -u +%FT%TZ)"; for f in $P/Protocole_P25_validation_independante_v0_1.md $P/p25_calib.json $P/p25_params.json $P/p25_tests_results.json $P/p25_pilot.json $P/code/p25.py $P/code/p25_calib.py $P/code/p25_select.py $P/code/p25_pilot.py $P/code/p25_run.py $P/code/p25_an.py $P/code/p25_tests.py $P/code/p25_dryrun_an.py $D/p24/code/p24.py $D/p24/p24_final_analysis.json $D/p23/p23_final_analysis.json; do sha256sum $f; done; } > $F
python3 -c "
import sys; sys.path.insert(0,'$D/p5'); import run_p1m as R; sys.exit(0 if R.verify_freeze('$F') else 1)" && echo "freeze OK"
