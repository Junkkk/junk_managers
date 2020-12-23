from sqlalchemy.orm import Session
from app.models.project import schema, db_model


async def create_project(db: Session, item: schema.Project):
    db_item = db_model.Project(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
