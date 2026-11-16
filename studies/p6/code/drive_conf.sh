#!/bin/bash
S=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6; cd $S/code; R=$S/runs
until grep -q "ALL DONE" $R/conf.log 2>/dev/null; do P6_MAXSEC=3000 python3 p6_run.py conf $R/conf $S/p6_freeze3.txt >> $R/conf.log 2>&1 || { echo "ERROR conf"; exit 1; }; done
echo CONF_DONE
