from sqlalchemy.orm import Session
from app.models.user import schema, db_model


async def get_user(db: Session, user_id: int):
    return db.query(db_model.User).filter(db_model.User.id == user_id).first()


async def create_user(db: Session, item: schema.User):
    db_item = db_model.User(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def authenticate(db_session: Session, name: str):
    user = db_session.query(db_model.User).filter(db_model.User.name == name).first()
    if not user:
        return None
    return user
