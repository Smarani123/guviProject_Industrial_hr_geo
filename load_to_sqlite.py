import sqlite3, pandas as pd

df = pd.read_csv("data/merged_industrial_workers.csv")

# Save into SQLite
conn = sqlite3.connect("industrial_hr.db")
df.to_sql("workers", conn, if_exists="replace", index=False)

# Example query
q = """
SELECT source_state, SUM(main_workers_total_persons) AS total
FROM workers
GROUP BY source_state
ORDER BY total DESC
LIMIT 5;
"""
print(pd.read_sql(q, conn))
conn.close()