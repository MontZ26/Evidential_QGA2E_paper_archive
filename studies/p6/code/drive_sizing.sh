#!/bin/bash
S=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6; cd $S/code
python3 p6_pilot.py $S/runs/pilot $S/runs/sizing >> $S/runs/sizing.log 2>&1 && echo SIZING_DONE || echo SIZING_ERROR
