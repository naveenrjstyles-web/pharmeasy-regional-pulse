# Presentation Storyline — Guntur April→May +122.19%

## Executive audience — Situation / Complication / Resolution

### Situation
Guntur sales increased from **INR 62,442.27 in April** to **INR 138,738.93 in May**, a verified **+122.19%** month-on-month movement. [HIGH]

### Complication
The movement was accompanied by distinct-order growth from **51 to 77** (+50.98%), while June sales then fell to **INR 99,745.18** (−28.11% versus May). [HIGH] The dataset therefore supports a large May movement followed by a partial reversal, but it does not establish a causal reason for either movement. [MEDIUM]

### Resolution
Use the May movement as a human review trigger rather than assuming it is a durable baseline change. [MEDIUM] Review the May category/order mix, particularly Wellness & Nutrition and Medical Devices, then repeat the same SQL-verified comparison at the next monthly checkpoint. [MEDIUM]

## Regional-manager audience — Overview / Category / Detail

### Overview
Guntur's April→May sales movement is **+122.19%**, from **INR 62,442.27** to **INR 138,738.93**. [HIGH]

### Category
In May, Wellness & Nutrition contributed **INR 53,085.01** and Medical Devices contributed **INR 32,766.69** to Guntur sales; these are the two largest category sales contributions for Guntur in May. [HIGH]

### Detail
The detail view is based on the cleaned 2,100-row dataset and SQL grouping by region and month. [LOW] Guntur had **51, 77, and 62** distinct orders in April, May, and June, while sales were **INR 62,442.27, INR 138,738.93, and INR 99,745.18**. [HIGH] The 8% rule is an operational flag threshold, not a statistical significance test. [LOW]

## Anticipated Pushback Q&A

### 1. Why should I believe this number?
**Direct acknowledgement:** The concern is valid because a large percentage movement can be misleading if the underlying rows are duplicated or the join logic is wrong. [LOW]  
**Verified vs. unverified:** The clean dataset contains **2,100 rows after removing 59 exact duplicates**, order IDs are unique, and the SQL region-month output gives Guntur April sales of **INR 62,442.27** and May sales of **INR 138,738.93**, producing **+122.19%**. [HIGH] The calculation does not prove why the movement happened. [MEDIUM]  
**Resolution:** Re-run the same cleaning, SQLite validation, and month-on-month query at the next monthly close; the new evidence should be available in the next scheduled regional review cycle. [LOW]

### 2. What if an alternative explanation is driving this?
**Direct acknowledgement:** The dataset cannot distinguish a causal operational driver from ordinary order-mix movement because it has order, category, product, sales, profit, region, and date fields but no causal-event field. [MEDIUM]  
**Verified vs. unverified:** We can verify the May category contributions and order-count movement, but any claim about promotions, competitor activity, festivals, supply issues, or other external causes would be unverified here. [MEDIUM]  
**Resolution:** Add the relevant operational-event evidence for May and compare it with the same category/order metrics at the next review, then revise the narrative if the added evidence supports another explanation. [LOW]

### 3. What would change your recommendation?
**Direct acknowledgement:** The recommendation is intentionally conditional because June already shows a partial reversal. [MEDIUM]  
**Verified vs. unverified:** If subsequent months continue to show a materially different level with consistent category/order support, that would provide stronger evidence of persistence; the current three-month dataset alone does not establish that persistence. [MEDIUM]  
**Resolution:** Reassess after the next monthly result using the same SQL definitions and review gate before changing the operational baseline. [LOW]
