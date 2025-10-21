# In backend/app/api/credits.py

# ====================
# IMPORTS
# ====================
from fastapi import APIRouter, Depends, HTTPException, Response, Request, Header
from supabase import Client
import os
import razorpay
import json
from supabase import create_client, Client
import supabase
from .auth import get_current_user # Import your user dependency

# ====================
# CONFIGURATION
# ====================
# supabase_url = os.environ.get("SUPABASE_URL")
# supabase_key = os.environ.get("SUPABASE_KEY")
# supabase: Client = Client(supabase_url, supabase_key)

# RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID")
# RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET")
# RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET")

# ==================================================
# CREATE THE ROUTER  <-- THIS IS THE FIX
# ==================================================
router = APIRouter()

# ====================
# ENDPOINTS
# ====================

@router.post("/use-credit")
async def use_credit(current_user: dict = Depends(get_current_user)):
    """
    Checks if a user has credits, deducts one if they do,
    and returns the new credit count.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_email = current_user.get("email")

    try:
        user_profile_response = supabase.table('users').select('graph_credits').eq('email', user_email).single().execute()
        
        if not user_profile_response.data:
            raise HTTPException(status_code=404, detail="User profile not found")

        current_credits = user_profile_response.data.get('graph_credits', 0)

        if current_credits > 0:
            new_credits = current_credits - 1
            updated_user = supabase.table('users').update({'graph_credits': new_credits}).eq('email', user_email).execute()
            return {"status": "success", "credits_remaining": new_credits}
        else:
            return {"status": "insufficient_credits", "credits_remaining": 0}

    except Exception as e:
        print(f"--- CREDIT ERROR: {e} ---")
        raise HTTPException(status_code=500, detail="An error occurred while processing credits.")


# @router.post("/add-credits")
# async def add_credits_webhook(request: Request, x_razorpay_signature: str = Header(None)):
#     """
#     Listens for successful payment webhooks from Razorpay to add credits to a user.
#     """
#     body = await request.body()
    
#     try:
#         client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#         client.utility.verify_webhook_signature(body.decode('utf-8'), x_razorpay_signature, RAZORPAY_WEBHOOK_SECRET)
    
#     except Exception as e:
#         print(f"--- RAZORPAY SIGNATURE ERROR: {e} ---")
#         raise HTTPException(status_code=400, detail="Invalid request signature")

#     event = json.loads(body)
    
#     if event['event'] == 'payment.captured':
#         payload = event['payload']['payment']['entity']
#         customer_email = payload.get('email')
#         credits_to_add = 50 # Example: adding 50 credits
        
#         try:
#             user_profile = supabase.table('users').select('graph_credits').eq('email', customer_email).single().execute().data
            
#             if user_profile:
#                 current_credits = user_profile.get('graph_credits', 0)
#                 new_total = current_credits + credits_to_add
#                 supabase.table('users').update({'graph_credits': new_total}).eq('email', customer_email).execute()
#                 print(f"Successfully added {credits_to_add} credits to {customer_email}")

#         except Exception as e:
#             print(f"--- ERROR ADDING CREDITS: {e} ---")
#             pass
    
#     return Response(status_code=200)