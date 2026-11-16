#!/bin/sh
# P19 driver: wait calibration -> select gamma_m -> freeze -> verify -> wait for P18 part B end -> run P19 main. Stops on any failure.
D=/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad; P=$D/p19
until [ -f $P/p19_calib.json ] || ! pgrep -f p19_calib.py >/dev/null; do sleep 30; done
[ -f $P/p19_calib.json ] || { echo "calibration failed: no p19_calib.json"; exit 1; }
python3 $P/code/p19_select.py > $P/p19_select_stdout.txt 2>&1 || { echo "select failed"; exit 1; }
F=$P/p19_freeze1.txt; { echo "# P19 freeze $(date -u +%FT%TZ)"; for f in $P/Protocole_P19_v0_3.md $P/p19_calib.json $P/p19_gamma.json $P/p19_manifest.json $P/p19_tests_results.json $P/code/p19.py $P/code/p19_calib.py $P/code/p19_select.py $P/code/p19_run.py $P/code/p19_an.py $P/code/p19_tests.py $D/p15/p15_params.json; do sha256sum $f; done; } > $F
python3 -c "
import sys; sys.path.insert(0,'$D/p5'); import run_p1m as R; sys.exit(0 if R.verify_freeze('$F') else 1)" || { echo "freeze verification failed"; exit 1; }
echo "freeze OK $(date -u +%FT%TZ)"
MISS=0
until grep -q "ALL DONE B" $D/p18/p18_B_stdout.txt 2>/dev/null; do
  if pgrep -f p18_run >/dev/null; then MISS=0; else MISS=$((MISS+1)); fi
  [ $MISS -ge 3 ] && { echo "P18 not running and part B not finished: P19 not launched"; exit 1; }
  sleep 60
done
echo "P18 done, launching P19 $(date -u +%FT%TZ)"
python3 $P/code/p19_run.py $P/runs/main $F
