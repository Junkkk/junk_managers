from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.membership.schema import Membership
from app.models.membership.service import create_membership
from app.db.utils import get_db


router = APIRouter()


@router.post("/membership")
async def membership_create(item: Membership, db: Session = Depends(get_db)):
    return await create_membership(db, item)
