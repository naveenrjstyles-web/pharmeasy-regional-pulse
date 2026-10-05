"""Clean and validate the PharmEasy monthly export."""
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS=["order_id","order_date","region","category","product","quantity","sales_inr","profit_inr"]
ROOT=Path(__file__).resolve().parent


def validate_schema(df, required_columns):
    missing=[c for c in required_columns if c not in df.columns]
    return {"status":"validated" if not missing else "blocked_schema","row_count":len(df),"missing_columns":missing}


def clean_orders(raw_path=ROOT/"pharmeasy_orders_raw.csv", output_path=ROOT/"orders_clean.csv"):
    df=pd.read_csv(raw_path, dtype=str)
    original=len(df)
    duplicate_mask=df.duplicated(keep="first")
    duplicates=int(duplicate_mask.sum())
    df=df.loc[~duplicate_mask].copy()
    raw_variants=int(df["region"].nunique(dropna=False))
    df["region"]=df["region"].str.strip().str.title()
    canonical=set(pd.read_csv(ROOT/"regions_master.csv")["region"])-{"Kurnool"}
    bad_regions=sorted(set(df["region"])-canonical)
    if bad_regions: raise ValueError(f"Unexpected canonical regions: {bad_regions}")
    # Exact product -> category lookup from rows whose category is present.
    lookup=(df.loc[df["category"].notna() & (df["category"].str.strip()!=""),["product","category"]]
              .drop_duplicates("product").set_index("product")["category"].to_dict())
    missing_category_before=int(df["category"].isna().sum()+ (df["category"].astype(str).str.strip()=="").sum())
    df["category"]=df["category"].replace(r"^\s*$",pd.NA,regex=True)
    df["category"]=df["category"].fillna(df["product"].map(lookup))
    if df["category"].isna().any(): raise ValueError("Unresolved category values remain")
    df["sales_inr"]=pd.to_numeric(df["sales_inr"],errors="raise")
    df["profit_inr"]=pd.to_numeric(df["profit_inr"],errors="coerce")
    missing_profit_before=int(df["profit_inr"].isna().sum())
    margins=(df.loc[df["profit_inr"].notna()].assign(margin=lambda x:x["profit_inr"]/x["sales_inr"]).groupby("category")["margin"].mean())
    df["profit_inr"]=df.apply(lambda r: round(r["sales_inr"]*margins[r["category"]],2) if pd.isna(r["profit_inr"]) else round(r["profit_inr"],2),axis=1)
    df["quantity"]=pd.to_numeric(df["quantity"],errors="raise").astype(int)
    df["order_date"]=pd.to_datetime(df["order_date"],errors="raise").dt.strftime("%Y-%m-%d")
    df=df[REQUIRED_COLUMNS]
    if df["profit_inr"].isna().any() or df["category"].isna().any(): raise ValueError("Cleaning left nulls")
    df.to_csv(output_path,index=False)
    report={"raw_rows":original,"duplicates_removed":duplicates,"clean_rows":len(df),"raw_region_variants_after_dedup":raw_variants,"canonical_regions":int(df["region"].nunique()),"missing_category_imputed":missing_category_before,"missing_profit_imputed":missing_profit_before}
    print(report)
    print("schema_clean:",validate_schema(df,REQUIRED_COLUMNS))
    broken=df.drop(columns=["profit_inr"])
    print("schema_broken:",validate_schema(broken,REQUIRED_COLUMNS))
    return df,report

if __name__=="__main__": clean_orders()
