# File: backend/main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Create the application
app = FastAPI()

# Tell the app where to find your HTML files
templates = Jinja2Templates(directory="templates")


# =================================================================
#    👇 THIS IS THE CORRECTED HOMEPAGE ROUTE 👇
# =================================================================
# This function handles the homepage (http://127.0.0.1:8000)
# and correctly loads dashboard.html. The old route for index.html is gone.
@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# =================================================================
#    ROUTES FOR ALL YOUR OTHER PAGES
# =================================================================

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
async def get_analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})
    
@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

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