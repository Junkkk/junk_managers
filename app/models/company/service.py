from sqlalchemy.orm import Session
from app.models.company import schema, db_model


async def create_company(db: Session, item: schema.Company):
    db_item = db_model.Company(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
