from fastapi import Header, HTTPException
from app.core.supabase import supabase

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    resp = supabase.auth.get_user(token)
    user = resp.user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
