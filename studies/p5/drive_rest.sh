#!/bin/bash
cd "$(dirname "$(readlink -f "$0")")"; S=$PWD; R=$S/runs
step() { until "$@"; do :; done; }
# P5-A
until grep -q "ALL DONE" $R/pA.log 2>/dev/null; do P5_MAXSEC=6000 python3 p5_run.py pA $R/pA >> $R/pA.log 2>&1 || { echo "ERROR pA"; exit 1; }; done
python3 an_p5_pA.py $R/pA $S/p5_strategy.json > $R/pA_analysis.txt 2>&1 || { echo "ERROR pA analysis"; exit 1; }
echo "STRATEGY $(python3 -c "import json;print(json.load(open('$S/p5_strategy.json'))['strategy'])")"
# C3 calibration
until [ -f $R/calib/calib_selected_C3.json ]; do P5_MAXSEC=6000 python3 p5_run.py calib C3 $R/calib >> $R/calib_C3.log 2>&1 || { echo "ERROR C3"; exit 1; }; done
echo "C3_CALIBRATED"
# pilot
until grep -q "ALL DONE" $R/pilot.log 2>/dev/null; do P5_MAXSEC=6000 python3 p5_run.py pilot $R/pilot >> $R/pilot.log 2>&1 || { echo "ERROR pilot"; exit 1; }; done
python3 an_p5_pilot.py $R/pilot $S/p5_n.json > $R/pilot_analysis.txt 2>&1 || { echo "ERROR pilot analysis"; exit 1; }
echo "N $(python3 -c "import json;d=json.load(open('$S/p5_n.json'));print(d['n'],d['under_powered'])")"
# freeze
{ echo "# P5 freeze $(date -u +%FT%TZ) (protocol v0.3)"; cat $S/p5_codefreeze.txt | grep -v '^#'; for f in p5_tuned.json p5_strategy.json p5_n.json; do sha256sum $S/$f; done; for f in $R/calib/calib_selected_*.json; do sha256sum $f; done; sha256sum $R/pilot_analysis.txt $R/pA_analysis.txt; } > $S/p5_freeze.txt
python3 -c "import run_p1m as R;assert R.verify_freeze('$S/p5_freeze.txt')" || { echo "ERROR freeze"; exit 1; }
echo "FROZEN"
# P5-B and P5-C
until grep -q "ALL DONE" $R/conf.log 2>/dev/null; do P5_MAXSEC=6000 python3 p5_run.py conf $R/conf $S/p5_freeze.txt >> $R/conf.log 2>&1 || { echo "ERROR conf"; exit 1; }; done
echo "CONF_DONE"
until grep -q "ALL DONE" $R/ablC.log 2>/dev/null; do P5_MAXSEC=6000 python3 p5_run.py ablC $R/ablC $S/p5_freeze.txt >> $R/ablC.log 2>&1 || { echo "ERROR ablC"; exit 1; }; done
echo "ALL_RUNS_DONE"
