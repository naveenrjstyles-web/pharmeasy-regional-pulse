"""Reusable deterministic alerting and state-persistence functions."""
import json
from pathlib import Path
from datetime import datetime, timezone

def compute_percentage_change_v1(current, previous):
    if previous == 0: return 0
    return (current-previous)/previous*100

def flag_significant_regions_v1(changes, threshold=8):
    """Return regions whose absolute change exceeds the operational threshold."""
    return sorted([region for region, change in changes.items() if abs(change) > threshold])

def save_state_v1(month_summary, path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(month_summary,indent=2,sort_keys=True),encoding='utf-8')

def load_previous_state_v1(path):
    path=Path(path)
    if not path.exists(): return None
    return json.loads(path.read_text(encoding='utf-8'))
