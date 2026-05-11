from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.supabase import supabase

router = APIRouter()

class VideoCreate(BaseModel):
    routine_id: str
    file_url: str
    storage_path: str
    recorded_at: str | None = None
    duration_seconds: float | None = None

@router.post('')
def create_video(payload: VideoCreate, user=Depends(get_current_user)):
    latest = supabase.table('videos').select('version_number').eq('routine_id', payload.routine_id).order('version_number', desc=True).limit(1).execute().data
    version = (latest[0]['version_number'] + 1) if latest else 1
    return supabase.table('videos').insert({
        'routine_id': payload.routine_id,
        'uploaded_by_user_id': user.id,
        'file_url': payload.file_url,
        'storage_path': payload.storage_path,
        'version_number': version,
        'recorded_at': payload.recorded_at,
        'duration_seconds': payload.duration_seconds,
    }).execute().data[0]

@router.get('/{video_id}')
def get_video(video_id: str, user=Depends(get_current_user)):
    video = supabase.table('videos').select('*').eq('video_id', video_id).single().execute().data
    return video
