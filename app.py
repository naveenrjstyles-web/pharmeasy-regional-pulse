import sqlite3
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from draft_report import draft_report_v1
from metrics_engine import compute_percentage_change_v1, flag_significant_regions_v1

ROOT=Path(__file__).resolve().parent
DB=ROOT/'pharmeasy.db'

st.set_page_config(page_title='PharmEasy Regional Pulse',layout='wide')

@st.cache_data
def load_data():
    with sqlite3.connect(DB) as con:
        orders=pd.read_sql_query('SELECT * FROM orders_clean',con)
        regions=pd.read_sql_query('SELECT * FROM regions_master',con)
    orders['month']=orders['order_date'].str[:7]
    return orders,regions

if not DB.exists():
    st.error('pharmeasy.db is missing. Run: python3 generate_dataset.py && python3 clean_data.py && python3 build_db.py')
    st.stop()
orders,regions=load_data()
months=['2026-04','2026-05','2026-06']
selected=st.sidebar.selectbox('Region filter',['All regions']+regions['region'].tolist())
view=orders if selected=='All regions' else orders[orders.region==selected]

# Verified portfolio metrics used by the executive summary.
total_sales=view.sales_inr.sum(); total_profit=view.profit_inr.sum(); total_orders=view.order_id.nunique()
month_sales=view.groupby('month').sales_inr.sum().reindex(months,fill_value=0)
month_orders=view.groupby('month').order_id.nunique().reindex(months,fill_value=0)
cat=view.groupby('category').agg(sales_inr=('sales_inr','sum'),profit_inr=('profit_inr','sum'),order_count=('order_id','nunique')).reset_index().sort_values('sales_inr',ascending=False)
region_month=view.groupby(['region','month']).agg(sales_inr=('sales_inr','sum'),profit_inr=('profit_inr','sum'),order_count=('order_id','nunique')).reset_index()

# Flags from the same Part 2 function.
portfolio_metrics=orders.groupby(['region','month']).agg(sales_inr=('sales_inr','sum'),order_count=('order_id','nunique')).reset_index()
sales_pivot=portfolio_metrics.pivot(index='region',columns='month',values='sales_inr').fillna(0)
flagged=[]
for p,c in [('2026-04','2026-05'),('2026-05','2026-06')]:
    changes={r:compute_percentage_change_v1(float(row.get(c,0)),float(row.get(p,0))) for r,row in sales_pivot.iterrows()}
    flagged.extend(flag_significant_regions_v1(changes))

st.title('PharmEasy Regional Pulse')
st.caption('SQL-verified regional performance • April–June 2026 • human-review-ready outputs')

# 3–5 sentence CII executive summary.
headline=f"The selected view contains {total_orders:,} distinct orders, INR {total_sales:,.2f} sales, and INR {total_profit:,.2f} profit."
shape=f"Monthly sales were {month_sales['2026-04']:,.2f} in April, {month_sales['2026-05']:,.2f} in May, and {month_sales['2026-06']:,.2f} in June."
if selected=='All regions':
    topcat=cat.iloc[0]
    breakdown=f"{topcat['category']} is the largest category by sales at INR {topcat['sales_inr']:,.2f}, while the review engine flags {len(set(flagged))} unique regions across the two month-on-month transitions."
elif cat.empty:
    breakdown=f"{selected} has no orders in the selected period; its zero-order status remains visible in the detail view."
else:
    topcat=cat.iloc[0]
    breakdown=f"For {selected}, {topcat['category']} is the largest category by sales at INR {topcat['sales_inr']:,.2f}; the region-level detail below shows its monthly movement."
implication='The operational implication is to review flagged movements before treating them as durable changes; use the CII narrative and memo for the human decision checkpoint.'
summary=' '.join([headline,shape,breakdown,implication,'Use the trend, comparison, category, and detail views below to inspect the selected results.'])
st.info(summary)

k1,k2,k3=st.columns(3)
k1.metric('Total sales (INR)',f'{total_sales:,.2f}')
k2.metric('Total profit (INR)',f'{total_profit:,.2f}')
k3.metric('Distinct order count',f'{total_orders:,}')

st.header('1. Trend — How did monthly sales move by region?')
fig=go.Figure()
regions_to_plot=[selected] if selected!='All regions' else regions['region'].tolist()
for r in regions_to_plot:
    y=[float(region_month.loc[(region_month.region==r)&(region_month.month==m),'sales_inr'].sum()) for m in months]
    fig.add_trace(go.Scatter(x=months,y=y,mode='lines+markers',name=r))
fig.update_layout(title='How did monthly sales change by region?',xaxis_title='Month',yaxis_title='Sales (INR)',hovermode='x unified')
fig.update_yaxes(rangemode='tozero')
st.plotly_chart(fig,use_container_width=True)

st.header('2. Comparison — Which regions contribute the most sales?')
bar=orders.groupby('region').sales_inr.sum().reindex(regions['region'],fill_value=0).sort_values(ascending=False)
if selected!='All regions': bar=bar.loc[[selected]]
fig2=go.Figure(go.Bar(x=bar.index,y=bar.values,name='Sales'))
fig2.update_layout(title='Which regions generated the most sales?',xaxis_title='Region',yaxis_title='Total sales (INR)',showlegend=False)
fig2.update_yaxes(rangemode='tozero')
st.plotly_chart(fig2,use_container_width=True)

st.header('3. Category — What category drives the selected view?')
if cat.empty:
    st.info('No category sales are available for this region in the selected period.')
else:
    fig3=go.Figure(go.Pie(labels=cat.category,values=cat.sales_inr,hole=.45,textinfo='label+percent'))
    fig3.update_layout(title='Which categories make up sales?',showlegend=True)
    st.plotly_chart(fig3,use_container_width=True)

st.header('4. Detail — What are the verified region-month numbers?')
detail=region_month.copy()
if selected!='All regions': detail=detail[detail.region==selected]
st.dataframe(detail.sort_values(['region','month']),use_container_width=True,hide_index=True)

st.header('5. CII narrative — What does the movement mean?')
cii_blocks=draft_report_v1(flagged,portfolio_metrics.assign(profit_inr=0))
for b in cii_blocks:
    if selected!='All regions' and b['region']!=selected: continue
    with st.expander(b['region'],expanded=(selected!='All regions' and b['region']==selected)):
        st.markdown(f"**Context:** {b['Context']}")
        st.markdown(f"**Insight:** {b['Insight']}")
        st.markdown(f"**Implication:** {b['Implication']}")

st.header('6. Human review status')
st.write('The narrative and memo are designed for human review; downstream use is permitted only after the approve path of `review_gate_v1()` is recorded in `audit_log.jsonl`.')
