#!/bin/sh
# Wait for kernel e15 to finish and download its outputs to logs/_e15.
cd /c/SIC || exit 1
export KAGGLE_API_TOKEN=$(grep -o 'KGAT_[0-9a-f]*' apikey_kaggle.txt | head -1)
while true; do
  s=$(kaggle kernels status thinhlai/sic-dr-run-e15 2>&1 | tail -n 1 | grep -o 'KernelWorkerStatus\.[A-Z_]*')
  case "$s" in
    *COMPLETE*|*ERROR*|*CANCEL*)
      mkdir -p logs/_e15
      kaggle kernels output thinhlai/sic-dr-run-e15 -p logs/_e15 > logs/_e15_download.out 2>&1
      echo "$(date +%H:%M) e15 downloaded ($s)" > logs/_e15_status.txt
      exit 0 ;;
  esac
  sleep 90
done
