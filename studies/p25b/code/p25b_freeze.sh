#!/bin/sh
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad; P=$D/p25b; F=$P/p25b_freeze1.txt
{ echo "# P25b freeze $(date -u +%FT%TZ)"; for f in $P/Protocole_P25b_geographies_de_benchmark_v0_1.md $P/files_sha256.txt $P/p25b_calib.json $P/p25b_params.json $P/p25b_tests_results.json $P/p25b_pilot.json $P/code/p25b.py $P/code/p25b_calib.py $P/code/p25b_select.py $P/code/p25b_pilot.py $P/code/p25b_run.py $P/code/p25b_an.py $P/code/p25b_tests.py $P/code/p25b_dryrun_an.py $D/p24/code/p24.py $D/p25/p25_final_analysis.json; do sha256sum $f; done; } > $F
python3 -c "
import sys; sys.path.insert(0,'$D/p5'); import run_p1m as R; sys.exit(0 if R.verify_freeze('$F') else 1)" && echo "freeze OK"
