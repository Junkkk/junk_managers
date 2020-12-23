from sqlalchemy.orm import Session
from app.models.membership import schema, db_model


async def create_membership(db: Session, item: schema.Membership):
    db_item = db_model.Membership(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
