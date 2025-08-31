import os, re, pandas as pd
from .utils import normalize_columns, categorize_industry

def extract_state_from_filename(path: str) -> str:
    m = re.search(r"_STATE_([A-Z_]+)-\d{4}\.csv", os.path.basename(path))
    if m:
        return m.group(1).replace("_", " ").title()
    return "Unknown"

def read_csv_safely(path: str) -> pd.DataFrame:
    for sep in [",", "|", "\t"]:
        for enc in ["utf-8", "latin-1"]:
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc)
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue
    return pd.read_csv(path, low_memory=False)

def load_and_merge_csvs(data_dir: str) -> pd.DataFrame:
    paths = [os.path.join(r, f) for r, _, files in os.walk(data_dir) for f in files if f.lower().endswith(".csv")]
    dfs = []
    for p in paths:
        df = read_csv_safely(p)
        df["Source State"] = extract_state_from_filename(p)
        dfs.append(df)

    merged = pd.concat(dfs, ignore_index=True)
    merged = normalize_columns(merged)

    # Deduplicate columns to avoid ValueError
    merged = merged.loc[:, ~merged.columns.duplicated()]

    if "nic_name" in merged.columns:
        merged["industry_group"] = merged["nic_name"].apply(categorize_industry)

    return merged

