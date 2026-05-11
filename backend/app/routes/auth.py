from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.supabase import supabase

router = APIRouter()

class SignupPayload(BaseModel):
    email: EmailStr
    password: str
    username: str
    full_name: str
    role: str

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

@router.post('/signup')
def signup(payload: SignupPayload):
    response = supabase.auth.sign_up({
        'email': payload.email,
        'password': payload.password,
        'options': {'data': {'username': payload.username, 'full_name': payload.full_name, 'role': payload.role}}
    })
    user = response.user
    if not user:
        raise HTTPException(status_code=400, detail='Signup failed')
    supabase.table('users').upsert({
        'user_id': user.id,
        'username': payload.username,
        'full_name': payload.full_name,
        'email': payload.email,
    }).execute()
    return {'user': user.model_dump()}

@router.post('/login')
def login(payload: LoginPayload):
    response = supabase.auth.sign_in_with_password({'email': payload.email, 'password': payload.password})
    if not response.session:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return {'access_token': response.session.access_token, 'refresh_token': response.session.refresh_token, 'user': response.user.model_dump()}
