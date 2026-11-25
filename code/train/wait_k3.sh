#!/bin/sh
# Wait for kernel k3 to finish, then download its outputs to logs/_k3.
cd /c/SIC || exit 1
export KAGGLE_API_TOKEN=$(grep -o 'KGAT_[0-9a-f]*' apikey_kaggle.txt | head -1)
while true; do
  s=$(kaggle kernels status thinhlai/sic-dr-run-k3 2>&1 | tail -n 1)
  case "$s" in
    *COMPLETE*) break ;;
    *ERROR*|*CANCEL*) echo "k3 ended badly: $s" > logs/_k3_status.txt; exit 1 ;;
  esac
  sleep 240
done
mkdir -p logs/_k3
kaggle kernels output thinhlai/sic-dr-run-k3 -p logs/_k3 > logs/_k3_download.out 2>&1
echo "k3 downloaded $(date +%H:%M)" > logs/_k3_status.txt
