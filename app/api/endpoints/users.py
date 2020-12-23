from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user.schema import User
from app.models.user.service import create_user
from app.db.utils import get_db


router = APIRouter()


@router.post("/user")
async def user_create(item: User, db: Session = Depends(get_db)):
    return await create_user(db, item)
