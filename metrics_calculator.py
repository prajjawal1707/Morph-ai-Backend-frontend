import pandas as pd
import numpy as np

# -----------------------------
# Load Data from CSV
# -----------------------------
df = pd.read_csv("Details.csv")

# -----------------------------
# Safe Date Handling
# -----------------------------
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Quarter"] = df["Date"].dt.quarter
else:
    print("⚠️ No 'Date' column found → Skipping time intelligence calculations.")

# -----------------------------
# BASIC CALCULATIONS
# -----------------------------
if "Sales" in df.columns:
    print("\n--- BASIC METRICS ---")
    print("Sum of Sales:", df["Sales"].sum())
    print("Average Sales:", df["Sales"].mean())
    print("Min Sales:", df["Sales"].min(), " | Max Sales:", df["Sales"].max())

if "Customers" in df.columns:
    print("Distinct Customers:", df["Customers"].nunique())

# -----------------------------
# TIME INTELLIGENCE
# -----------------------------
if "Date" in df.columns and "Sales" in df.columns:
    latest_month = df["Month"].max()
    latest_quarter = df["Quarter"].max()
    latest_year = df["Year"].max()

    mtd = df[df["Month"] == latest_month]["Sales"].sum()
    qtd = df[df["Quarter"] == latest_quarter]["Sales"].sum()
    ytd = df[df["Year"] == latest_year]["Sales"].sum()
    previous_year_sales = df[df["Year"] == latest_year - 1]["Sales"].sum()

    yoy_growth = ((ytd - previous_year_sales) / previous_year_sales * 100) if previous_year_sales else None
    mom_growth = ((df.iloc[-1]["Sales"] - df.iloc[-2]["Sales"]) / df.iloc[-2]["Sales"] * 100) if len(df) > 1 else None

    df["Rolling_Avg_3M"] = df["Sales"].rolling(3).mean()

    start_value = df.iloc[0]["Sales"]
    end_value = df.iloc[-1]["Sales"]
    n_years = (df["Date"].iloc[-1] - df["Date"].iloc[0]).days / 365
    cagr = ((end_value / start_value) ** (1/n_years) - 1) * 100 if n_years > 0 else None

    print("\n--- TIME INTELLIGENCE ---")
    print("MTD:", mtd, "| QTD:", qtd, "| YTD:", ytd)
    print("Previous Year Sales:", previous_year_sales)
    print("YOY Growth %:", yoy_growth)
    print("MOM Growth %:", mom_growth)
    print("CAGR %:", cagr)

# -----------------------------
# RATIOS & PERCENTAGES
# -----------------------------
if all(col in df.columns for col in ["Profit","Sales"]):
    df["Profit_Margin_%"] = df["Profit"] / df["Sales"] * 100
if all(col in df.columns for col in ["Sales","Cost"]):
    df["Gross_Margin_%"] = (df["Sales"] - df["Cost"]) / df["Sales"] * 100
if all(col in df.columns for col in ["Conversions","Customers"]):
    df["Conversion_Rate_%"] = df["Conversions"] / df["Customers"] * 100
if all(col in df.columns for col in ["Retained_Customers","Customers"]):
    df["Retention_Rate_%"] = df["Retained_Customers"] / df["Customers"] * 100
    df["Churn_Rate_%"] = (1 - df["Retention_Rate_%"] / 100) * 100
if "Sales" in df.columns:
    df["Contribution_%"] = df["Sales"] / df["Sales"].sum() * 100

# -----------------------------
# OPERATIONAL METRICS
# -----------------------------
if all(col in df.columns for col in ["Resolution_Time_Hours","Resolved_Tickets"]):
    df["Avg_Resolution_Time"] = df["Resolution_Time_Hours"] / df["Resolved_Tickets"]
if all(col in df.columns for col in ["Employee_Worked_Hours","Employee_Available_Hours"]):
    df["Utilization_%"] = df["Employee_Worked_Hours"] / df["Employee_Available_Hours"] * 100
if all(col in df.columns for col in ["Stock_Sold","Stock_Avg"]):
    df["Stock_Turnover"] = df["Stock_Sold"] / df["Stock_Avg"]
if all(col in df.columns for col in ["On_Time_Delivery","Total_Delivery"]):
    df["On_Time_Delivery_%"] = df["On_Time_Delivery"] / df["Total_Delivery"] * 100

# -----------------------------
# CUSTOMER & MARKETING METRICS
# -----------------------------
if "Customer_Lifetime_Revenue" in df.columns:
    df["CLV"] = df["Customer_Lifetime_Revenue"]
if "Customer_Acquisition_Cost" in df.columns:
    df["CAC"] = df["Customer_Acquisition_Cost"]
if all(col in df.columns for col in ["Revenue","Marketing_Spend"]):
    df["ROI_%"] = (df["Revenue"] - df["Marketing_Spend"]) / df["Marketing_Spend"] * 100
if all(col in df.columns for col in ["Converted_Leads","Leads"]):
    df["Lead_Conversion_Rate_%"] = df["Converted_Leads"] / df["Leads"] * 100

# -----------------------------
# FINANCIAL METRICS
# -----------------------------
if all(col in df.columns for col in ["Net_Profit","Revenue"]):
    df["Net_Profit_%"] = df["Net_Profit"] / df["Revenue"] * 100
if all(col in df.columns for col in ["Operating_Income","Revenue"]):
    df["Operating_Margin_%"] = df["Operating_Income"] / df["Revenue"] * 100
if all(col in df.columns for col in ["Working_Capital_CurrentAssets","Working_Capital_CurrentLiabilities"]):
    df["Working_Capital"] = df["Working_Capital_CurrentAssets"] - df["Working_Capital_CurrentLiabilities"]
if all(col in df.columns for col in ["Total_Debt","Total_Equity"]):
    df["Debt_to_Equity"] = df["Total_Debt"] / df["Total_Equity"]

# -----------------------------
# SAVE RESULTS
# -----------------------------
df.to_csv("calculated_metrics.csv", index=False)
print("\n✅ Metrics calculated successfully. Saved to 'calculated_metrics.csv'")
