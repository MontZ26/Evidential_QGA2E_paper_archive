#!/bin/sh
set -e
P=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p25b; cd $P/code
[ -f $P/p25b_calib.json ] || python3 p25b_calib.py > $P/calib_stdout.txt 2>&1
[ -f $P/p25b_params.json ] || python3 p25b_select.py > $P/select_stdout.txt 2>&1
[ -f $P/p25b_pilot.json ] || python3 p25b_pilot.py > $P/pilot_stdout.txt 2>&1
python3 p25b_dryrun_an.py > $P/dry_stdout.txt 2>&1
[ -f $P/p25b_freeze1.txt ] || sh p25b_freeze.sh > $P/freeze_stdout.txt 2>&1
python3 p25b_run.py $P/runs/main $P/p25b_freeze1.txt > $P/run_stdout.txt 2>&1
python3 p25b_an.py precheck $P/runs/main $P/p25b_freeze1.txt > $P/precheck_stdout.txt 2>&1
[ -f $P/p25b_final_analysis.json ] || python3 p25b_an.py final $P/runs/main $P/p25b_final_analysis.json $P/p25b_freeze1.txt > $P/final_stdout.txt 2>&1
echo CHAIN_DONE
