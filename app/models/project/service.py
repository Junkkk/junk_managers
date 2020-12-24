from sqlalchemy.orm import Session
from app.models.project import schema, db_model


async def create_project(db: Session, item: schema.Project):
    db_item = db_model.Project(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


async def get_project(db: Session, project_id: int):
    return db.query(db_model.Project).filter(db_model.Project.id == project_id).first()
