#!/bin/bash
cd "$(dirname "$(readlink -f "$0")")"; S=$PWD
for L in C2a C2b C2c C0b NSGA2 MOEAD; do
  until [ -f $S/runs/calib/calib_selected_$L.json ]; do P5_MAXSEC=6000 python3 p5_run.py calib $L $S/runs/calib || { echo "ERROR on $L"; exit 1; }; done
done
echo CALIB1_DONE
