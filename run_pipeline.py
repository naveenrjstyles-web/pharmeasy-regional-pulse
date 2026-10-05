"""Convenience orchestrator: run the complete non-dashboard pipeline in order."""
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
scripts=['generate_dataset.py','clean_data.py','build_db.py','queries.py','draft_report.py','review_gate.py']
for script in scripts:
    print(f'\n=== Running {script} ===')
    subprocess.run([sys.executable,str(ROOT/script)],check=True,cwd=ROOT)
print('\nPipeline completed successfully. Start dashboard with: streamlit run app.py')
