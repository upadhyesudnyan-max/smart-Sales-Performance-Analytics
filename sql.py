

import pandas as pd
import mysql.connector

# ---- Config ----------------------------------------------------------
CSV_PATH =  r"E:\project\Smart Sales Performance mini project\smart_sales_performance.csv"  # <-- update to your actual CSV path
DB_NAME = "smart_sales_analytics"

DB_CONFIG_NO_DB = dict(
    host="localhost",
    user="root",
    password="system",
)

# ---- 1. Read CSV -------------------------------------------------------
df = pd.read_csv(CSV_PATH)
print("CSV data loaded successfully!")
print(df.head())
print("Total rows:", len(df))

# ---- 2. Connect to MySQL server (no database selected yet) --------------
conn = mysql.connector.connect(**DB_CONFIG_NO_DB)
cursor = conn.cursor()
print("MySQL server connected successfully!")

# ---- 3. Create database if it doesn't exist ------------------------------
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
conn.commit()
print(f"Database '{DB_NAME}' ready.")

# Switch to the database
cursor.execute(f"USE {DB_NAME}")

# ---- 4. Create table (matches actual CSV columns) -----------------------
create_table_sql = """
CREATE TABLE IF NOT EXISTS sales (
    Order_ID              VARCHAR(20) PRIMARY KEY,
    Order_Date            DATE,
    Sales_Rep             VARCHAR(100),
    Region                VARCHAR(50),
    Customer_Segment      VARCHAR(50),
    Product_Category      VARCHAR(50),
    Product_Name          VARCHAR(100),
    Units_Sold            INT,
    Unit_Price_USD        DECIMAL(12, 2),
    Discount_Pct          DECIMAL(5, 4),
    Total_Revenue_USD     DECIMAL(14, 2),
    Cost_of_Goods_USD     DECIMAL(14, 2),
    Profit_USD            DECIMAL(14, 2),
    Pipeline_Stage        VARCHAR(30),
    Lead_Conversion_Days  INT,
    CSAT_Score            DECIMAL(3, 1)
)
"""
cursor.execute(create_table_sql)
conn.commit()
print("Table 'sales' ready.")

# ---- 5. Insert data ------------------------------------------------------
insert_sql = """
INSERT INTO sales (
    Order_ID, Order_Date, Sales_Rep, Region, Customer_Segment,
    Product_Category, Product_Name, Units_Sold, Unit_Price_USD,
    Discount_Pct, Total_Revenue_USD, Cost_of_Goods_USD, Profit_USD,
    Pipeline_Stage, Lead_Conversion_Days, CSAT_Score
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE Order_ID = Order_ID
"""

data = []
for _, row in df.iterrows():
    data.append((
        row["Order_ID"],
        pd.to_datetime(row["Date"]).date(),
        row["Sales_Rep"],
        row["Region"],
        row["Customer_Segment"],
        row["Product_Category"],
        row["Product_Name"],
        int(row["Units_Sold"]),
        float(row["Unit_Price_USD"]),
        float(row["Discount_Pct"]),
        float(row["Total_Revenue_USD"]),
        float(row["Cost_of_Goods_USD"]),
        float(row["Profit_USD"]),
        row["Pipeline_Stage"],
        int(row["Lead_Conversion_Days"]),
        float(row["CSAT_Score"]),
    ))

cursor.executemany(insert_sql, data)
conn.commit()
print("Data inserted successfully!")
print("Rows inserted:", cursor.rowcount)

cursor.close()
conn.close()
print("MySQL connection closed.")