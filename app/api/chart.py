# # app/api/chart.py

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from app.services.file_handler import get_dataframe
# import pandas as pd

# router = APIRouter()

# # Define a request model to get data from the frontend
# class ChartRequest(BaseModel):
#     metric: str
#     type: str

# @router.post("/chart")
# async def chart(req: ChartRequest):
#     """
#     Returns { labels, values } for a requested metric and chart type.
#     """
#     df = get_dataframe()
#     if df is None:
#         raise HTTPException(status_code=400, detail="No data available. Upload a file first.")

#     metric = req.metric
#     chart_type = req.type.lower()

#     if metric not in df.columns:
#         raise HTTPException(status_code=400, detail=f"Metric '{metric}' not found in data.")

#     # X-axis selection: Use 'Date' if available, otherwise use index
#     if "Date" in df.columns:
#         # Try to convert to string for consistent labeling
#         labels = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d').tolist()
#     else:
#         labels = list(range(1, len(df) + 1))

#     # Y-axis data
#     values = pd.to_numeric(df[metric], errors='coerce').fillna(0).tolist()
    
#     # You can add logic here for different chart types if needed in the future
#     # For now, we return labels and values which works for both line and bar.

#     return {
#         "status": "success",
#         "labels": labels,
#         "values": values
#     }


# app/api/chart.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.file_handler import get_dataframe
import pandas as pd

router = APIRouter()

class ChartRequest(BaseModel):
    metric: str
    type: str # Hum type ko abhi bhi le rahe hain, lekin logic metric par depend karega

@router.post("/chart")
async def chart(req: ChartRequest):
    df = get_dataframe()
    if df is None:
        raise HTTPException(status_code=400, detail="No data available. Upload a file first.")

    metric = req.metric

    if metric not in df.columns:
        raise HTTPException(status_code=400, detail=f"Metric '{metric}' not found in data.")

    # --- KEY CHANGE: YAHAN HUM DATA TYPE CHECK KAR RAHE HAIN ---
    
    # Agar column numeric hai, toh purana logic istemal karein (time series/value trend)
    if pd.api.types.is_numeric_dtype(df[metric]):
        if "Date" in df.columns:
            labels = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d').tolist()
        else:
            labels = list(range(1, len(df) + 1))
        
        values = pd.to_numeric(df[metric], errors='coerce').fillna(0).tolist()

    # Agar column categorical (text) hai, toh uski har value ki ginati karein
    else:
        counts = df[metric].value_counts()
        labels = counts.index.tolist()
        values = counts.values.tolist()

    return {
        "status": "success",
        "labels": labels,
        "values": values
    }


