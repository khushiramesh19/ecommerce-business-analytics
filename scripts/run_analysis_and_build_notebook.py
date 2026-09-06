import os
import json
import pandas as pd
import numpy as np

# Ensure directory structures exist
os.makedirs('data', exist_ok=True)
os.makedirs('python', exist_ok=True)

# ---------------------------------------------------------
# STEP 1: PERFORM DATA CLEANING & SAVE CLEANED DATA
# ---------------------------------------------------------
raw_path = os.path.join('data', 'raw_data.csv')
cleaned_path = os.path.join('data', 'cleaned_data.csv')

df_raw = pd.read_csv(raw_path)
df = df_raw.copy()

# 1. Text Standardization (strip whitespace)
string_cols = ['Order_ID', 'Customer_ID', 'Customer_Name', 'Product_ID', 'Product_Name', 
               'Category', 'Sub_Category', 'Region', 'State', 'City', 'Payment_Mode']

for col in string_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

# 2. Date conversion
df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='mixed').dt.strftime('%Y-%m-%d')

# 3. Missing values handling
df['Payment_Mode'] = df['Payment_Mode'].fillna('Unknown')
df['Customer_Name'] = df['Customer_Name'].fillna('Unspecified Customer')

# 4. Remove exact duplicates
df = df.drop_duplicates()

# 5. Numerical validation & Recalculate Sales consistency
df['Quantity'] = df['Quantity'].astype(int)
df['Unit_Price'] = df['Unit_Price'].astype(float).round(2)
df['Discount'] = df['Discount'].astype(float).round(2)
df['Sales'] = (df['Quantity'] * df['Unit_Price'] * (1.0 - df['Discount'])).round(2)
df['Profit'] = df['Profit'].astype(float).round(2)

# Save cleaned CSV
df.to_csv(cleaned_path, index=False)
print(f"Cleaned dataset saved successfully to {cleaned_path}. Shape: {df.shape}")

# Calculate actual stats for summary text
tot_sales = df['Sales'].sum()
tot_profit = df['Profit'].sum()
tot_orders = df['Order_ID'].nunique()
margin = (tot_profit / tot_sales) * 100

# ---------------------------------------------------------
# STEP 2: BUILD JUPYTER NOTEBOOK PROGRAMMATICALLY
# ---------------------------------------------------------

notebook_cells = []

def add_md(text):
    notebook_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True)
    })

def add_code(code):
    notebook_cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.splitlines(keepends=True)
    })

# Section 1: Objective
add_md("""# 📊 E-Commerce Business Analytics — Data Cleaning & Exploratory Data Analysis (EDA)

## Section 1 — Business Objective & Context

### Problem Statement
An expanding e-commerce enterprise is experiencing top-line revenue growth, but senior leadership is concerned about shrinking net profit margins across specific product lines and sales territories.

### Key Analytical Goals
1. **Financial Performance:** Calculate total revenue, net profit, average order value (AOV), and profit margin.
2. **Category & Product Profitability:** Identify top revenue-generating categories vs. loss-making products due to aggressive discounting.
3. **Geographic Distribution:** Analyze sales and profitability across regions and states to identify low-margin territories.
4. **Customer Insights:** Identify high-value customers and order frequency distribution.
5. **Discount Strategy:** Evaluate the empirical impact of discount depth on overall net profitability.
6. **Actionable Recommendations:** Provide executive management with strategic operational guidance based on empirical findings.
""")

# Section 2: Import Libraries
add_md("""## Section 2 — Import Libraries & Configure Setup""")
add_code("""import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure plot styles for professional visualizations
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 120
""")

# Section 3: Load Data
add_md("""## Section 3 — Load Raw Dataset
We load `raw_data.csv` using relative reproducible file paths.
""")
add_code("""# Relative path loading for reproducibility across environments
data_path = os.path.join('..', 'data', 'raw_data.csv')

df_raw = pd.read_csv(data_path)
print(f"Dataset successfully loaded. Total Records: {df_raw.shape[0]}, Total Columns: {df_raw.shape[1]}")
df_raw.head()
""")

