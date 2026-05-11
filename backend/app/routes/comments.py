from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.supabase import supabase

router = APIRouter()

class CommentCreate(BaseModel):
    video_id: str
    body: str
    video_timestamp_seconds: float
    target_type: str
    user_id: str | None = None
    subgroup_id: str | None = None
    team_id: str | None = None

@router.post('')
def create_comment(payload: CommentCreate, user=Depends(get_current_user)):
    comment = supabase.table('comments').insert({
        'video_id': payload.video_id,
        'author_user_id': user.id,
        'body': payload.body,
        'video_timestamp_seconds': payload.video_timestamp_seconds,
        'target_type': payload.target_type,
    }).execute().data[0]

    supabase.table('comment_targets').insert({
        'comment_id': comment['comment_id'],
        'user_id': payload.user_id,
        'subgroup_id': payload.subgroup_id,
        'team_id': payload.team_id,
    }).execute()

    recipients = []
    if payload.target_type == 'individual' and payload.user_id:
        recipients = [payload.user_id]
    elif payload.target_type == 'subgroup' and payload.subgroup_id:
        rows = supabase.table('subgroup_members').select('user_id').eq('subgroup_id', payload.subgroup_id).execute().data
        recipients = [r['user_id'] for r in rows]
    elif payload.target_type == 'team' and payload.team_id:
        rows = supabase.table('team_members').select('user_id').eq('team_id', payload.team_id).eq('role', 'dancer').execute().data
        recipients = [r['user_id'] for r in rows]
    else:
        raise HTTPException(status_code=400, detail='Invalid target')

    if recipients:
        supabase.table('comment_recipients').insert([
            {'comment_id': comment['comment_id'], 'user_id': uid, 'status': 'open'} for uid in recipients
        ]).execute()

    return comment

@router.get('/video/{video_id}')
def list_video_comments(video_id: str, user=Depends(get_current_user)):
    return supabase.table('comments').select('*, comment_targets(*)').eq('video_id', video_id).order('video_timestamp_seconds').execute().data

@router.get('/video/{video_id}/recipient')
def recipient_comments(video_id: str, user=Depends(get_current_user)):
    return supabase.table('comment_recipients').select('*, comments(*)').eq('user_id', user.id).eq('comments.video_id', video_id).execute().data

@router.post('/{comment_id}/acknowledge')
def acknowledge(comment_id: str, user=Depends(get_current_user)):
    return supabase.table('comment_recipients').update({'acknowledged_at': 'now()', 'status': 'acknowledged'}).eq('comment_id', comment_id).eq('user_id', user.id).execute().data

@router.post('/{comment_id}/resolve')
def resolve(comment_id: str, user=Depends(get_current_user)):
    return supabase.table('comments').update({'status': 'resolved', 'resolved_by_user_id': user.id, 'resolved_at': 'now()'}).eq('comment_id', comment_id).execute().data
