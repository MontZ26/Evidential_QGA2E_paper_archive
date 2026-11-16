#!/bin/bash
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad; cd $D/p22/code
set -e
python3 p22_calib.py > $D/p22/p22_calib_stdout.txt 2>&1
python3 p22_select.py > $D/p22/p22_select_stdout.txt 2>&1
{ echo "# P22 freeze $(date -u +%FT%TZ)"; for f in $D/p22/Protocole_P22_v1_0.md $D/p22/p22_calib.json $D/p22/p22_gamma.json $D/p22/p22_tests_results.json $D/p22/code/p22.py $D/p22/code/p22_tests.py $D/p22/code/p22_calib.py $D/p22/code/p22_select.py $D/p22/code/p22_run.py $D/p22/code/p22_an.py $D/p14/p14_params.json $D/p14/code/p14.py; do sha256sum $f; done; } > $D/p22/p22_freeze1.txt
python3 p22_run.py $D/p22/runs/main $D/p22/p22_freeze1.txt >> $D/p22/p22_run_stdout.txt 2>&1
echo "ALL DONE" >> $D/p22/p22_run_stdout.txt
