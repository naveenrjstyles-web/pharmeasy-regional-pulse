"""Generate Context-Insight-Implication blocks from verified metrics."""
from pathlib import Path
import pandas as pd
from metrics_engine import compute_percentage_change_v1, flag_significant_regions_v1
ROOT=Path(__file__).resolve().parent

def draft_report_v1(flagged_regions, metrics):
    m=metrics.copy()
    m['month']=m['month'].astype(str)
    sales=m.pivot(index='region',columns='month',values='sales_inr').fillna(0)
    orders=m.pivot(index='region',columns='month',values='order_count').fillna(0)
    blocks=[]
    for region in sorted(set(flagged_regions)):
        row=m[m.region==region].sort_values('month')
        months=list(row.month)
        changes=[]
        for prev,curr in [('2026-04','2026-05'),('2026-05','2026-06')]:
            if prev in sales.columns and curr in sales.columns:
                ch=compute_percentage_change_v1(float(sales.loc[region,curr]),float(sales.loc[region,prev]))
                if abs(ch)>8: changes.append((prev,curr,ch))
        first=row.iloc[0]
        latest=row.iloc[-1]
        change_text='; '.join(f'{a}→{b}: {c:+.2f}%' for a,b,c in changes)
        context=(f"{region} recorded {int(first.order_count)} orders and INR {first.sales_inr:,.2f} sales in April 2026; "
                 f"its June 2026 position was {int(latest.order_count)} orders and INR {latest.sales_inr:,.2f} sales.")
        insight=f"The verified SQL sales movements above the 8% operational threshold are {change_text}."
        implication=("The flag means the regional lead should inspect the underlying order/category mix before treating the movement as a durable change; "
                     "the alert is an operational review trigger, not a statistical significance test.")
        blocks.append({'region':region,'Context':context,'Insight':insight,'Implication':implication,'changes':changes})
    return blocks

def main():
    metrics=pd.read_csv(ROOT/'region_month_metrics.csv')
    sales=metrics.pivot(index='region',columns='month',values='sales_inr').fillna(0)
    flagged=[]
    for p,c in [('2026-04','2026-05'),('2026-05','2026-06')]:
        changes={r:compute_percentage_change_v1(float(v.get(c,0)),float(v.get(p,0))) for r,v in sales.iterrows()}
        flagged += flag_significant_regions_v1(changes)
    blocks=draft_report_v1(flagged,metrics)
    with open(ROOT/'cii_report.md','w',encoding='utf-8') as f:
        f.write('# CII Review Draft\n\n')
        for b in blocks:
            f.write(f"## {b['region']}\n\n**Context:** {b['Context']}\n\n**Insight:** {b['Insight']}\n\n**Implication:** {b['Implication']}\n\n")
    print(f'Generated {len(blocks)} unique CII blocks.')
if __name__=='__main__': main()
