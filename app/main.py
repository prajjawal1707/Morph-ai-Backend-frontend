#  1. IMPORTS

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import pandas as pd
from fastapi import Depends
from fastapi.responses import RedirectResponse
from app.api.auth import get_current_user # This imports your security guard
# Local application imports
from app.api import upload, chart, auth  # <-- This line now works because auth.py exists
from app.services.file_handler import get_dataframe
# =================================================================
#  2. APP INITIALIZATION & CONFIGURATION
# =================================================================
# Initialize the FastAPI application
app = FastAPI(title="Morph-AI Backend")

# Configure Jinja2 to find HTML templates in the "templates" directory
templates = Jinja2Templates(directory="templates")

# Add CORS Middleware to allow the frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

#  3. API ROUTERS

# Include routers from other files (upload.py, chart.py)
# API-specific routes (data upload, chart generation, etc.)
app.include_router(upload.router, prefix="/api")
app.include_router(chart.router, prefix="/api")
# Top-level routes for authentication (login, signup, logout)
app.include_router(auth.router) # <-- CORRECTED: The "/api" prefix is removed

#  4. CORE API ENDPOINTS

@app.get("/api/summary")
def get_summary():
    """
    Calculates summary statistics and identifies column types from the uploaded data.
    """
    df = get_dataframe()
    if df is None or df.empty:
        return JSONResponse(content={"error": "No data available to summarize."}, status_code=404)

    try:
        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        
        categorical_columns = []
        for col in df.select_dtypes(include=['object', 'category']).columns:
            if df[col].nunique() < 50:
                categorical_columns.append(col)
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
        return JSONResponse(content=summary_data)
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred during summary calculation: {str(e)}"}, status_code=500)

# This route serves the main page when you visit the root URL
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Routes for all other pages in the application
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
async def get_analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})
    
@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request, current_user: dict = Depends(get_current_user)):
    # This is the security check
    if not current_user:
        # If the guard finds no logged-in user, send them to the login page
        return RedirectResponse(url="/login")

    # If the user is logged in, show the history page
    return templates.TemplateResponse("history.html", {"request": request, "user": current_user})

@app.get("/settings", response_class=HTMLResponse)
async def get_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})
    
@app.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
    
@app.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})