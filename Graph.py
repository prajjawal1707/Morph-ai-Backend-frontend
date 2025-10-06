
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Load Calculated Metrics
# -----------------------------
df = pd.read_csv("calculated_metrics.csv")

# Ensure Date column exists
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])

# Create folder for saving graphs
output_folder = "graphs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# -----------------------------
# LINE CHARTS / TIME SERIES
# -----------------------------
line_columns = ["Sales", "Profit", "Net_Profit_%", "Operating_Margin_%", "Daily_Sales",
                "Avg_Resolution_Time", "Utilization_%", "Stock_Turnover", "On_Time_Delivery_%",
                "CLV", "CAC", "ROI_%", "Lead_Conversion_Rate_%"]

for col in line_columns:
    if col in df.columns and "Date" in df.columns:
        plt.figure(figsize=(10,5))
        plt.plot(df["Date"], df[col], marker='o')
        plt.title(f"{col} Over Time")
        plt.xlabel("Date")
        plt.ylabel(col)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_folder}/{col}_line.png")
        plt.close()

# -----------------------------
# AREA / STACKED AREA CHART
# -----------------------------
area_columns = ["Sales", "Profit", "Daily_Sales"]
existing_cols = [col for col in area_columns if col in df.columns and "Date" in df.columns]
if existing_cols:
    plt.figure(figsize=(10,5))
    plt.stackplot(df["Date"], df[existing_cols].T, labels=existing_cols, alpha=0.6)
    plt.title("Stacked Area Chart")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/stacked_area_chart.png")
    plt.close()

# -----------------------------
# BAR CHARTS
# -----------------------------
bar_columns = ["Profit_Margin_%","Gross_Margin_%","Conversion_Rate_%","Retention_Rate_%","Churn_Rate_%","Contribution_%"]
for col in bar_columns:
    if col in df.columns and "Date" in df.columns:
        plt.figure(figsize=(10,5))
        sns.barplot(x=df["Date"], y=df[col], palette="viridis")
        plt.title(f"{col} Over Time")
        plt.xlabel("Date")
        plt.ylabel(col)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_folder}/{col}_bar.png")
        plt.close()

# -----------------------------
# PIE / DONUT CHARTS
# -----------------------------
pie_columns = ["Contribution_%"]
for col in pie_columns:
    if col in df.columns:
        plt.figure(figsize=(7,7))
        plt.pie(df[col], labels=df.index, autopct='%1.1f%%', startangle=140)
        plt.title(f"{col} Distribution")
        plt.tight_layout()
        plt.savefig(f"{output_folder}/{col}_pie.png")
        plt.close()

# -----------------------------
# HISTOGRAMS
# -----------------------------
numeric_cols = df.select_dtypes(include='number').columns
for col in numeric_cols:
    plt.figure(figsize=(8,5))
    sns.histplot(df[col], bins=10, kde=True, color='skyblue')
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/{col}_hist.png")
    plt.close()

# -----------------------------
# BOX / VIOLIN PLOTS
# -----------------------------
for col in numeric_cols:
    plt.figure(figsize=(8,5))
    sns.boxplot(x=df[col], color='lightgreen')
    plt.title(f"Boxplot of {col}")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/{col}_box.png")
    plt.close()

    plt.figure(figsize=(8,5))
    sns.violinplot(x=df[col], color='lightblue')
    plt.title(f"Violin Plot of {col}")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/{col}_violin.png")
    plt.close()

# -----------------------------
# SCATTER PLOTS (Relationships)
# -----------------------------
scatter_pairs = [("Sales","Profit"), ("Marketing_Spend","Revenue"), ("CLV","CAC")]
for x,y in scatter_pairs:
    if x in df.columns and y in df.columns:
        plt.figure(figsize=(8,5))
        sns.scatterplot(x=df[x], y=df[y])
        sns.regplot(x=df[x], y=df[y], scatter=False, color='red')  # trendline
        plt.title(f"{y} vs {x}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.tight_layout()
        plt.savefig(f"{output_folder}/{x}_vs_{y}_scatter.png")
        plt.close()

# -----------------------------
# CORRELATION HEATMAP
# -----------------------------
if len(numeric_cols) > 1:
    plt.figure(figsize=(12,10))
    sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Between Metrics")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/correlation_heatmap.png")
    plt.close()

# -----------------------------
# PAIRPLOT
# -----------------------------
pairplot_cols = ["Sales", "Profit", "Net_Profit_%", "Operating_Margin_%"]
existing_pair_cols = [col for col in pairplot_cols if col in df.columns]
if len(existing_pair_cols) >= 2:
    sns.pairplot(df[existing_pair_cols])
    plt.savefig(f"{output_folder}/pairplot.png")
    plt.close()

# -----------------------------
# CUMULATIVE / ROLLING
# -----------------------------
if "Sales" in df.columns:
    plt.figure(figsize=(10,5))
    plt.plot(df["Date"], df["Sales"].cumsum(), marker='o', label="Cumulative Sales")
    if "Sales" in df.columns:
        plt.plot(df["Date"], df["Sales"].rolling(3).mean(), marker='x', label="3M Rolling Avg")
    plt.title("Cumulative Sales & Rolling Average")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/cumulative_rolling_sales.png")
    plt.close()

# -----------------------------
# SIMPLE FUNNEL-LIKE PLOT (Leads → Converted Leads → Customers)
# -----------------------------
if all(col in df.columns for col in ["Leads","Converted_Leads","Customers"]):
    stages = ["Leads","Converted_Leads","Customers"]
    values = [df[stage].sum() for stage in stages]
    plt.figure(figsize=(6,5))
    plt.barh(stages, values, color=['skyblue','orange','green'])
    plt.title("Funnel: Leads → Converted Leads → Customers")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/funnel_leads.png")
    plt.close()

print(f"\n All possible graphs generated and saved in the folder '{output_folder}'")
