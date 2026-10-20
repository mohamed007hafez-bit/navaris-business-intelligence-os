#!/bin/bash
set -euo pipefail
python -m pip install -r requirements.txt
python core/master.py health
