import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

NUM_ROWS = 5250

# Lookup dictionaries for realistic structure
CATEGORIES = {
    'Technology': {
        'Laptops & Monitors': [
            ('ProBook 15.6 Inch Laptop', 850.00, 0.22),
            ('UltraSlim 14 Inch Notebook', 1100.00, 0.25),
            ('27-Inch 4K UHD Monitor', 350.00, 0.28),
            ('24-Inch IPS FHD Monitor', 180.00, 0.30)
        ],
        'Accessories': [
            ('Wireless Ergonomic Mouse', 35.00, 0.40),
            ('Mechanical RGB Keyboard', 75.00, 0.35),
            ('USB-C Multi-Port Hub', 45.00, 0.45),
            ('HD Pro Webcam 1080p', 65.00, 0.38)
        ],
        'Phones & Audio': [
            ('Noise Canceling Headphones', 199.00, 0.30),
            ('True Wireless Earbuds', 89.00, 0.35),
            ('Bluetooth Conference Speaker', 120.00, 0.32),
            ('Smart Fitness Watch', 149.00, 0.28)
        ]
    },
    'Furniture': {
        'Chairs & Stools': [
            ('Ergonomic Executive Mesh Chair', 240.00, 0.20),
            ('High-Back Leather Gaming Chair', 290.00, 0.18),
            ('Adjustable Drafting Stool', 110.00, 0.25)
        ],
        'Desks & Tables': [
            ('Electric Dual-Motor Standing Desk', 450.00, 0.18),
            ('Compact Computer Desk', 130.00, 0.22),
            ('Solid Wood Conference Table', 850.00, 0.15)
        ],
        'Bookcases': [
            ('5-Shelf Ladder Bookcase', 140.00, 0.25),
            ('Modern Modular Bookshelf', 210.00, 0.22)
        ]
    },
    'Office Supplies': {
        'Paper & Stationary': [
            ('Premium Multipurpose Copy Paper 5 Reams', 38.00, 0.45),
            ('Executive Hardcover Notebook 3-Pack', 24.00, 0.50),
            ('Gel Ink Pens Box of 24', 15.00, 0.55)
        ],
        'Storage & Organization': [
            ('Heavy-Duty Plastic Storage Bins 4-Pack', 55.00, 0.40),
            ('3-Drawer Mobile File Cabinet', 145.00, 0.28),
            ('Desktop Document Organizer', 28.00, 0.45)
        ],
        'Art & Craft': [
            ('Professional Acrylic Paint Set', 42.00, 0.42),
            ('Precision Cutting Mat & Knife Set', 22.00, 0.48)
        ]
    },
    'Home & Kitchen': {
        'Appliances': [
            ('Digital Touchscreen Air Fryer 5.8Qt', 110.00, 0.30),
            ('Programmable Drip Coffee Maker', 75.00, 0.35),
            ('Compact HEPA Air Purifier', 130.00, 0.28)
        ],
        'Cookware & Dining': [
            ('Non-Stick Ceramic Cookware 10-Piece', 180.00, 0.32),
            ('Stainless Steel Chef Knife 8-Inch', 45.00, 0.45),
            ('Insulated Stainless Steel Tumbler 30oz', 25.00, 0.50)
        ],
        'Bedding & Decor': [
            ('100% Organic Cotton Sheet Set Queen', 85.00, 0.38),
            ('Weighted Cooling Blanket 15lbs', 95.00, 0.35)
        ]
    }
}

REGIONS_GEO = {
    'East': [('New York', 'New York City'), ('New York', 'Buffalo'), ('Pennsylvania', 'Philadelphia'), ('Massachusetts', 'Boston')],
    'West': [('California', 'Los Angeles'), ('California', 'San Francisco'), ('California', 'San Diego'), ('Washington', 'Seattle'), ('Oregon', 'Portland')],
    'Central': [('Illinois', 'Chicago'), ('Texas', 'Houston'), ('Texas', 'Austin'), ('Texas', 'Dallas'), ('Ohio', 'Columbus')],
    'South': [('Florida', 'Miami'), ('Florida', 'Orlando'), ('Georgia', 'Atlanta'), ('North Carolina', 'Charlotte')],
    'North': [('Michigan', 'Detroit'), ('Minnesota', 'Minneapolis'), ('Wisconsin', 'Milwaukee')]
}

PAYMENT_MODES = ['Credit Card', 'Debit Card', 'PayPal', 'UPI / Net Banking', 'Cash on Delivery']
PAYMENT_WEIGHTS = [0.40, 0.25, 0.18, 0.12, 0.05]

