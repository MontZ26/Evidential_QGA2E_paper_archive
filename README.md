# Evidential vs probabilistic target distributions in QGA2-E (home health care team assignment)

Companion repository of the manuscript *Evidential versus Probabilistic Target Distributions in a Quantum-Inspired Multiobjective Genetic Algorithm: The Case of Home Health Care Team Assignment* (Dr Montassar Zaghdoud, Manouba School of Engineering, Manouba University, Tunisia).

## Contents
- `paper/` : condensed manuscript (`Paper_v0_9_short.*`, 20 pages) and extended manuscript = Supplementary Material (`Paper_v0_9.*`, 36 pages), Markdown sources, build scripts and figures.
- `studies/pN/` : one folder per study (P2 to P26). Each holds the protocol and/or final report (`*.md`), the frozen parameters and freeze records (`*_params.json`, `*_freeze*.txt`), the code (`code/`), the pre-specified test results (`*_tests_results.json`) and the final analysis file (`*_final_analysis.json`).
- `Synthese_protocoles_P2_P22_v2.md` : summary of protocols P2 to P22.

## Language note
The protocols and final reports in `studies/` were written in French and are kept as the original, hash-linked records of each study. The manuscript (`paper/`) is the English account of all methods and results. English translations of any protocol or report are available on request from the corresponding author (montassar.zaghdoud@mse.uma.tn).

## What is not included
The raw per-run result files (several GB) are not stored here because of GitHub size limits. The final analysis files, which the manuscript tables are computed from, are included. Raw runs can be regenerated with the code and the seeds stated in each protocol.

## Reproducing a study
Each study folder lists its seeds in its protocol. Scripts were run in a Linux environment with Python 3 and NumPy; some scripts contain absolute paths of that environment, which must be adapted.

## Licence
Code: MIT. Text, data and analysis files: CC BY 4.0. See `LICENSE`.

## Citation
See `CITATION.cff`. A permanent DOI can be obtained by archiving a tagged release (e.g. through Zenodo) if the journal requires it.
