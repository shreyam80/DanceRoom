from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.core.supabase import supabase

router = APIRouter()

@router.get('')
def dashboard(user=Depends(get_current_user)):
    profile = supabase.table('users').select('*').eq('user_id', user.id).single().execute().data
    role = user.user_metadata.get('role', 'dancer')
    if role == 'choreographer':
        organizations = supabase.table('organizations').select('*').eq('created_by_user_id', user.id).execute().data
        teams = supabase.table('teams').select('*').eq('created_by_user_id', user.id).execute().data
        routines = supabase.table('routines').select('*').eq('created_by_user_id', user.id).execute().data
        videos = supabase.table('videos').select('*').eq('uploaded_by_user_id', user.id).execute().data
        comments = supabase.table('comments').select('status').eq('author_user_id', user.id).execute().data
        return {'role': role, 'profile': profile, 'organizations': organizations, 'teams': teams, 'routines': routines, 'videos': videos, 'comments': comments}
    assigned = supabase.table('comment_recipients').select('status, comments(*)').eq('user_id', user.id).execute().data
    return {'role': role, 'profile': profile, 'assigned_feedback': assigned}
