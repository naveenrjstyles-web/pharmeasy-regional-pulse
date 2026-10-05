"""Build the local SQLite database from the exact Part 1 clean output."""
import sqlite3
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
DB=ROOT/'pharmeasy.db'

def build_db():
    orders=pd.read_csv(ROOT/'orders_clean.csv')
    regions=pd.read_csv(ROOT/'regions_master.csv')
    with sqlite3.connect(DB) as con:
        regions.to_sql('regions_master',con,if_exists='replace',index=False)
        orders.to_sql('orders_clean',con,if_exists='replace',index=False)
        con.execute('CREATE INDEX IF NOT EXISTS idx_orders_region ON orders_clean(region)')
        con.execute('CREATE INDEX IF NOT EXISTS idx_orders_date ON orders_clean(order_date)')
        con.commit()
    print(f'Built {DB.name}: regions_master={len(regions)}, orders_clean={len(orders)}')
if __name__=='__main__': build_db()
