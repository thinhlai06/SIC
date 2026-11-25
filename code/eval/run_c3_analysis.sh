#!/bin/sh
# Analysis of the continued runs (5+3 epochs). Usage: sh run_c3_analysis.sh <runs-json-content-file> <out-dir>
# Expects the *_c3 outputs (npz, val logits, logs) already copied to logs/_npz and logs/.
cd /c/SIC || exit 1
RUNS="$1"; OUT="$2"
python code/eval/analyze.py --npz-dir logs/_npz --runs "$RUNS" --out "$OUT" 2>&1 | tail -n 8
python code/eval/ordinal_variant.py --npz-dir logs/_npz --val-dir logs/_npz --runs "$RUNS" --manifest logs/manifest.csv --out "$OUT" 2>&1 | tail -n 3
python code/eval/budget_table.py --five results/main_5ep --cont "$OUT" --out "$OUT" 2>&1 | tail -n 3
