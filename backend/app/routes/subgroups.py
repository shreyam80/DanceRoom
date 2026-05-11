from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.supabase import supabase

router = APIRouter()

class SubgroupCreate(BaseModel):
    team_id: str
    name: str

class AddSubgroupMember(BaseModel):
    user_id: str

@router.post('')
def create_subgroup(payload: SubgroupCreate, user=Depends(get_current_user)):
    return supabase.table('subgroups').insert({'team_id': payload.team_id, 'name': payload.name, 'created_by_user_id': user.id}).execute().data[0]

@router.post('/{subgroup_id}/members')
def add_subgroup_member(subgroup_id: str, payload: AddSubgroupMember, user=Depends(get_current_user)):
    return supabase.table('subgroup_members').upsert({'subgroup_id': subgroup_id, 'user_id': payload.user_id}).execute().data[0]
