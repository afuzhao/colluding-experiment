#!/bin/bash
# v17 part B: formation then branches for Claude Sonnet 5.5
cd "$(dirname "$0")"
M=anthropic/claude-sonnet-5.5
python3 run_v11.py son_form 1.6 main $M 3 PQ chat > v17_son_form.log 2>&1
python3 run_v15.py son15 0.8 main $M 5101,5202,5303 PQ placebo,fmsg > v17_son15.log 2>&1 &
python3 run_v16.py son16 0.9 main $M 5101,5202,5303 PQ outsider,act > v17_son16.log 2>&1 &
wait
