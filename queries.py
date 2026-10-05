"""SQL verification queries and metric extraction."""
import sqlite3
from pathlib import Path
import subprocess, sys, json
import pandas as pd
from metrics_engine import compute_percentage_change_v1, flag_significant_regions_v1, save_state_v1, load_previous_state_v1
ROOT=Path(__file__).resolve().parent; DB=ROOT/'pharmeasy.db'

def run_query(sql, params=()):
    with sqlite3.connect(DB) as con: return pd.read_sql_query(sql,con,params=params)

def build_metrics():
    sql="""
    SELECT r.region, r.state, r.tier,
           substr(o.order_date,1,7) AS month,
           COUNT(DISTINCT o.order_id) AS order_count,
           COALESCE(SUM(o.sales_inr),0) AS sales_inr,
           COALESCE(SUM(o.profit_inr),0) AS profit_inr
    FROM regions_master r
    LEFT JOIN orders_clean o ON r.region=o.region
    GROUP BY r.region,r.state,r.tier,substr(o.order_date,1,7)
    HAVING month IS NOT NULL
    ORDER BY r.region,month
    """
    return run_query(sql)

def main():
    left=run_query('SELECT COUNT(*) AS n FROM regions_master r LEFT JOIN orders_clean o ON r.region=o.region').iloc[0,0]
    inner=run_query('SELECT COUNT(*) AS n FROM regions_master r INNER JOIN orders_clean o ON r.region=o.region').iloc[0,0]
    print('\nJOIN row-count check: LEFT JOIN =',left,'INNER JOIN =',inner,'delta =',left-inner)
    print('\nDuplicate order_id check:')
    print(run_query('SELECT order_id, COUNT(*) AS n FROM orders_clean GROUP BY order_id HAVING COUNT(*) > 1').to_string(index=False))
    nulls=run_query('''SELECT r.region, COUNT(*) AS count_star, COUNT(o.order_id) AS count_order_id FROM regions_master r LEFT JOIN orders_clean o ON r.region=o.region GROUP BY r.region ORDER BY r.region''')
    print('\nCOUNT(*) vs COUNT(order_id):'); print(nulls.to_string(index=False))
    print('\nPer-region order counts ascending:'); print(run_query('''SELECT r.region, COUNT(o.order_id) AS order_count FROM regions_master r LEFT JOIN orders_clean o ON r.region=o.region GROUP BY r.region ORDER BY order_count, r.region''').to_string(index=False))
    metrics=build_metrics(); metrics.to_csv(ROOT/'region_month_metrics.csv',index=False)
    print('\nRegion-month metrics:'); print(metrics.to_string(index=False))
    pivot=metrics.pivot(index='region',columns='month',values='sales_inr').fillna(0)
    for prev,curr in [('2026-04','2026-05'),('2026-05','2026-06')]:
        changes={r:compute_percentage_change_v1(row.get(curr,0),row.get(prev,0)) for r,row in pivot.iterrows()}
        print(f'\n{prev} -> {curr} changes:')
        for r,c in changes.items(): print(f'  {r}: {c:.2f}%')
        print('Flagged:',flag_significant_regions_v1(changes))
    # Persist April summary and demonstrate reload.
    april={r:{'month':'2026-04','sales_inr':float(v)} for r,v in pivot['2026-04'].items()}
    save_state_v1(april,ROOT/'state_2026-04.json')
    state_path=ROOT/'state_2026-04.json'
    reloaded=load_previous_state_v1(state_path)
    # Verify the persistence contract in a fresh Python process as well.
    probe = (
        'import json; from metrics_engine import load_previous_state_v1; '
        f'print(json.dumps(load_previous_state_v1({str(state_path)!r}), sort_keys=True))'
    )
    fresh_json=subprocess.check_output([sys.executable,'-c',probe],cwd=ROOT,text=True).strip()
    fresh=json.loads(fresh_json)
    print('\nState round-trip in current process:', april==reloaded)
    print('State round-trip in fresh Python process:', april==fresh)

if __name__=='__main__': main()
