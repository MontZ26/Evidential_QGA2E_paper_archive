#!/bin/bash
S=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7; cd $S/code; R=$S/runs; mkdir -p $R/calib
until [ -f $R/calib/calib_selected.json ]; do P7_MAXSEC=3000 python3 p7_run.py calib $R/calib $S/p7_freeze1.txt >> $R/calib.log 2>&1 || { echo "ERROR calib"; exit 1; }; done
echo CALIB_DONE
