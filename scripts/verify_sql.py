import sqlite3
import pandas as pd
import os

cleaned_path = os.path.join('data', 'cleaned_data.csv')
sql_path = os.path.join('sql', 'ecommerce_analysis.sql')

df = pd.read_csv(cleaned_path)

conn = sqlite3.connect(':memory:')
df.to_sql('ecommerce_sales', conn, index=False, if_exists='replace')

with open(sql_path, 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Split statements by semicolon
statements = [s.strip() for s in sql_script.split(';') if s.strip() and not s.strip().startswith('-- =')]

print(f"Testing {len(statements)} SQL statements against SQLite...")

success_count = 0
for idx, stmt in enumerate(statements, 1):
    # Remove leading comments
    lines = stmt.splitlines()
    clean_lines = [l for l in lines if not l.strip().startswith('--')]
    clean_sql = '\n'.join(clean_lines).strip()
    
    if not clean_sql:
        continue
        
    try:
        res = pd.read_sql_query(clean_sql, conn)
        success_count += 1
        print(f"Query {success_count} SUCCESS! Returned {len(res)} rows. First col: {res.columns[0]}")
    except Exception as e:
        print(f"Query {idx} FAILED! Error: {e}")
        print("SQL Code:")
        print(clean_sql[:200])

print(f"\nCompleted SQL Verification: {success_count}/{len(statements)} queries executed successfully.")
conn.close()
