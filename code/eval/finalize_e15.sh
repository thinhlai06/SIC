#!/bin/sh
# Final analysis of the 15-epoch runs. Run after logs/_e15 contains the kernel outputs.
# Usage: sh code/eval/finalize_e15.sh
cd /c/SIC || exit 1
D=logs/_e15
OUT=results/main_e15
mkdir -p $OUT
ls $D | head -40
cat > $D/runs.json <<EOF
{"B1": ["b1_s0_e15", "b1_s1_e15"], "B2": ["b2_s0_e15"], "M1": ["m1_s0_e15"]}
EOF
python code/eval/analyze.py --npz-dir $D --runs $D/runs.json --out $OUT 2>&1 | tail -n 8
python code/eval/ordinal_variant.py --npz-dir $D --val-dir $D --runs $D/runs.json --manifest logs/manifest.csv --out $OUT 2>&1 | tail -n 40
python code/eval/curves_all.py $D $OUT/t01_curves_all.png
python code/eval/gradcam_examples.py --npz-dir $D --ddr-tar logs/_pkg/ddr_test.tar --manifest logs/manifest.csv \
  --ckpt M1=$D/m1_s0_e15_best.pt --ckpt B2=$D/b2_s0_e15_best.pt --runs M1=m1_s0_e15,B2=b2_s0_e15 --out $OUT 2>&1 | tail -n 3
python code/eval/to_latex_figs.py $OUT
