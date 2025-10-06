# from fastapi import APIRouter
# from app.services.filehandler import get_dataframe

# router = APIRouter(prefix="/api", tags=["summary"])

# @router.get("/summary")
# async def get_summary():
#     df = get_dataframe()
#     if df is None:
#         return {"error": "No file uploaded"}

#     summary = {
#         "rows": len(df),
#         "columns": list(df.columns),
#         "dtypes": df.dtypes.astype(str).to_dict(),
#     }
#     return summary












from fastapi import APIRouter
from app.services.file_handler import get_dataframe

router = APIRouter(prefix="/api", tags=["summary"])

@router.get("/summary")
async def get_summary():
    df = get_dataframe()
    if df is None:
        return {"error": "No file uploaded"}
    result = {}
    if "Sales" in df.columns:
        result["total_sales"] = float(df["Sales"].sum())
    if "Profit" in df.columns:
        result["avg_profit"] = float(df["Profit"].mean())
        result["max_profit"] = float(df["Profit"].max())
        result["min_profit"] = float(df["Profit"].min())
    result["rows"] = len(df)
    result["columns"] = list(df.columns)
    return result