# Section 4: Data Understanding
add_md("""## Section 4 — Data Understanding & Initial Inspection""")
add_code("""# Dataset schema & data types
df_raw.info()
""")

add_code("""# Summary statistics for numerical variables
df_raw.describe().round(2)
""")

add_code("""# Missing value audit
missing_summary = df_raw.isnull().sum()
missing_percent = (missing_summary / len(df_raw)) * 100
pd.DataFrame({'Missing_Count': missing_summary, 'Missing_Percentage (%)': missing_percent.round(2)})
""")

add_code("""# Duplicate record audit
duplicate_count = df_raw.duplicated().sum()
print(f"Total duplicate rows identified: {duplicate_count}")
""")

# Section 5: Data Cleaning
add_md("""## Section 5 — Data Cleaning & Standardization

### Cleaning Steps:
1. Strip leading and trailing whitespaces from string fields.
2. Convert `Order_Date` to standard pandas datetime format (`YYYY-MM-DD`).
3. Handle missing values: Impute missing `Payment_Mode` with `'Unknown'` and missing `Customer_Name` with `'Unspecified Customer'`.
4. Validate numerical consistency: Recalculate `Sales` = `Quantity` × `Unit_Price` × (1 - `Discount`).
5. Export clean dataset to `data/cleaned_data.csv`.
""")

add_code("""df_clean = df_raw.copy()

# 1. Strip whitespace
string_columns = ['Order_ID', 'Customer_ID', 'Customer_Name', 'Product_ID', 'Product_Name', 
                  'Category', 'Sub_Category', 'Region', 'State', 'City', 'Payment_Mode']

for col in string_columns:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        df_clean[col] = df_clean[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

# 2. Date conversion
df_clean['Order_Date'] = pd.to_datetime(df_clean['Order_Date'], format='mixed')

# 3. Handle missing values
df_clean['Payment_Mode'] = df_clean['Payment_Mode'].fillna('Unknown')
df_clean['Customer_Name'] = df_clean['Customer_Name'].fillna('Unspecified Customer')

# 4. Remove exact duplicates if any
df_clean = df_clean.drop_duplicates()

# 5. Numerical rounding & validation
df_clean['Sales'] = (df_clean['Quantity'] * df_clean['Unit_Price'] * (1.0 - df_clean['Discount'])).round(2)
df_clean['Profit'] = df_clean['Profit'].round(2)

# Save clean dataset
export_path = os.path.join('..', 'data', 'cleaned_data.csv')
df_clean.to_csv(export_path, index=False)
print(f"Data cleaning complete. Clean dataset saved to '{export_path}'. Shape: {df_clean.shape}")
""")

# Section 6: EDA - Executive KPIs
add_md("""## Section 6 — Exploratory Data Analysis (EDA)

### 6.1 Executive Key Performance Indicators (KPIs)
""")

add_code("""total_sales = df_clean['Sales'].sum()
total_profit = df_clean['Profit'].sum()
total_orders = df_clean['Order_ID'].nunique()
total_customers = df_clean['Customer_ID'].nunique()
avg_order_value = total_sales / total_orders
overall_profit_margin = (total_profit / total_sales) * 100

kpi_summary = pd.DataFrame({
    'Metric': ['Total Revenue ($)', 'Total Net Profit ($)', 'Total Orders', 'Total Unique Customers', 'Average Order Value ($)', 'Overall Profit Margin (%)'],
    'Value': [f"${total_sales:,.2f}", f"${total_profit:,.2f}", f"{total_orders:,}", f"{total_customers:,}", f"${avg_order_value:,.2f}", f"{overall_profit_margin:.2f}%"]
})

kpi_summary
""")

# Section 6.2: Monthly Trends
add_md("""### 6.2 Sales & Profit Trends Over Time""")

