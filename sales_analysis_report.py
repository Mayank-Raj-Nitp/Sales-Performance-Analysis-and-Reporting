import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# ---  DATA GENERATION (Simulating Data Collection/Loading) ---
# Simulating a moderately large dataset of sales transactions
np.random.seed(42)
data_size = 5000

products = ['Laptop', 'Smartphone', 'Monitor', 'Keyboard', 'Mouse']
regions = ['North', 'South', 'East', 'West']

start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 12, 31)

dates = [start_date + datetime.timedelta(days=np.random.randint(0, (end_date - start_date).days)) 
         for _ in range(data_size)]

df = pd.DataFrame({
    'OrderDate': dates,
    'Product': np.random.choice(products, data_size, p=[0.25, 0.35, 0.15, 0.15, 0.10]),
    'Region': np.random.choice(regions, data_size),
    'Quantity': np.random.randint(1, 5, data_size),
    'UnitPrice': np.round(np.random.uniform(20, 1500, data_size), 2)
})

df['Revenue'] = df['Quantity'] * df['UnitPrice']
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

print(f"--- Data Loaded: {len(df)} transactions ---")

# --- DATA ANALYSIS & TREND IDENTIFICATION ---

# A. Monthly Sales Trend
df['Month'] = df['OrderDate'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Revenue'].sum().reset_index()

# B. Top 5 Products
product_sales = df.groupby('Product')['Revenue'].sum().nlargest(5).reset_index()

# C. Regional Performance
regional_sales = df.groupby('Region')['Revenue'].sum().reset_index()

# --- 3. VISUALIZATION AND REPORTING  ---

sns.set_style("whitegrid")
fig, axes = plt.subplots(3, 1, figsize=(10, 15))
plt.suptitle('E-Commerce Sales Performance Report', fontsize=16, y=1.02)

# Chart 1: Monthly Sales Trend (Time-series analysis)
monthly_sales['Month'] = monthly_sales['Month'].astype(str)
sns.lineplot(x='Month', y='Revenue', data=monthly_sales, marker='o', ax=axes[0], color='skyblue')
axes[0].set_title('Trend 1: Monthly Revenue Over Time (Identifying Seasonal Patterns)')
axes[0].tick_params(axis='x', rotation=45)
axes[0].set_ylabel('Total Revenue ($)')
axes[0].set_xlabel('')

# Chart 2: Product Performance (Identifying top drivers)
sns.barplot(x='Revenue', y='Product', data=product_sales, palette='viridis', ax=axes[1])
axes[1].set_title('Trend 2: Top 5 Products by Total Revenue')
axes[1].set_xlabel('Total Revenue ($)')
axes[1].set_ylabel('')

# Chart 3: Regional Analysis (Identifying geographical patterns)
sns.pie(regional_sales['Revenue'], labels=regional_sales['Region'], autopct='%1.1f%%', startangle=90, ax=axes[2], colors=sns.color_palette('pastel'))
axes[2].set_title('Trend 3: Revenue Distribution by Region')
axes[2].set_ylabel('')

plt.tight_layout()
plt.show()

# ---  EXECUTIVE SUMMARY (Simulating business decision insight) ---
print("\n" + "="*50)
print("EXECUTIVE DATA SUMMARY")
print("="*50)
print(f"Total Revenue Generated: ${df['Revenue'].sum():,.2f}")
print(f"Highest Revenue Month: {monthly_sales.iloc[-1]['Month']} (Identified a recent peak)")
print(f"Top Performing Product: {product_sales.iloc[0]['Product']} (Key growth driver)")
print(f"Recommendation: Allocate additional marketing budget to the {product_sales.iloc[0]['Product']} and target the {regional_sales.iloc[0]['Region']} region.")
print("="*50)