FIRST_NAMES = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth',
               'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen',
               'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Donald', 'Sandra',
               'Mark', 'Ashley', 'Paul', 'Kimberly', 'Steven', 'Emily', 'Andrew', 'Donna', 'Kenneth', 'Michelle',
               'Joshua', 'Carol', 'Kevin', 'Amanda', 'Brian', 'Dorothy', 'George', 'Melissa', 'Edward', 'Deborah']

LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
              'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
              'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores']

# Generate ~450 customers
CUSTOMERS = []
for i in range(1, 451):
    c_id = f"CUST-{1000 + i}"
    c_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    CUSTOMERS.append((c_id, c_name))

# Flatten products and assign IDs
PRODUCT_LIST = []
prod_counter = 101
for cat, subcats in CATEGORIES.items():
    for subcat, items in subcats.items():
        for pname, base_price, margin in items:
            pid = f"PROD-{cat[:3].upper()}-{prod_counter}"
            PRODUCT_LIST.append({
                'Product_ID': pid,
                'Product_Name': pname,
                'Category': cat,
                'Sub_Category': subcat,
                'Unit_Price': base_price,
                'Base_Margin': margin
            })
            prod_counter += 1

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 6, 30)
date_delta = (end_date - start_date).days

rows = []

for i in range(1, NUM_ROWS + 1):
    order_id = f"ORD-202{random.choice([2, 3, 4])}-{10000 + i}"
    
    # Date generation
    random_days = random.randint(0, date_delta)
    order_dt = start_date + timedelta(days=random_days)
    order_date_str = order_dt.strftime('%Y-%m-%d')
    
    # Customer
    cust = random.choice(CUSTOMERS)
    cust_id, cust_name = cust[0], cust[1]
    
    # Product
    prod = random.choice(PRODUCT_LIST)
    
    # Quantity
    # Weighted towards smaller quantities
    quantity = np.random.choice([1, 2, 3, 4, 5, 6, 8, 10], p=[0.35, 0.25, 0.18, 0.10, 0.05, 0.04, 0.02, 0.01])
    
    unit_price = prod['Unit_Price']
    
    # Discount logic
    # Some high sales products heavily discounted
    discount = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50], 
                                p=[0.40, 0.20, 0.15, 0.10, 0.06, 0.04, 0.025, 0.015, 0.01])
    
    # Sales calculation: Sales = Quantity * Unit_Price * (1 - Discount)
    sales = round(quantity * unit_price * (1.0 - discount), 2)
    
    # Profit calculation:
    # Cost per unit = Unit_Price * (1 - Base_Margin)
    # Freight / handling cost = $3 per order + $1 per item
    unit_cost = unit_price * (1.0 - prod['Base_Margin'])
    total_cost = (unit_cost * quantity) + (3.0 + 1.0 * quantity)
    
    # Profit = Sales - Total_Cost
    profit = round(sales - total_cost, 2)
    
    # Location
    region = np.random.choice(list(REGIONS_GEO.keys()), p=[0.25, 0.28, 0.20, 0.17, 0.10])
    state_city = random.choice(REGIONS_GEO[region])
    state, city = state_city[0], state_city[1]
    
    payment_mode = np.random.choice(PAYMENT_MODES, p=PAYMENT_WEIGHTS)
    
    # Introduce small realistic data flaws in raw data:
    # 1. Trailing/leading whitespace in Customer_Name or City (~1% of rows)
    if random.random() < 0.015:
        cust_name = f" {cust_name} "
    if random.random() < 0.01:
        city = f"{city}  "
        
    # 2. Slight date formatting variation (~0.8% of rows e.g. YYYY/MM/DD)
    if random.random() < 0.008:
        order_date_str = order_dt.strftime('%Y/%m/%d')
        
    # 3. Missing values (~0.5% in Payment_Mode and Customer_Name)
    if random.random() < 0.005:
        payment_mode = None
    if random.random() < 0.004:
        cust_name = None

    rows.append({
        'Order_ID': order_id,
        'Order_Date': order_date_str,
        'Customer_ID': cust_id,
        'Customer_Name': cust_name,
        'Product_ID': prod['Product_ID'],
        'Product_Name': prod['Product_Name'],
        'Category': prod['Category'],
        'Sub_Category': prod['Sub_Category'],
        'Quantity': int(quantity),
        'Unit_Price': unit_price,
        'Sales': sales,
        'Discount': discount,
        'Profit': profit,
        'Region': region,
        'State': state,
        'City': city,
        'Payment_Mode': payment_mode
    })

df = pd.DataFrame(rows)

os.makedirs('data', exist_ok=True)
raw_path = os.path.join('data', 'raw_data.csv')
df.to_csv(raw_path, index=False)

print(f"Successfully generated {len(df)} rows of synthetic e-commerce data.")
print(f"Saved to: {raw_path}")
print(df.info())
print("\nSample Data:")
print(df.head())
