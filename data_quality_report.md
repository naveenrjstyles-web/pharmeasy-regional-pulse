# Data Quality Report

| Fix implemented | Quality dimension | Why it matters |
|---|---|---|
| Remove 59 exact duplicate rows | **Uniqueness** | Prevents the same source record from being counted twice. |
| Strip whitespace and title-case region names | **Consistency** | Makes equivalent region labels join to one canonical master-data value. |
| Product → category lookup for 48 missing categories | **Completeness** and **Validity** | Recovers missing categorical values from an exact deterministic relationship instead of dropping valid orders. |
| Category-level mean margin imputation for 94 missing profits | **Completeness** and **Accuracy** | Restores profit values using the specified category-specific margin rule and preserves the sales relationship. |
| Required-column schema validation | **Validity** | Blocks downstream processing when a required field is absent. |
| Region master join validation | **Relevance** | Keeps Kurnool visible as a valid master region even though it has zero orders. |
| Month/date parsing and numeric coercion | **Timeliness** and **Validity** | Ensures records can be grouped by reporting month and numeric metrics can be calculated reliably. |

## Deterministic checkpoints

- Raw rows: **2,159**.
- Exact duplicates removed: **59**.
- Clean rows: **2,100**.
- Raw region variants after deduplication: **16**.
- Canonical active regions after normalization: **9**.
- Missing categories imputed: **48**.
- Missing profits imputed: **94**.
- Clean schema validation: **validated**.
- Deliberately broken schema validation: **blocked_schema**, missing `profit_inr`.
