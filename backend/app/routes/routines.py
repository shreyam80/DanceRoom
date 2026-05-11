from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.supabase import supabase

router = APIRouter()

class RoutineCreate(BaseModel):
    team_id: str
    title: str

@router.post('')
def create_routine(payload: RoutineCreate, user=Depends(get_current_user)):
    return supabase.table('routines').insert({'team_id': payload.team_id, 'title': payload.title, 'created_by_user_id': user.id}).execute().data[0]

@router.get('/{routine_id}')
def get_routine(routine_id: str, user=Depends(get_current_user)):
    routine = supabase.table('routines').select('*').eq('routine_id', routine_id).single().execute().data
    videos = supabase.table('videos').select('*').eq('routine_id', routine_id).order('version_number', desc=True).execute().data
    return {'routine': routine, 'videos': videos}
