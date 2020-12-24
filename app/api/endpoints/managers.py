from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user.schema import User
from app.db.utils import get_db
from app.api.auth import get_current_user
from app.models.managers.service import manager_list


router = APIRouter()


@router.get("/managers")
async def company_create(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    return await manager_list(db, current_user.id)
