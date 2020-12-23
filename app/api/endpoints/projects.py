from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.project.schema import Project
from app.models.project.service import create_project
from app.db.utils import get_db


router = APIRouter()


@router.post("/project")
async def project_create(item: Project, db: Session = Depends(get_db)):
    return await create_project(db, item)
