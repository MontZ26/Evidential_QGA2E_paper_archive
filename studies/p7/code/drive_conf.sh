#!/bin/bash
S=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7; cd $S/code; R=$S/runs; mkdir -p $R/conf
until grep -q "ALL DONE" $R/conf.log 2>/dev/null; do P7_MAXSEC=3000 python3 p7_run2.py conf $R/conf $S/p7_freeze4.txt >> $R/conf.log 2>&1 || { echo "ERROR conf"; exit 1; }; done
echo CONF_DONE
