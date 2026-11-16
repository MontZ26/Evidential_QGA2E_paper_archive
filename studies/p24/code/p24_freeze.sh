#!/bin/sh
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad; P=$D/p24; F=$P/p24_freeze1.txt
{ echo "# P24 freeze $(date -u +%FT%TZ)"; for f in $P/Protocole_P24_v0_2_candidat.md $P/Mise_en_oeuvre_P24_v0_2.md $P/p24_calib.json $P/p24_params.json $P/p24_tests_results.json $P/p24_seedcheck.json $P/p24_pilot.json $P/code/p24.py $P/code/p24_calib.py $P/code/p24_select.py $P/code/p24_pilot.py $P/code/p24_run.py $P/code/p24_an.py $P/code/p24_tests.py $P/code/p24_dryrun_an.py $D/p23/p23_params.json $D/p23/p23_final_analysis.json $D/p15/p15_params.json; do sha256sum $f; done; } > $F
python3 -c "
import sys; sys.path.insert(0,'$D/p5'); import run_p1m as R; sys.exit(0 if R.verify_freeze('$F') else 1)" && echo "freeze OK"
