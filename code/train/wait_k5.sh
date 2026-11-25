#!/bin/sh
# Report status changes of kernel k5; on a terminal state download outputs to logs/_k5.
cd /c/SIC || exit 1
export KAGGLE_API_TOKEN=$(grep -o 'KGAT_[0-9a-f]*' apikey_kaggle.txt | head -1)
prev=""
while true; do
  s=$(kaggle kernels status thinhlai/sic-dr-run-k5 2>&1 | tail -n 1 | grep -o 'KernelWorkerStatus\.[A-Z_]*')
  if [ "$s" != "$prev" ] && [ -n "$s" ]; then echo "$(date +%H:%M) k5 $s"; prev="$s"; fi
  case "$s" in
    *COMPLETE*|*ERROR*|*CANCEL*)
      mkdir -p logs/_k5
      kaggle kernels output thinhlai/sic-dr-run-k5 -p logs/_k5 > logs/_k5_download.out 2>&1
      echo "$(date +%H:%M) k5 downloaded ($s)"
      exit 0 ;;
  esac
  sleep 60
done
