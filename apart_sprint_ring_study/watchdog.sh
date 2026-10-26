#!/bin/bash
# Stop every paid collector if total counted spend passes the limit.
cd /Users/aakritigarodia/Desktop/Projects/apart-sprint
LIMIT=${1:-46.5}
while true; do
  TOTAL=$(python3 spend.py | tail -1 | awk '{print $2}')
  if python3 -c "import sys; sys.exit(0 if float('$TOTAL') > float('$LIMIT') else 1)"; then
    pkill -f run_pairs.py; pkill -f run_v4.py; pkill -f run_v5.py; pkill -f run_v6.py; pkill -f run_v3_study.py; pkill -f run_grid
    echo "$(date) STOPPED all collectors at total $TOTAL (limit $LIMIT)" >> OPERATIONS_LOG.md
    exit 0
  fi
  sleep 20
done
