from sqlalchemy.orm import Session
from app.models.user import schema, db_model


async def create_user(db: Session, item: schema.User):
    db_item = db_model.User(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
