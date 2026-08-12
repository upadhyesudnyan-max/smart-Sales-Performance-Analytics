# 📊 Smart Sales Performance Analysis

A mini data analytics project that cleans, explores, and forecasts sales performance data using **Python**, **Pandas**, **Seaborn/Matplotlib**, **Scikit-learn**, and **MySQL**.

The project takes raw sales transaction data, engineers key business metrics (revenue, quarter, month), visualizes trends across regions and product categories, and builds a simple linear regression model to forecast future sales. It also includes a script to load the cleaned dataset into a MySQL database for persistent storage and further querying.

---

## 🗂️ Project Structure

```
├── sales_analysis.py     # Data cleaning, EDA, feature engineering, and ML forecasting
├── sql.py                # Loads CSV data into a MySQL database
└── README.md
```

---

## ✨ Features

### 1. Data Cleaning & Preprocessing
- Loads raw CSV sales data
- Inspects structure (`.info()`, `.describe()`, `.dtypes`)
- Checks and removes duplicate records
- Reports null values and unique counts per column

### 2. Feature Engineering
- **Net Revenue** = `Units_Sold × Unit_Price_USD × (1 - Discount_Pct / 100)`
- Date-derived features: `Month`, `Month_Num`, `Year`, `Quarter`
- Aggregation-ready periods: `Year_Month`, `Year_Quarter`

### 3. Exploratory Data Analysis (EDA)
Visualizations generated with Matplotlib & Seaborn:
- 📊 Revenue by Region (bar chart)
- 📈 Monthly Sales Trend (line chart)
- 🔥 Revenue Heatmap by Product Category × Region
- 🥧 Revenue Distribution by Product Category (pie chart)
- 🏆 Top Product Categories by Revenue
- 🌍 Region-wise Sales Comparison
- 📉 Yearly Growth Trend

### 4. Pattern Detection
- Identifies seasonality and growth trends across years and months

### 5. Sales Forecasting (Machine Learning)
- Aggregates revenue by month
- Trains a **Linear Regression** model on a time-index feature
- Predicts historical sales and forecasts the **next 12 months**
- Plots actual vs. predicted vs. forecasted revenue

### 6. MySQL Integration (`sql.py`)
- Connects to a local MySQL server
- Creates the `smart_sales_analytics` database and a `sales` table (if not present)
- Inserts cleaned sales records with conflict handling (`ON DUPLICATE KEY UPDATE`)

---

## 🛠️ Tech Stack

| Category            | Tools                             |
|---------------------|------------------------------------|
| Language             | Python 3                          |
| Data Handling         | Pandas, NumPy                     |
| Visualization         | Matplotlib, Seaborn               |
| Machine Learning       | Scikit-learn (Linear Regression)  |
| Database               | MySQL (via `mysql.connector`)    |

---

## 📦 Requirements

Install dependencies:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn mysql-connector-python
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/smart-sales-performance-analysis.git
cd smart-sales-performance-analysis
```

### 2. Add the dataset
Place your `smart_sales_performance.csv` file in a known location and update the `CSV_PATH` variable in both scripts:

```python
CSV_PATH = r"path/to/your/smart_sales_performance.csv"
```

### 3. Run the analysis
```bash
python sales_analysis.py
```
This will print cleaning/EDA summaries to the console and open a series of charts.

### 4. (Optional) Load data into MySQL
Update your MySQL credentials in `sql.py`:

```python
DB_CONFIG_NO_DB = dict(
    host="localhost",
    user="root",
    password="your_password",
)
```

Then run:
```bash
python sql.py
```
This creates the `smart_sales_analytics` database, a `sales` table, and loads all records from the CSV.

---

## 📄 Expected Dataset Columns

The scripts assume the source CSV includes (at minimum) the following columns:

`Order_ID`, `Date`, `Sales_Rep`, `Region`, `Customer_Segment`, `Product_Category`, `Product_Name`, `Units_Sold`, `Unit_Price_USD`, `Discount_Pct`, `Total_Revenue_USD`, `Cost_of_Goods_USD`, `Profit_USD`, `Pipeline_Stage`, `Lead_Conversion_Days`, `CSAT_Score`

> ⚠️ Note: Column names are case- and spelling-sensitive — ensure your CSV headers match exactly, or update the scripts accordingly.

---

## 📈 Sample Outputs

- Revenue breakdown by region and product category
- Monthly and yearly sales trend charts
- A 12-month sales forecast plotted against historical actuals

---

## 🔮 Future Improvements

- Replace Linear Regression with a time-series model (e.g., ARIMA, Prophet) for more robust forecasting
- Add a Streamlit/Dash dashboard for interactive exploration
- Parameterize file paths and DB credentials via a `.env` / config file instead of hardcoding
- Add unit tests for the data cleaning and feature engineering steps

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
