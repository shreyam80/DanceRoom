from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.supabase import supabase

router = APIRouter()

class OrganizationCreate(BaseModel):
    name: str
    type: str

@router.post('')
def create_org(payload: OrganizationCreate, user=Depends(get_current_user)):
    org = supabase.table('organizations').insert({
        'name': payload.name,
        'type': payload.type,
        'created_by_user_id': user.id
    }).execute().data[0]
    supabase.table('organization_memberships').insert({
        'organization_id': org['organization_id'],
        'user_id': user.id,
        'role': 'choreographer',
        'status': 'active'
    }).execute()
    return org

@router.get('')
def list_orgs(user=Depends(get_current_user)):
    memberships = supabase.table('organization_memberships').select('organization_id').eq('user_id', user.id).execute().data
    ids = [m['organization_id'] for m in memberships]
    if not ids:
        return []
    return supabase.table('organizations').select('*').in_('organization_id', ids).execute().data
