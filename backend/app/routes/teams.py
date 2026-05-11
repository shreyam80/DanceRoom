from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.auth import get_current_user
from app.core.supabase import supabase

router = APIRouter()

class TeamCreate(BaseModel):
    organization_id: str
    name: str
    description: str = ''

class AddMemberPayload(BaseModel):
    email: EmailStr
    role: str = 'dancer'

@router.post('')
def create_team(payload: TeamCreate, user=Depends(get_current_user)):
    team = supabase.table('teams').insert({
        'organization_id': payload.organization_id,
        'name': payload.name,
        'description': payload.description,
        'created_by_user_id': user.id
    }).execute().data[0]
    supabase.table('team_members').insert({'team_id': team['team_id'], 'user_id': user.id, 'role': 'choreographer', 'status': 'active'}).execute()
    return team

@router.get('/{team_id}')
def get_team(team_id: str, user=Depends(get_current_user)):
    team = supabase.table('teams').select('*').eq('team_id', team_id).single().execute().data
    members = supabase.table('team_members').select('*, users(full_name,email)').eq('team_id', team_id).execute().data
    return {'team': team, 'members': members}

@router.post('/{team_id}/members')
def add_member(team_id: str, payload: AddMemberPayload, user=Depends(get_current_user)):
    found = supabase.table('users').select('user_id,email').eq('email', payload.email).maybe_single().execute().data
    if not found:
        raise HTTPException(status_code=404, detail='User with this email must sign up first')
    member = supabase.table('team_members').upsert({'team_id': team_id, 'user_id': found['user_id'], 'role': payload.role, 'status': 'active'}).execute().data[0]
    return member
