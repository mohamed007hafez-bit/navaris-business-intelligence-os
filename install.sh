#!/bin/bash
set -euo pipefail
pip install -r requirements.txt
python core/master.py --health
