"""Minimal NAVARIS core configuration."""
from pathlib import Path
import os
ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_DIR=Path(os.environ.get("NAVARIS_DATA_DIR",ROOT_DIR/"data")).expanduser().resolve()
DB_PATH=Path(os.environ.get("NAVARIS_DB_PATH",DATA_DIR/"navaris_core.sqlite3")).expanduser().resolve()
CURRENCY=os.environ.get("NAVARIS_CURRENCY","USD")
MAX_TEXT_LENGTH=12000
