#!/bin/sh
# Wait for kernel k5 to reach a terminal state, then push k6 (timeout 6 h, NOT 9000 s: the K3 cancellation came from -t 9000).
cd /c/SIC || exit 1
export KAGGLE_API_TOKEN=$(grep -o 'KGAT_[0-9a-f]*' apikey_kaggle.txt | head -1)
while true; do
  s=$(kaggle kernels status thinhlai/sic-dr-run-k5 2>&1 | tail -n 1 | grep -o 'KernelWorkerStatus\.[A-Z_]*')
  case "$s" in *COMPLETE*|*ERROR*|*CANCEL*) echo "$(date +%H:%M) k5 finished: $s"; break;; esac
  sleep 45
done
tries=0
until kaggle kernels push -p code/runs/sic-dr-run-k6 --accelerator NvidiaTeslaT4 -t 21600 2>&1 | grep -q "successfully pushed"; do
  tries=$((tries + 1)); echo "$(date +%H:%M) push k6 failed (try $tries)"; sleep 45
done
echo "$(date +%H:%M) pushed k6"
while true; do
  s=$(kaggle kernels status thinhlai/sic-dr-run-k6 2>&1 | tail -n 1 | grep -o 'KernelWorkerStatus\.[A-Z_]*')
  case "$s" in *COMPLETE*|*ERROR*|*CANCEL*)
    mkdir -p logs/_k6
    kaggle kernels output thinhlai/sic-dr-run-k6 -p logs/_k6 > logs/_k6_download.out 2>&1
    echo "$(date +%H:%M) k6 downloaded ($s)"; exit 0;; esac
  sleep 60
done
