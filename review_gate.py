"""Human review gate with append-only JSONL audit trail."""
import json, uuid
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ALLOWED={'approve','edit','reject'}

def review_gate_v1(report, decision, reviewer_note=''):
    if decision not in ALLOWED:
        raise ValueError("decision must be one of: approve, edit, reject")
    run_id=report.get('run_id') or str(uuid.uuid4())
    region=report.get('region','portfolio')
    downstream_allowed=(decision=='approve')
    updated=dict(report)
    updated.update({'run_id':run_id,'decision':decision,'reviewer_note':reviewer_note,'downstream_use_allowed':downstream_allowed})
    entry={'timestamp':datetime.now(timezone.utc).isoformat(),'run_id':run_id,'region':region,'decision':decision,'reviewer_note':reviewer_note}
    with open(ROOT/'audit_log.jsonl','a',encoding='utf-8') as f: f.write(json.dumps(entry,separators=(',',':'))+'\n')
    return updated

def main():
    # Fresh test harness entries demonstrate all three paths. The approved memo is the downstream artifact.
    sample={'region':'Guntur','headline':'April to May sales movement','run_id':'demo-guntur-2026-09-28'}
    for decision,note in [('approve','Verified against SQL metrics; approved for downstream use.'),('edit','Clarify that the threshold is an operational alert, not a statistical test.'),('reject','Evidence block needs correction before release.')]:
        before=dict(sample)
        after=review_gate_v1(sample,decision,note)
        print('\nBEFORE:',before); print('AFTER:',after)
if __name__=='__main__': main()
