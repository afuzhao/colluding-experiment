#!/bin/bash
cd .
until python3 -c "import json,sys; sys.exit(0 if json.load(open('busting_status.json'))['state'] != 'running' else 1)"; do sleep 15; done
caffeinate -i python3 extensions.py
