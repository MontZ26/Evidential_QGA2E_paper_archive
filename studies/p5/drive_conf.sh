#!/bin/bash
cd "$(dirname "$(readlink -f "$0")")"; S=$PWD; R=$S/runs
rm -f $R/conf.log $R/ablC.log
until grep -q "ALL DONE" $R/conf.log 2>/dev/null; do P5_MAXSEC=6000 python3 p5_run.py conf $R/conf $S/p5_freeze.txt >> $R/conf.log 2>&1 || { echo "ERROR conf"; exit 1; }; done
echo "CONF_DONE"
until grep -q "ALL DONE" $R/ablC.log 2>/dev/null; do P5_MAXSEC=6000 python3 p5_run.py ablC $R/ablC $S/p5_freeze.txt >> $R/ablC.log 2>&1 || { echo "ERROR ablC"; exit 1; }; done
echo "ALL_RUNS_DONE"
