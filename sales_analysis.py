#####################################################################################
## Mini Project: Smart Sales Performance Analysis
#####################################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Data Set Loading
df = pd.read_csv( r"E:\project\Smart Sales Performance mini project\smart_sales_performance.csv"
)
print(df.head(10))

#  2.	Data cleaning & preprocessing
print("\nCleaning Data & Preprocessing...")
print(df.head())
print(df.tail())
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.drop_duplicates(inplace=True))
print(df.columns)
print(df.shape)
print(df.nunique())
print(df.dtypes)


#3.	Feature engineering (Revenue, Month, Quarter)

# Revenue Calculation
print("\nCalculating Revenue...")

df['Net Revenue'] = df['Units_Sold'] * df['Unit_Price_USD'] * (1 - df['Discount_Pct'] / 100)
print("\nData after Revenue Calculation:")
print(df.head())

#Exploring the data Analysis
print("\nExploring the data Analysis:")
print("Sum:", df['Net Revenue'].sum())
print("Mean:", df['Net Revenue'].mean())
print("Max:", df['Net Revenue'].max())
print("Min:", df['Net Revenue'].min())
print("Median:", df['Net Revenue'].median())
print("Standard Deviation:", df['Net Revenue'].std())
print("\nData after Revenue Calculation:")
print(df.head())


# Convert Month to Quarter
print("\nConverting Month to Quarter...")
#Convert Date
df['Date'] = pd.to_datetime(df['Date'])

#Create Month Column
df['Month'] = df['Date'].dt.month_name()

#Create Month Column number
df['Month_Num'] = df['Date'].dt.month

#Create Year Column
df['Year'] = df['Date'].dt.year

#Create Quarter Column
df['Quarter'] = df['Date'].dt.quarter

# Create Year-Month column
df["Year_Month"] = df["Date"].dt.to_period("M").astype(str)

# Create Year-Quarter column
df["Year_Quarter"] = df["Date"].dt.to_period("Q").astype(str)

print("\nData after Feature Engineering:")
print(df.head())


#4. Exploratory Data Analysis (EDA)
print("\nExploratory Data Analysis (EDA)...")

#Revenue by Region
#-------------------1 Bar Chart-------------------
region = df.groupby("Region")['Net Revenue'].sum()
region.plot(kind='bar', color='skyblue')
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Total Revenue (USD)")
plt.show()


#------------------ 2 Line Chart-------------------
#Monthly Sales Trend
monthly_sales = df.groupby("Month")['Net Revenue'].sum()
monthly_sales.plot(kind='line', marker='o', color='green')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue (USD)")
plt.show()

#-------------------3 Heatmap-------------------
#Heatmap: Revenue by Product Category and Region
pivot_table = df.pivot_table(values='Net Revenue', index='Product_Category', columns='Region', aggfunc='sum')
sns.heatmap(pivot_table, annot=True, fmt=".0f")
plt.title("Revenue by Product Category and Region")
plt.xlabel("Region")
plt.ylabel("Product Category")
plt.show()

#-------------------4 pie Chart-------------------
#pie Chart: Revenue Distribution by Product Category
category_revenue = df.groupby("Product_Category")['Net Revenue'].sum()
category_revenue.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='Set3')
plt.title("Revenue Distribution by Product Category")
plt.ylabel("")
plt.show()


# Top Products:

top=df.groupby("Product_Category")["Net Revenue"].sum().sort_values(ascending=False).head(10)

top.plot(kind="bar")
plt.title("Top Products by Revenue")
plt.xlabel("Product Category")
plt.ylabel("Total Revenue (USD)")
plt.show()

# Region Wise Sales:

region_sales=df.groupby("Region")["Net Revenue"].sum()
region_sales.plot(kind="bar")
plt.title("Region Wise Sales")
plt.xlabel("Region")
plt.ylabel("Total_Revenue_USD")
plt.show()

#5.	Pattern detection (seasonality, growth trends)

yearly_sales = df.groupby('Year')['Net Revenue'].sum().reset_index()
sns.lineplot(x='Year', y='Net Revenue', data=yearly_sales, marker='o')
plt.title("Yearly Growth Trend")
plt.show()

#6.	Sales forecasting using ML

# Aggregate monthly revenue
monthly_sales = df.groupby('Year_Month')['Net Revenue'].sum().reset_index()

# Create time index
monthly_sales['Time_Index'] = np.arange(len(monthly_sales))

# Features and target
X = monthly_sales[['Time_Index']]
y = monthly_sales['Net Revenue']

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict historical sales
monthly_sales['Predicted_Sales'] = model.predict(X)

# Forecast next 12 months
future_index = np.arange(len(monthly_sales), len(monthly_sales) + 12).reshape(-1, 1)
future_sales = model.predict(future_index)

# Create future dates
last_date = pd.to_datetime(monthly_sales['Year_Month'].iloc[-1])
future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=12, freq='MS')

forecast_df = pd.DataFrame({'Date': future_dates, 'Forecasted_Sales': future_sales})

# Plot
plt.figure(figsize=(12,6))
plt.plot(monthly_sales['Time_Index'], monthly_sales['Net Revenue'], label='Actual Sales', marker='o')
plt.plot(monthly_sales['Time_Index'], monthly_sales['Predicted_Sales'], label='Predicted Sales', linestyle='--')
plt.plot(np.arange(len(monthly_sales), len(monthly_sales) + 12), future_sales, label='Forecasted Sales', marker='o')
plt.title("Actual vs Predicted and Forecasted Sales")
plt.xlabel("Time Index")
plt.ylabel("Revenue (USD)")
plt.legend()
plt.grid(True)
plt.show()

