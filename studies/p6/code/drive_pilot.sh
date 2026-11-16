#!/bin/bash
S=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6; cd $S/code; R=$S/runs
until grep -q "ALL DONE" $R/pilot.log 2>/dev/null; do P6_MAXSEC=3000 python3 p6_run.py pilot $R/pilot $S/p6_freeze2.txt >> $R/pilot.log 2>&1 || { echo "ERROR pilot"; exit 1; }; done
echo PILOT_DONE
