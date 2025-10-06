from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

if os.path.exists(CSV_FILE):
 df = pd.read_csv(CSV_FILE)
elif DATAFRAME is not None:
 df = DATAFRAME


if df is None or df.empty:
 raise HTTPException(status_code=400, detail="No data available. Upload a file first.")


out = {
"total_sales": float(pd.to_numeric(df.get("Sales", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()),
"avg_profit": float(pd.to_numeric(df.get("Profit", pd.Series(dtype=float)), errors="coerce").mean() or 0),
"max_profit": float(pd.to_numeric(df.get("Profit", pd.Series(dtype=float)), errors="coerce").max() or 0),
"min_profit": float(pd.to_numeric(df.get("Profit", pd.Series(dtype=float)), errors="coerce").min() or 0),
}
return out


@router.post("/chart")
async def chart(req: ChartRequest):
"""
Return a base64 PNG of the requested metric as a line/bar plot.
X-axis will be 'Date' if present, else the DataFrame index.
"""
# Prefer the saved CSV so a refresh still works without re-upload
if os.path.exists(CSV_FILE):
 df = pd.read_csv(CSV_FILE)
elif DATAFRAME is not None:
 df = DATAFRAME.copy()
else:
 raise HTTPException(status_code=400, detail="No data available. Upload a file first.")


metric = req.metric
chart_type = req.type.lower()


if metric not in df.columns:
 raise HTTPException(status_code=400, detail=f"Metric '{metric}' not found in data.")


# X-axis selection
x = None
if "Date" in df.columns:
# Try to parse for nicer tick rendering; fallback silently
try:
x = pd.to_datetime(df["Date"]) # converts if possible
except Exception:
x = df["Date"].astype(str)
else:
x = df.index # fallback


y = pd.to_numeric(df[metric], errors="coerce")


plt.figure(figsize=(10, 5))
if chart_type == "line":
 plt.plot(x, y, marker="o")
elif chart_type == "bar":
 plt.bar(x, y)
else:
 raise HTTPException(status_code=400, detail="Invalid chart type. Use 'line' or 'bar'.")


plt.title(f"{metric} Over Time")
plt.xlabel("Date" if "Date" in df.columns else "Index")
plt.ylabel(metric)
plt.xticks(rotation=45)
plt.tight_layout()


buf = BytesIO()
plt.savefig(buf, format="png")
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode("utf-8")
plt.close()


return {"image": f"data:image/png;base64,{img_base64}"}