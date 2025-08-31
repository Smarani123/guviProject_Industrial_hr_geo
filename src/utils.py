import re
import pandas as pd

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    def norm(s):
        return re.sub(r'[^a-z0-9]+', '_', str(s).strip().lower()).strip('_')
    df = df.copy()
    df.columns = [norm(c) for c in df.columns]
    return df

def categorize_industry(name: str) -> str:
    n = str(name).lower()
    rules = [
        ("Retail", r"retail|wholesale|trade"),
        ("Agriculture", r"agri|crop|animal|poultry|farming|forestry|fish"),
        ("Manufacturing - Chemicals", r"chemical|pharma|fertilizer|paint|dye"),
        ("Manufacturing - Plastics & Rubber", r"plastic|rubber"),
        ("Manufacturing - Food", r"food|beverage|bakery|grain|dairy|meat|fish"),
        ("Manufacturing - Metals", r"steel|metal|iron|foundry|fabricated"),
        ("Manufacturing - Textiles", r"textile|garment|apparel|weaving|spinning|knit"),
        ("Manufacturing - Wood & Furniture", r"wood|furniture|sawmill|plywood"),
        ("Construction", r"construction|builder|building|road|bridge|civil"),
        ("Services - Transport & Storage", r"transport|storage|logistics|warehouse"),
        ("Services - ICT", r"computer|telecom|information|software"),
        ("Services - Finance & Real Estate", r"bank|finance|insurance|real estate"),
        ("Services - Education & Health", r"education|school|college|health|hospital"),
        ("Mining & Quarrying", r"mining|quarry|coal|ore|stone"),
        ("Utilities", r"electric|power|gas|water"),
    ]
    for label, pat in rules:
        if re.search(pat, n):
            return label
    return "Other/Uncategorized"
