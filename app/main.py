# # main.py

# from fastapi import FastAPI
# from fastapi.responses import JSONResponse, FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd

# # Routers
# from app.api import upload, chart
# from app.services.file_handler import get_dataframe

# # FastAPI application ko initialize karein
# app = FastAPI(title="Morph-AI Backend")

# # CORS Middleware (frontend se connection ke liye zaroori)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )





# # Doosri files (upload.py, chart.py) ke routes ko jodein
# app.include_router(upload.router, prefix="/api")
# app.include_router(chart.router, prefix="/api")

# # --- YEH HAMARA FINAL /api/summary ENDPOINT HAI ---
# @app.get("/api/summary")
# def get_summary():
#     """
#     Calculates summary stats and returns categorized lists of columns
#     for smart chart selection on the frontend.
#     """
#     df = get_dataframe()
#     if df is None or df.empty:
#         return JSONResponse({"error": "No data available"}, status_code=400)
    
#     try:
#         # 1. Numeric columns ko pehchanein
#         numeric_columns = df.select_dtypes(include='number').columns.tolist()
        
#         # 2. Categorical (text) columns ko pehchanein
#         categorical_columns = []
#         for col in df.select_dtypes(include=['object', 'category']).columns:
#             # Sirf un columns ko lein jinki unique values 50 se kam ho
#             if df[col].nunique() < 50:
#                 categorical_columns.append(col)

#         # 3. Frontend ke liye data taiyaar karein
#         summary_data = {
#             "total_sales": float(pd.to_numeric(df.get("Sales"), errors='coerce').fillna(0).sum()),
#             "avg_profit": float(pd.to_numeric(df.get("Profit"), errors='coerce').fillna(0).mean()),
            
#             # Frontend ko dono tarah ke columns ki list bhejein
#             "numeric_columns": numeric_columns,
#             "categorical_columns": categorical_columns
#         }
#         return summary_data
#     except Exception as e:
#         return JSONResponse({"error": f"Error calculating summary: {str(e)}"}, status_code=500)



# @app.get("/dashboard", response_class=FileResponse)
# async def get_dashboard():
#     """
#     Serves the main HTML dashboard file.
#     """
#     return "dashboard.html"


# @app.get("/")
# def root():
#     """
#     Root endpoint to check if the server is running.
#     """
#     return {"message": "Backend running!"}







from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd


# FastAPI application ko initialize karein
app = FastAPI(title="Morph-AI Backend")
# Routers
from app.api import upload, chart
from app.services.file_handler import get_dataframe


# CORS Middleware (frontend se connection ke liye zaroori)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Doosri files (upload.py, chart.py) ke routes ko jodein
app.include_router(upload.router, prefix="/api")
app.include_router(chart.router, prefix="/api")


# --- YEH /api/summary KA SAHI AUR FINAL VERSION HAI ---
@app.get("/api/summary")
def get_summary():
    """
    Calculates summary stats and returns categorized lists of columns.
    This version is crash-proof.
    """
    df = get_dataframe()
    if df is None or df.empty:
        return JSONResponse({"error": "No data available"}, status_code=400)
    
    try:
        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        
        categorical_columns = []
        for col in df.select_dtypes(include=['object', 'category']).columns:
            if df[col].nunique() < 50:
                categorical_columns.append(col)

        # Crash-proof calculations
        total_sales = float(pd.to_numeric(df["Sales"], errors='coerce').sum()) if "Sales" in df.columns else 0
        avg_profit = float(pd.to_numeric(df["Profit"], errors='coerce').mean()) if "Profit" in df.columns else 0
        max_profit = float(pd.to_numeric(df["Profit"], errors='coerce').max()) if "Profit" in df.columns else 0
        min_profit = float(pd.to_numeric(df["Profit"], errors='coerce').min()) if "Profit" in df.columns else 0

        summary_data = {
            "total_sales": total_sales,
            "avg_profit": avg_profit,
            "max_profit": max_profit,
            "min_profit": min_profit,
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns
        }
        return summary_data
    except Exception as e:
        return JSONResponse({"error": f"Error calculating summary: {str(e)}"}, status_code=500)


# ADD THIS NEW FUNCTION
@app.get("/", response_class=FileResponse)
async def serve_dashboard():
    """
    Serves the main dashboard.html file as the root page.
    """
    return "dashboard.html"