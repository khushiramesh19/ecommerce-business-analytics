# 🎨 Power BI Executive Dashboard Setup & Implementation Guide

This guide provides step-by-step instructions to assemble a recruiter-grade, executive **E-Commerce Sales & Profitability Dashboard** in Power BI Desktop using `cleaned_data.csv`.

---

## 📐 Dashboard Visual Layout & Grid Blueprint

Canvas Page Setup: **Standard 16:9 Aspect Ratio (1280px × 720px)**

```text
+-------------------------------------------------------------------------------------------------------------------+
| HEADER (Y: 0-60px): E-COMMERCE BUSINESS PERFORMANCE DASHBOARD | Executive Financial & Operational Overview       |
+-------------------------------------------------------------------------------------------------------------------+
| KPI CARDS (Y: 70-150px)                                                                                           |
| [ Total Sales ]   [ Total Profit ]   [ Total Orders ]   [ Customers ]   [ Avg Order Value ]   [ Profit Margin % ] |
+-------------------------------------------------------------+-----------------------------------------------------+
| LEFT COLUMN (X: 20-620px)                                   | RIGHT COLUMN (X: 640-1240px)                        |
|                                                             |                                                     |
| Visual 1: Monthly Revenue & Profit Trend (Line Chart)       | Visual 2: Category Revenue vs Profit (Clustered Bar)|
| (Y: 160-390px, H: 230px)                                    | (Y: 160-390px, H: 230px)                            |
|                                                             |                                                     |
| Visual 3: Top 10 Products by Revenue (Bar Chart)           | Visual 4: Geographic Performance (Region/State)     |
| (Y: 410-640px, H: 230px)                                    | (Y: 410-640px, H: 230px)                            |
+-------------------------------------------------------------+-----------------------------------------------------+
| BOTTOM SLICER BAR (Y: 650-710px)                                                                                  |
| [ Date Range Slicer ] | [ Region Slicer ] | [ Category Slicer ] | [ Payment Mode Slicer ]                        |
+-------------------------------------------------------------------------------------------------------------------+
```

---

## 🎨 Theme, Typography & Color Palette

To ensure a recruiter-ready executive appearance, avoid default Power BI colors and gradients.

- **Primary Brand / Header Color:** `#1F4E78` (Deep Corporate Navy)
- **Profit / Positive Indicator:** `#2E7D32` (Emerald Green)
- **Revenue Line / Accent Color:** `#0072C6` (Cobalt Blue)
- **Alert / Loss / Negative Margin:** `#C62828` (Crimson Red)
- **Background / Card Fill:** `#F8F9FA` (Soft Off-White)
- **Typography:** Segoe UI (Titles: 14pt Semi-Bold | Subtitles: 10pt Regular | KPI Values: 22pt Bold)

---

## 🧮 DAX Measures Dictionary

Create a dedicated measure table `_Measures` in Power BI:

### 1. Total Sales Revenue
```dax
Total Sales = 
SUM('cleaned_data'[Sales])
```
*Format:* Currency (`$#,##0.00`)

### 2. Total Net Profit
```dax
Total Profit = 
SUM('cleaned_data'[Profit])
```
*Format:* Currency (`$#,##0.00`)

### 3. Total Orders Processed
```dax
Total Orders = 
DISTINCTCOUNT('cleaned_data'[Order_ID])
```
*Format:* Whole Number (`#,##0`)

### 4. Total Unique Customers
```dax
Total Customers = 
DISTINCTCOUNT('cleaned_data'[Customer_ID])
```
*Format:* Whole Number (`#,##0`)

### 5. Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE([Total Sales], [Total Orders], 0)
```
*Format:* Currency (`$#,##0.00`)

### 6. Net Profit Margin (%)
```dax
Profit Margin % = 
DIVIDE([Total Profit], [Total Sales], 0)
```
*Format:* Percentage (`0.00%`)

### 7. Deep Discount Order Count
```dax
High Discount Orders = 
CALCULATE(
    [Total Orders], 
    'cleaned_data'[Discount] > 0.20
)
```
*Format:* Whole Number (`#,##0`)

---

## 📊 Visuals Configuration Matrix & Interview Defense

| Visual Name | Visual Type | X-Axis / Category | Y-Axis / Metric | Purpose & Interview Rationale |
|---|---|---|---|---|
| **KPI Executive Banner** | Card (New) / Multi-row Card | Metric Headers | `[Total Sales]`, `[Total Profit]`, `[Total Orders]`, `[Total Customers]`, `[AOV]`, `[Profit Margin %]` | Provides instant operational health overview for executive stakeholders. |
| **Sales & Profit Trend** | Line & Clustered Column Chart | `Order_Date` (Year-Month) | Column: `[Total Sales]` \| Line: `[Total Profit]` | Evaluates seasonality and detects month-over-month margin compression. |
| **Category Breakdown** | Clustered Bar Chart | `Category` | `[Total Sales]` & `[Total Profit]` | Compares top-line revenue against bottom-line margin across product groups. |
| **Top 10 Products** | Horizontal Bar Chart | `Product_Name` (Top 10 filter) | `[Total Sales]` | Highlights revenue concentration among core catalog items. |
| **Regional Performance** | Treemap / Filled Map | `Region`, `State` | Values: `[Total Sales]`, Tooltip: `[Profit Margin %]` | Identifies geographical territories with high sales but weak operational margins. |
| **Discount vs Margin** | Scatter Plot / Column | `Discount` | Y: `[Profit Margin %]`, Size: `[Total Sales]` | Empirically proves that deep discounts (>20%) destroy overall profit margin. |

---

## ⚙️ Step-by-Step Implementation Instructions

### Step 1: Data Import
1. Open Power BI Desktop.
2. Select **Get Data → Text/CSV**.
3. Choose `data/cleaned_data.csv`.
4. Verify column data types: `Order_Date` (Date), `Sales` (Decimal Number), `Profit` (Decimal Number), `Discount` (Decimal Number), `Quantity` (Whole Number).

### Step 2: Create DAX Measures
1. Click **Enter Data** → Name table `_Measures`.
2. Right-click `_Measures` → **New Measure** and enter each DAX formula listed above.

### Step 3: Configure Canvas Layout & Background
1. Click Canvas Background → Color: `#F4F6F9`, Transparency: `0%`.
2. Insert Top Shape Header Rectangle (Color: `#1F4E78`, Height: `60px`).
3. Add Title TextBox: **E-COMMERCE BUSINESS ANALYTICS DASHBOARD** (White text, Segoe UI Semibold 16pt).

### Step 4: Build Visuals
1. **KPI Cards:** Add Card visuals along top row (Y: 70px). Set Background to White, Border Radius: 4px, Shadow: Off.
2. **Monthly Trend Line Chart:** Add Line Chart. Axis: `Order_Date` (Month-Year), Values: `[Total Sales]` and `[Total Profit]`.
3. **Category Bar Chart:** Add Bar Chart. Y-Axis: `Category`, X-Axis: `[Total Sales]` and `[Total Profit]`.
4. **Top 10 Products:** Add Horizontal Bar Chart. Filter Pane → Top N = 10 by `[Total Sales]`.
5. **Interactive Slicers:** Add slicers at bottom for `Date Range`, `Region`, `Category`, and `Payment_Mode`.

---

## 🎯 Interview Q&A Alignment: Power BI Defense

**Interviewer Question:** *"Why did you choose a Line and Column chart for monthly performance?"*
**Answer:** *"Line and Column combo chart allows us to plot two distinct monetary scales simultaneously. Column bars represent top-line revenue volume while the overlaid line tracks net profit margin, making revenue-profit divergences instantly visible to executive management."*
