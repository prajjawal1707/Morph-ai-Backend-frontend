
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import os

# -----------------------------
# Load CSV
# -----------------------------
csv_file = "calculated_metrics.csv"  # make sure this file exists in the same folder
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"{csv_file} not found!")

df = pd.read_csv(csv_file)

# Convert Date column to datetime if exists
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# Define metrics
# -----------------------------
line_metrics = ["Sales", "Profit", "Net_Profit_%", "Operating_Margin_%"]
bar_metrics = ["Profit_Margin_%","Gross_Margin_%","Conversion_Rate_%","Retention_Rate_%","Churn_Rate_%"]
hist_metrics = ["Daily_Sales","Avg_Resolution_Time","Utilization_%","Stock_Turnover","On_Time_Delivery_%"]
box_metrics = ["Sales", "Profit", "Net_Profit_%", "Daily_Sales"]
scatter_pairs = [("Sales","Profit"), ("CLV","CAC")]

# Total plots for layout
total_plots = len(line_metrics) + len(bar_metrics) + len(hist_metrics) + len(box_metrics) + len(scatter_pairs) + 1
cols = 3
rows = math.ceil(total_plots / cols)

# -----------------------------
# Create dashboard figure
# -----------------------------
fig, axes = plt.subplots(rows, cols, figsize=(20, rows*5))
axes = axes.flatten()
plot_idx = 0

# LINE CHARTS
for col_name in line_metrics:
    if col_name in df.columns and "Date" in df.columns:
        axes[plot_idx].plot(df["Date"], df[col_name], marker='o', color='blue')
        axes[plot_idx].set_title(col_name)
        axes[plot_idx].set_xlabel("Date")
        axes[plot_idx].set_ylabel(col_name)
        axes[plot_idx].grid(True)
        plot_idx += 1

# BAR CHARTS
for col_name in bar_metrics:
    if col_name in df.columns and "Date" in df.columns:
        sns.barplot(x=df["Date"], y=df[col_name], ax=axes[plot_idx], palette="viridis")
        axes[plot_idx].set_title(col_name)
        axes[plot_idx].set_xlabel("Date")
        axes[plot_idx].set_ylabel(col_name)
        axes[plot_idx].tick_params(axis='x', rotation=45)
        plot_idx += 1

# HISTOGRAMS
for col_name in hist_metrics:
    if col_name in df.columns:
        sns.histplot(df[col_name], bins=10, kde=True, ax=axes[plot_idx], color='skyblue')
        axes[plot_idx].set_title(f"Distribution of {col_name}")
        axes[plot_idx].set_xlabel(col_name)
        axes[plot_idx].set_ylabel("Frequency")
        plot_idx += 1

# BOX PLOTS
for col_name in box_metrics:
    if col_name in df.columns:
        sns.boxplot(x=df[col_name], ax=axes[plot_idx], color='lightgreen')
        axes[plot_idx].set_title(f"Boxplot of {col_name}")
        plot_idx += 1

# SCATTER PLOTS
for x_col, y_col in scatter_pairs:
    if x_col in df.columns and y_col in df.columns:
        sns.scatterplot(x=df[x_col], y=df[y_col], ax=axes[plot_idx])
        sns.regplot(x=df[x_col], y=df[y_col], scatter=False, ax=axes[plot_idx], color='red')
        axes[plot_idx].set_title(f"{y_col} vs {x_col}")
        plot_idx += 1

# CUMULATIVE + ROLLING SALES
if "Sales" in df.columns and "Date" in df.columns:
    axes[plot_idx].plot(df["Date"], df["Sales"].cumsum(), marker='o', label="Cumulative Sales")
    axes[plot_idx].plot(df["Date"], df["Sales"].rolling(3).mean(), marker='x', label="3M Rolling Avg")
    axes[plot_idx].set_title("Cumulative & Rolling Avg Sales")
    axes[plot_idx].set_xlabel("Date")
    axes[plot_idx].set_ylabel("Sales")
    axes[plot_idx].legend()
    axes[plot_idx].grid(True)
    plot_idx += 1

# Remove unused axes
for i in range(plot_idx, len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()

# Save the dashboard PNG
os.makedirs("graphs", exist_ok=True)
plt.savefig("graphs/all_metrics_dashboard.png")
plt.show()

print(" All metrics dashboard saved as 'graphs/all_metrics_dashboard.png'")
