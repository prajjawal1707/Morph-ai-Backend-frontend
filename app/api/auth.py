from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import os

# Import Google's libraries for token verification
from google.oauth2 import id_token
from google.auth.transport import requests

# This reads your Google Client ID from the Onrender environment variables
# This is the secure way to handle secrets.
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

router = APIRouter()

# Pydantic model to expect the token in the request body
class Token(BaseModel):
    token: str

@router.post("/auth/google")
async def google_auth(token_data: Token = Body(...)):
    """
    Handles the token sent from the frontend, verifies it with Google,
    and returns user information upon successful verification.
    """
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google Client ID is not configured on the server.")

    try:
        # Verify the token with Google
        id_info = id_token.verify_oauth2_token(
            token_data.token, requests.Request(), GOOGLE_CLIENT_ID
        )

        user_email = id_info.get("email")
        user_name = id_info.get("name")
        
        # In the future, you can find or create a user in your database here.
        # For now, we just return a success message.
        return {
            "message": "Login successful!",
            "user": {
                "email": user_email,
                "name": user_name,
            }
        }

    except ValueError as e:
        # This error happens if the token is invalid
        raise HTTPException(status_code=401, detail=f"Invalid Google token: {e}")