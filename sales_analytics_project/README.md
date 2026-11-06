# Sales Analytics (Simple Base Project)

Analyses sales data: KPIs, monthly trend, revenue by product and region, and saves a dashboard chart.

## Setup
pip install -r requirements.txt

## Run
python sales_analytics.py

If `sales_data.csv` is missing, sample data is generated automatically.

## Your own data
Place a `sales_data.csv` in this folder with columns:
order_id, date, region, product, quantity, unit_price

## Output (in ./output)
- dashboard.png
- monthly_revenue.csv
- product_revenue.csv
- region_revenue.csv
