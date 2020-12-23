from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.company.schema import Company
from app.models.company.service import create_company
from app.db.utils import get_db


router = APIRouter()


@router.post("/company")
async def company_create(item: Company, db: Session = Depends(get_db)):
    return await create_company(db, item)
