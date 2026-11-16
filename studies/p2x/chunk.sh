#!/bin/bash
# runs the frozen runner for ~9-10 min and stops it only right after it finished a write (a new progress line is printed after json.dump)
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/revision; cd $D
python3 -c "import json;json.load(open('$D/p2s2_conf.json'))" && cp $D/p2s2_conf.json $D/p2s2_conf.json.bak
L=$D/p2s2_chunk.log; : > $L
python3 run_p2s2.py conf $D/p2s2_conf.json $D/p2s2_freeze.txt > $L 2>&1 &
PID=$!; T0=$(date +%s); N0=$(wc -l < $L)
while kill -0 $PID 2>/dev/null; do
  sleep 1; N1=$(wc -l < $L); E=$(( $(date +%s) - T0 ))
  if [ $E -ge 500 ] && [ "$N1" != "$N0" ]; then sleep 1; kill $PID; break; fi
  N0=$N1
done
sleep 2; pkill -f "^python3 run_p2s2"; cat $L >> $D/p2s2_conf_resume.log
python3 -c "import json;print(len(json.load(open('$D/p2s2_conf.json'))),'/600')" || { cp $D/p2s2_conf.json.bak $D/p2s2_conf.json; echo restored_from_backup; }
