# PharmEasy Regional Pulse

## 1. Install and run end-to-end

This repository is a zero-API-key, local-only pipeline. It uses Python, pandas, SQLite from the standard library, Streamlit, and Plotly.

### Fresh clone setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Three-command run

**Command 1 — install dependencies:**

```bash
pip install -r requirements.txt
```

**Command 2 — regenerate data and run the complete pipeline (dataset → cleaning → SQL metrics → CII report → review-gate harness):**

```bash
python3 run_pipeline.py
```

Equivalent explicit sequence, if you want to inspect every stage:

```bash
python3 generate_dataset.py && python3 clean_data.py && python3 build_db.py && python3 queries.py && python3 draft_report.py && python3 review_gate.py
```

**Command 3 — launch the dashboard:**

```bash
streamlit run app.py
```

No API key, paid service, signup, or network connection is required at runtime.

## 2. Four-artifact cover note

**Headline finding:** Guntur sales rose from INR 62,442.27 in April 2026 to INR 138,738.93 in May 2026, a verified +122.19% month-on-month movement, followed by a June decline to INR 99,745.18.

- **Streamlit dashboard — `app.py`:** live interactive exploration of verified KPIs, trends, category mix, region comparison, detail rows, and embedded CII narrative.
- **CII narrative — embedded in `app.py`:** explains the flagged movements using Context → Insight → Implication blocks sourced from the SQL metrics.
- **One-page memo — `memo.md`:** the recommendation and evidence for the Guntur review.
- **Presentation storyline — `presentation_storyline.md`:** executive SCR framing, regional-manager OCD framing, and anticipated pushback Q&A.

**Reviewer consumption order:** run the pipeline → open `app.py` → read the embedded CII narrative → read `memo.md` → use `presentation_storyline.md` to defend the finding live.

**Single unverified assumption:** the dataset contains no causal-event field, so any explanation of the Guntur May movement beyond the observed order/category movements is a hypothesis until corroborating operational evidence is added.

## Pipeline architecture

`pharmeasy_orders_raw.csv` → `clean_data.py` → `orders_clean.csv` → `build_db.py` → `pharmeasy.db` → `queries.py` / `metrics_engine.py` → `draft_report.py` → `review_gate.py` + `audit_log.jsonl` → `app.py`.

Every downstream stage consumes the output of the previous stage rather than recomputing an unrelated version of the data.

## Key deterministic checkpoints

| Check | Result |
|---|---:|
| Raw rows | 2,159 |
| Exact duplicates removed | 59 |
| Clean rows | 2,100 |
| Raw region variants after deduplication | 16 |
| Canonical active regions | 9 |
| Master regions | 10, including zero-order Kurnool |
| Missing categories imputed | 48 |
| Missing profits imputed | 94 |
| LEFT JOIN row count | 2,101 |
| INNER JOIN row count | 2,100 |
| Kurnool COUNT(*) | 1 (null-padded row) |
| Kurnool COUNT(order_id) | 0 |
| Guntur Apr→May sales change | +122.19% |
| Unique CII flagged-region union | 8 |

## Repository map

- `generate_dataset.py` — deterministic dataset generator, seed 2026.
- `clean_data.py` — ordered cleaning pipeline and `validate_schema()`.
- `data_quality_report.md` — quality dimensions and fixes.
- `build_db.py` — SQLite database builder.
- `queries.py` — JOIN checks and SQL-verified region/month metrics.
- `metrics_engine.py` — required change, flagging, and state-persistence functions.
- `draft_report.py` — `draft_report_v1()` CII generator.
- `memo.md` — seven-field recommendation memo with risk tags.
- `review_gate.py` — `review_gate_v1()` and three-path test harness.
- `audit_log.jsonl` — generated audit trail.
- `reliability_checklist.md` — safety, validation, critique/refine, human sign-off.
- `app.py` — Streamlit + Plotly dashboard.
- `presentation_storyline.md` — audience reframing and pushback Q&A.
- `run_pipeline.py` — convenience orchestrator for all non-dashboard stages.
- `orders_clean.csv`, `region_month_metrics.csv`, `state_2026-04.json`, `pharmeasy.db` — generated pipeline artifacts.

## Human-review principle

The 8% rule is an operational review threshold, not a statistical significance test. A flag means a human should inspect the number; it does not prove that an underlying business shift occurred. Downstream use is allowed only by the `approve` decision of `review_gate_v1()`.
