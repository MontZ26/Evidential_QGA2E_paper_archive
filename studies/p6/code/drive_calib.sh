#!/bin/bash
S=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6; cd $S/code; R=$S/runs
for pair in "C2|on" "C3|on" "C2|off" "C3|off"; do
  tag=${pair/|/_}
  until [ -f $R/calib/calib_selected_$tag.json ]; do P6_MAXSEC=3000 python3 p6_run.py calib "$pair" $R/calib $S/p6_freeze1.txt >> $R/calib_$tag.log 2>&1 || { echo "ERROR $pair"; exit 1; }; done
  echo "DONE $pair"
done
echo CALIB_ALL_DONE
