#!/bin/bash
S=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7; cd $S/code; R=$S/runs; mkdir -p $R/pilot
until grep -q "ALL DONE" $R/pilot.log 2>/dev/null; do P7_MAXSEC=3000 python3 p7_run2.py pilot $R/pilot $S/p7_freeze2.txt >> $R/pilot.log 2>&1 || { echo "ERROR pilot"; exit 1; }; done
python3 p7_an.py pilot $R/pilot $R/sizing >> $R/sizing.log 2>&1 && echo PILOT_SIZING_DONE || echo ERROR sizing
