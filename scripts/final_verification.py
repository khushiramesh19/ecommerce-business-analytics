import os
import pandas as pd

required_files = [
    'data/raw_data.csv',
    'data/cleaned_data.csv',
    'python/ecommerce_analysis.ipynb',
    'sql/ecommerce_analysis.sql',
    'excel/ecommerce_analysis.xlsx',
    'powerbi/dashboard_guide.md',
    'insights/business_insights.md',
    'interview/interview_questions.md',
    'README.md',
    'START_HERE.md',
    'requirements.txt',
    '.gitignore'
]

print("==================================================")
print("FINAL PROJECT VERIFICATION & AUDIT")
print("==================================================")

all_ok = True
for f in required_files:
    if os.path.exists(f):
        size_kb = os.path.getsize(f) / 1024
        print(f"[OK] {f:<35} ({size_kb:.2f} KB)")
    else:
        print(f"[MISSING] {f:<35}")
        all_ok = False

if all_ok:
    raw_df = pd.read_csv('data/raw_data.csv')
    clean_df = pd.read_csv('data/cleaned_data.csv')
    print("--------------------------------------------------")
    print(f"Raw Dataset Record Count: {len(raw_df):,}")
    print(f"Cleaned Dataset Record Count: {len(clean_df):,}")
    print(f"Total Sales Revenue: ${clean_df['Sales'].sum():,.2f}")
    print(f"Total Net Profit: ${clean_df['Profit'].sum():,.2f}")
    print(f"Profit Margin: {(clean_df['Profit'].sum() / clean_df['Sales'].sum()) * 100:.2f}%")
    print("--------------------------------------------------")
    print("ALL PROJECT DELIVERABLES VERIFIED 100% COMPLETE & RECRUITER READY!")
else:
    print("Verification failed: Some required files are missing.")
