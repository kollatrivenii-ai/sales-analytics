"""
Sales Analytics - Simple Base Project
-------------------------------------
Steps:
  1. Load data (creates sample data if sales_data.csv is missing)
  2. Clean data
  3. Calculate KPIs
  4. Analyse by month, product, region
  5. Save charts + summary tables to ./output

Required columns in your own CSV:
  order_id, date, region, product, quantity, unit_price

Run:  pip install pandas numpy matplotlib
      python sales_analytics.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # works without a display
import matplotlib.pyplot as plt

DATA_FILE = "sales_data.csv"
OUT_DIR = "output"


# ---------------------------------------------------------------- 1. LOAD
def generate_sample_data(path, n=1000, seed=42):
    """Create a random sales dataset for demo purposes."""
    rng = np.random.default_rng(seed)
    prices = {"Laptop": 55000, "Phone": 25000, "Tablet": 18000,
              "Smartwatch": 8000, "Headphones": 3000, "Keyboard": 1500}
    products = rng.choice(list(prices), n)
    df = pd.DataFrame({
        "order_id": np.arange(1001, 1001 + n),
        "date": pd.to_datetime("2025-01-01")
                + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
        "region": rng.choice(["North", "South", "East", "West"], n),
        "product": products,
        "quantity": rng.integers(1, 6, n),
        "unit_price": [prices[p] for p in products],
    })
    df.to_csv(path, index=False)
    print(f"Sample data created: {path}")


def load_data(path):
    if not os.path.exists(path):
        generate_sample_data(path)
    return pd.read_csv(path)


# --------------------------------------------------------------- 2. CLEAN
def clean_data(df):
    df = df.drop_duplicates()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "product", "region", "quantity", "unit_price"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)].copy()
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


# ---------------------------------------------------------------- 3. KPIs
def calculate_kpis(df):
    return {
        "Total Revenue (INR)": df["revenue"].sum(),
        "Total Orders": df["order_id"].nunique(),
        "Units Sold": df["quantity"].sum(),
        "Avg Order Value (INR)": df["revenue"].sum() / df["order_id"].nunique(),
    }


# ------------------------------------------------------------ 4. ANALYSE
def analyse(df):
    monthly = df.groupby("month")["revenue"].sum()
    by_product = df.groupby("product")["revenue"].sum().sort_values(ascending=False)
    by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    return monthly, by_product, by_region


# ------------------------------------------------------------- 5. CHARTS
def make_dashboard(kpis, monthly, by_product, by_region, path):
    fig, ax = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Sales Analytics Dashboard", fontsize=18, fontweight="bold")

    # KPI panel
    ax[0, 0].axis("off")
    text = "\n\n".join(f"{k}:  {v:,.0f}" for k, v in kpis.items())
    ax[0, 0].text(0.05, 0.5, text, fontsize=14, va="center",
                  bbox=dict(boxstyle="round", facecolor="#eef3fb"))
    ax[0, 0].set_title("Key Metrics")

    # Monthly trend
    ax[0, 1].plot(monthly.index, monthly.values, marker="o", color="#2a6fdb")
    ax[0, 1].set_title("Monthly Revenue")
    ax[0, 1].tick_params(axis="x", rotation=60)

    # Product revenue
    ax[1, 0].barh(by_product.index[::-1], by_product.values[::-1], color="#2a9d8f")
    ax[1, 0].set_title("Revenue by Product")

    # Region share
    ax[1, 1].pie(by_region.values, labels=by_region.index,
                 autopct="%1.1f%%", startangle=90)
    ax[1, 1].set_title("Revenue Share by Region")

    plt.tight_layout()
    plt.savefig(path, dpi=130)
    plt.close()


# ------------------------------------------------------------------ MAIN
def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    df = clean_data(load_data(DATA_FILE))
    kpis = calculate_kpis(df)
    monthly, by_product, by_region = analyse(df)

    print("\n=== KEY METRICS ===")
    for k, v in kpis.items():
        print(f"{k:<24}: {v:,.0f}")
    print("\n=== TOP PRODUCTS ===")
    print(by_product.head().apply(lambda x: f"{x:,.0f}").to_string())
    print("\n=== REGIONS ===")
    print(by_region.apply(lambda x: f"{x:,.0f}").to_string())
    print(f"\nBest month: {monthly.idxmax()} ({monthly.max():,.0f})")

    monthly.to_csv(f"{OUT_DIR}/monthly_revenue.csv")
    by_product.to_csv(f"{OUT_DIR}/product_revenue.csv")
    by_region.to_csv(f"{OUT_DIR}/region_revenue.csv")
    make_dashboard(kpis, monthly, by_product, by_region,
                   f"{OUT_DIR}/dashboard.png")
    print(f"\nSaved results and dashboard.png in ./{OUT_DIR}/")


if __name__ == "__main__":
    main()
