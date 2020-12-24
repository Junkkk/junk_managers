from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.user.schema import User
from app.models.project.service import get_project
from app.db.utils import get_db
from app.api.auth import get_current_user
from app.models.managers.service import manager_list


router = APIRouter()


@router.get("/managers")
async def company_create(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        q: List[int] = Query(None)
):
    if q:
        list_names = []
        for project_id in q:
            project = await get_project(db, project_id)
            list_names.append(project.name)
        managers_list = await manager_list(db, current_user.id)
        out_data = {}
        for k, v in managers_list.items():
            if k in list_names:
                out_data[k] = v
        return out_data
    return await manager_list(db, current_user.id)
