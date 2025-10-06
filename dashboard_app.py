import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv("calculated_metrics.csv")
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])

st.title(" Metrics Dashboard")

# -----------------------------
# Line Charts
# -----------------------------
line_metrics = ["Sales", "Profit", "Net_Profit_%"]
st.header("Line Charts")
for metric in line_metrics:
    if metric in df.columns and "Date" in df.columns:
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(df["Date"], df[metric], marker='o')
        ax.set_title(metric)
        ax.set_xlabel("Date")
        ax.set_ylabel(metric)
        ax.grid(True)
        st.pyplot(fig)  # Important: display each graph individually

# -----------------------------
# Bar Charts
# -----------------------------
bar_metrics = ["Profit_Margin_%","Gross_Margin_%"]
st.header("Bar Charts")
for metric in bar_metrics:
    if metric in df.columns and "Date" in df.columns:
        fig, ax = plt.subplots(figsize=(8,4))
        sns.barplot(x=df["Date"], y=df[metric], ax=ax)
        ax.set_title(metric)
        st.pyplot(fig)
