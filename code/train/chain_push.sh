#!/bin/sh
# Sequential launcher: Kaggle allows only one of our 2-GPU batch sessions at a time.
# Usage: sh chain_push.sh k1 k2 k3   (k1 is assumed already pushed; waits for it, then pushes k2, waits, pushes k3 ...)
cd "$(dirname "$0")/../.." || exit 1
export KAGGLE_API_TOKEN=$(grep -o 'KGAT_[0-9a-f]*' apikey_kaggle.txt | head -1)
status() { kaggle kernels status "thinhlai/sic-dr-run-$1" 2>&1 | tail -1 | grep -o 'KernelWorkerStatus\.[A-Z]*'; }
wait_done() {
  while true; do
    s=$(status "$1")
    case "$s" in *COMPLETE*|*ERROR*|*CANCEL*) echo "$(date +%H:%M) $1 finished: $s"; return;; esac
    sleep 30
  done
}
prev="$1"; shift
for k in "$@"; do
  wait_done "$prev"
  tries=0
  until kaggle kernels push -p "code/runs/sic-dr-run-$k" --accelerator NvidiaTeslaT4 -t 9000 2>&1 | grep -q "successfully pushed"; do
    tries=$((tries + 1)); echo "$(date +%H:%M) push $k failed (try $tries), retrying in 60 s"; sleep 60
  done
  echo "$(date +%H:%M) pushed $k"
  prev="$k"
done
wait_done "$prev"
echo "CHAIN DONE"
