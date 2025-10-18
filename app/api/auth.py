from fastapi import APIRouter, HTTPException, Depends, Request, Form, Response
from fastapi.responses import RedirectResponse
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

# Security and Token Libraries
from passlib.context import CryptContext
from jose import JWTError, jwt

# Supabase Library
from supabase import create_client, Client
# Add this to your imports at the top of auth.py
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# =================================================================
#  CONFIGURATION
# =================================================================

# --- Supabase Connection ---
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# --- Password Hashing Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- JWT Configuration ---
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Router Setup ---
router = APIRouter()

# =================================================================
#  HELPER & DEPENDENCY FUNCTIONS
# =================================================================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    token = token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
    
    # Check the REAL database
    user_response = supabase.table('users').select("*").eq('email', email).execute()
    if not user_response.data:
        return None
        
    return user_response.data[0]

# In backend/app/api/auth.py

@router.post("/signup")
async def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        # We now ONLY call the official Supabase auth function.
        # The database trigger will handle creating the public profile automatically.
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username
                }
            }
        })

        if not auth_response.user:
            return RedirectResponse(url="/signup?error=Signup+failed,+user+may+already+exist.", status_code=303)

    except Exception as e:
        print(f"--- SIGNUP ERROR: {e} ---")
        return RedirectResponse(url="/signup?error=An+unexpected+error+occurred.", status_code=303)

    # Redirect to a page telling the user to check their email for a confirmation link.
    return RedirectResponse(url="/login?msg=Signup+Successful!+Please+confirm+your+email.", status_code=303)

# In backend/app/api/auth.py

@router.post("/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...)):
    try:
        # Use the official Supabase function to sign in.
        # This securely communicates with the auth system.
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        # If login is successful, Supabase returns a session object with an access token.
        if auth_response.session:
            access_token = auth_response.session.access_token
            
            # Create a redirect response and set the access token in a secure cookie.
            redirect_response = RedirectResponse(url="/dashboard", status_code=303)
            redirect_response.set_cookie(
                key="access_token", 
                value=f"Bearer {access_token}", 
                httponly=True, 
                samesite="lax"
            )
            return redirect_response
        else:
            # Handle cases where login failed (wrong password, unconfirmed email, etc.)
            return RedirectResponse(url="/login?error=Incorrect+email+or+password", status_code=303)
            
    except Exception as e:
        print(f"--- LOGIN ERROR: {e} ---")
        return RedirectResponse(url="/login?error=Incorrect+email+or+password", status_code=303)

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token")
    return response


@router.get("/users/me")
async def read_users_me(current_user: Optional[dict] = Depends(get_current_user)):
    if current_user:
        return {
            "loggedIn": True, 
            "username": current_user.get("username"), 
            "email": current_user.get("email"),
            "credits": current_user.get("graph_credits")
        }
    return {"loggedIn": False}


# Add this new route inside auth.py
@router.post("/auth/google/callback")
async def google_auth_callback(request: Request):
    # The form data is sent by the JavaScript in your HTML
    form_data = await request.form()
    credential = form_data.get('credential')
    
    if not credential:
        raise HTTPException(status_code=400, detail="No credential provided")

    try:
        # Verify the ID token with Google
        id_info = id_token.verify_oauth2_token(
            credential, 
            google_requests.Request(), 
            os.environ.get("GOOGLE_CLIENT_ID")
        )

        email = id_info.get('email')
        username = id_info.get('name')

        # Check if user exists in your database
        user_response = supabase.table('users').select("*").eq('email', email).execute()

        if not user_response.data:
            # If user doesn't exist, create them
            supabase.table('users').insert({
                "username": username,
                "email": email,
                # You might want to leave password null for Google users
            }).execute()
            # Fetch the new user's data
            user_response = supabase.table('users').select("*").eq('email', email).execute()
        
        user = user_response.data[0]
        
        # Create an access token and log them in
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="lax")
        return response

    except ValueError as e:
        # Invalid token
        print(f"Google Token Error: {e}")
        return RedirectResponse(url="/login?error=Invalid+Google+token", status_code=303)