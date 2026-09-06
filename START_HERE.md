# 🚀 START HERE — E-Commerce Business Analytics Project Guide

Welcome! This is an end-to-end **E-Commerce Business Analytics** portfolio project designed to showcase practical Business Analyst and Data Analyst skills in **Python, SQL, Excel, and Power BI**.

---

## 📌 Project Architecture & Quick Reference

| Directory / File | Purpose | Key Contents |
|---|---|---|
| `data/` | Data Storage | `raw_data.csv` (5,000+ orders), `cleaned_data.csv` |
| `python/` | Data Cleaning & EDA | `ecommerce_analysis.ipynb` (Pandas, Matplotlib) |
| `sql/` | SQL Queries | `ecommerce_analysis.sql` (20 business analytics queries) |
| `excel/` | Financial & Pivot Analysis | `ecommerce_analysis.xlsx` (Summary, Pivots, Charts) |
| `powerbi/` | Power BI Dashboard Guide | `dashboard_guide.md` (DAX, Layout, Visuals) |
| `insights/` | Business Findings | `business_insights.md` (Insights & Actionable Recommendations) |
| `interview/` | Interview Prep | `interview_questions.md` (20 QA + 30s/1m/2m pitch scripts) |
| `README.md` | Main Landing Page | Full portfolio documentation for GitHub |

---

## 🛠️ Step-by-Step Execution Guide

### Step 1: Environment Setup
1. Open terminal inside `Ecommerce-Business-Analytics`.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Python Data Analysis & Cleaning
1. Launch Jupyter Notebook:
   ```bash
   jupyter notebook python/ecommerce_analysis.ipynb
   ```
2. Run all cells sequentially to explore dataset stats, clean data, and output `data/cleaned_data.csv`.

### Step 3: SQL Business Query Execution
1. Open `sql/ecommerce_analysis.sql` in PostgreSQL, MySQL, SQLite, or DB Fiddle.
2. Load `data/cleaned_data.csv` as table `ecommerce_sales`.
3. Execute queries 1 through 20 to review business aggregate calculations, CTEs, and window functions.

### Step 4: Excel Financial Workbook
1. Open `excel/ecommerce_analysis.xlsx` in Microsoft Excel.
2. Review sheets: `Executive Summary`, `Pivot Tables`, `Category Analysis`, and `Regional Performance`.

### Step 5: Power BI Dashboard Setup
1. Open Power BI Desktop.
2. Follow `powerbi/dashboard_guide.md` to import `data/cleaned_data.csv`.
3. Build DAX measures and configure slicers & visuals matching the executive grid layout.