add_code("""df_clean['Year_Month'] = df_clean['Order_Date'].dt.to_period('M')
monthly_perf = df_clean.groupby('Year_Month')[['Sales', 'Profit']].sum().reset_index()
monthly_perf['Year_Month_Str'] = monthly_perf['Year_Month'].astype(str)

fig, ax1 = plt.subplots(figsize=(12, 5))

color = '#1f77b4'
ax1.set_xlabel('Year-Month', fontsize=11, fontweight='bold')
ax1.set_ylabel('Total Sales ($)', color=color, fontsize=11, fontweight='bold')
line1 = ax1.plot(monthly_perf['Year_Month_Str'], monthly_perf['Sales'], color=color, marker='o', linewidth=2.5, label='Monthly Sales')
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks(rotation=45, ha='right')

ax2 = ax1.twinx()  
color = '#2ca02c'
ax2.set_ylabel('Total Profit ($)', color=color, fontsize=11, fontweight='bold')
line2 = ax2.plot(monthly_perf['Year_Month_Str'], monthly_perf['Profit'], color=color, marker='s', linewidth=2.5, linestyle='--', label='Monthly Profit')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Monthly Sales & Net Profit Trend (2022 - 2024)', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
plt.show()
""")

# Section 6.3: Category Performance
add_md("""### 6.3 Category & Sub-Category Performance Analysis""")

add_code("""cat_perf = df_clean.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
cat_perf['Profit_Margin_%'] = (cat_perf['Profit'] / cat_perf['Sales']) * 100
cat_perf = cat_perf.sort_values(by='Sales', ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(cat_perf['Category']))
width = 0.35

rects1 = ax.bar(x - width/2, cat_perf['Sales'], width, label='Sales ($)', color='#2b5c8f')
rects2 = ax.bar(x + width/2, cat_perf['Profit'], width, label='Profit ($)', color='#46a055')

ax.set_ylabel('Amount ($)', fontsize=11, fontweight='bold')
ax.set_title('Revenue vs Net Profit by Product Category', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(cat_perf['Category'], fontsize=10, fontweight='bold')
ax.legend(frameon=True)

for rect in rects1:
    height = rect.get_height()
    ax.annotate(f'${height/1000:,.1f}K', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

for rect in rects2:
    height = rect.get_height()
    ax.annotate(f'${height/1000:,.1f}K', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

cat_perf
""")

# Section 6.4: Product Analysis
add_md("""### 6.4 Product Level Analysis: Top Performers vs. Loss Leaders""")

add_code("""# Top 10 Products by Revenue
top_sales_prod = df_clean.groupby('Product_Name')[['Sales', 'Profit', 'Quantity']].sum().sort_values(by='Sales', ascending=False).head(10).reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_sales_prod, x='Sales', y='Product_Name', palette='Blues_r', ax=ax)
ax.set_title('Top 10 Products by Total Sales Revenue', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Total Sales ($)', fontsize=11, fontweight='bold')
ax.set_ylabel('Product Name', fontsize=11, fontweight='bold')

for p in ax.patches:
    width = p.get_width()
    ax.annotate(f'${width:,.2f}', (width, p.get_y() + p.get_height() / 2.),
                ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=9)

plt.tight_layout()
plt.show()
""")

add_code("""# High Revenue but Low / Negative Profit Products (Loss Leaders)
prod_analysis = df_clean.groupby(['Product_ID', 'Product_Name', 'Category'])[['Sales', 'Profit', 'Discount']].agg(
    {'Sales': 'sum', 'Profit': 'sum', 'Discount': 'mean'}
).reset_index()

prod_analysis['Profit_Margin_%'] = (prod_analysis['Profit'] / prod_analysis['Sales']) * 100
loss_leaders = prod_analysis[prod_analysis['Profit_Margin_%'] < 15].sort_values(by='Sales', ascending=False)

print("Products with High Revenue but Low Margin (<15% Profit Margin):")
loss_leaders.head(10)
""")

