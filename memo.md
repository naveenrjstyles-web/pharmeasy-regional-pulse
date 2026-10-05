# Guntur May Sales Review — One-Page Recommendation Memo

## Title
**Guntur April→May Sales Movement Review** [LOW]

## Context
Guntur generated **INR 62,442.27** in sales from **51 distinct orders** in April 2026. [HIGH]  
Guntur generated **INR 138,738.93** in sales from **77 distinct orders** in May 2026. [HIGH]  
The verified April→May sales change is **+122.19%**. [HIGH]

## Key Insight
The May increase was accompanied by order growth from **51 to 77**, a **50.98%** increase in distinct orders. [HIGH]  
Within May, **Wellness & Nutrition** contributed **INR 53,085.01** of Guntur sales and **Medical Devices** contributed **INR 32,766.69**. [HIGH]  
The following month, Guntur sales fell to **INR 99,745.18** in June, a **28.11%** decrease from May. [HIGH]  
This means the dataset shows a large May movement followed by a partial reversal, rather than evidence that the May level persisted into June. [MEDIUM]

## Evidence
The metrics were calculated from the 2,100-row cleaned order dataset loaded into SQLite and grouped by region and month. [LOW]  
The Guntur April, May, and June sales values were **INR 62,442.27**, **INR 138,738.93**, and **INR 99,745.18**, respectively. [HIGH]  
The corresponding distinct-order counts were **51**, **77**, and **62**. [HIGH]  
The operational review rule flags absolute month-on-month sales movements above **8%**; Guntur therefore triggered the rule in both April→May (**+122.19%**) and May→June (**−28.11%**). [HIGH]

## Recommendation
Treat the May movement as a **review trigger**, not as proof of a sustained structural change. [MEDIUM]  
First, inspect Guntur's May category/order mix, with particular attention to Wellness & Nutrition and Medical Devices because they were the two largest May category sales contributions in this dataset. [MEDIUM]  
Then compare the next available monthly result with May and June using the same SQL metric definition before changing an operational plan. [LOW]

## Next Check
At the next monthly review, recompute Guntur sales and distinct orders using the same cleaned-data and SQL workflow, then compare the new month with June and May. [LOW]  
A materially different category mix or another large month-on-month movement should be routed through the same human review gate before downstream use. [LOW]

## Assumptions
**Single unverified assumption:** the observed May movement is not causally explained by an external event or operational change because this dataset contains order-level performance fields but no causal-driver field; any explanation beyond the observed order/category movements is therefore a hypothesis until corroborating operational evidence is added. [MEDIUM]

## Review Status
Approved for downstream use after human review-gate execution; the audit trail records the approve, edit, and reject test paths. [LOW]
