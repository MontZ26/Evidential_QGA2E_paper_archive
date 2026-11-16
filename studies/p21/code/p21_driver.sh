#!/bin/bash
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p21
cd $D/code
python3 p21_run.py A $D/runs/A $D/p21_freeze1.txt >> $D/p21_run_stdout.txt 2>&1
python3 p21_run.py B $D/runs/B $D/p21_freeze1.txt >> $D/p21_run_stdout.txt 2>&1
echo "ALL DONE" >> $D/p21_run_stdout.txt