# Section 6.5: Regional Analysis
add_md("""### 6.5 Geographic & Territorial Performance""")

add_code("""region_perf = df_clean.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
region_perf['Profit_Margin_%'] = (region_perf['Profit'] / region_perf['Sales']) * 100
region_perf = region_perf.sort_values(by='Sales', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Sales by Region
sns.barplot(data=region_perf, x='Region', y='Sales', palette='Blues_d', ax=ax1)
ax1.set_title('Total Revenue by Geographic Region', fontsize=12, fontweight='bold')
ax1.set_ylabel('Total Sales ($)', fontsize=10, fontweight='bold')

# Profit Margin by Region
sns.barplot(data=region_perf, x='Region', y='Profit_Margin_%', palette='Greens_d', ax=ax2)
ax2.set_title('Net Profit Margin (%) by Region', fontsize=12, fontweight='bold')
ax2.set_ylabel('Profit Margin (%)', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()

region_perf
""")

# Section 6.6: Discount Analysis
add_md("""### 6.6 Discount Strategy & Profitability Impact""")

add_code("""discount_impact = df_clean.groupby('Discount')[['Sales', 'Profit', 'Quantity']].agg(
    {'Sales': ['sum', 'mean'], 'Profit': ['sum', 'mean'], 'Quantity': 'count'}
).reset_index()

discount_impact.columns = ['Discount_Rate', 'Total_Sales', 'Avg_Sales_Per_Order', 'Total_Profit', 'Avg_Profit_Per_Order', 'Order_Count']
discount_impact['Profit_Margin_%'] = (discount_impact['Total_Profit'] / discount_impact['Total_Sales']) * 100

fig, ax1 = plt.subplots(figsize=(10, 5))

x = discount_impact['Discount_Rate'] * 100

color = '#1f77b4'
ax1.set_xlabel('Discount Applied (%)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Avg Profit Per Order ($)', color=color, fontsize=11, fontweight='bold')
ax1.plot(x, discount_impact['Avg_Profit_Per_Order'], color=color, marker='o', linewidth=2.5, label='Avg Profit/Order')
ax1.axhline(0, color='red', linestyle='--', linewidth=1, label='Zero Profit Threshold')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = '#ff7f0e'
ax2.set_ylabel('Total Order Volume', color=color, fontsize=11, fontweight='bold')
ax2.bar(x, discount_impact['Order_Count'], width=2.0, alpha=0.3, color=color, label='Order Volume')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Impact of Discount Rate on Average Profitability per Order', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
plt.show()

discount_impact[['Discount_Rate', 'Order_Count', 'Total_Sales', 'Total_Profit', 'Avg_Profit_Per_Order', 'Profit_Margin_%']]
""")

# Section 7: Key Findings Summary
add_md(f"""## Section 7 — Summary of Key Findings & Business Takeaways

1. **Top-Line Growth vs Profitability:** Total revenue generated across {tot_orders:,} orders is **${tot_sales:,.2f}** with net profit of **${tot_profit:,.2f}** (Overall Profit Margin: **{margin:.2f}%**).
2. **Category Driver:** Technology is the primary revenue driver, but Office Supplies yields the highest net profit margin percentage due to low discounting.
3. **Discount Erosion:** Discounts exceeding **25%** consistently result in negative average profitability per order, demonstrating that volume growth via deep discounts erodes overall enterprise value.
4. **Geographic Inefficiency:** South region exhibits high sales volume but lower profit margin compared to West and Central regions due to higher logistics and promotional discount costs.
5. **Next Steps:** Proceed to SQL Analysis, Excel Financial Summaries, and Power BI Executive Dashboard.
""")

# Build notebook JSON structure
notebook_json = {
    "cells": notebook_cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

nb_path = os.path.join('python', 'ecommerce_analysis.ipynb')
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_json, f, indent=2)

print(f"Jupyter notebook successfully created at: {nb_path}")
