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
    print(name)
    user = db_session.query(db_model.User).filter(db_model.User.name == name).first()
    if not user:
        return None
    return user


# from typing import Optional
# from datetime import datetime
# from sqlalchemy.orm import Session
#
# from app.models.user.db_model import User
# from app.models.user.schema import UserCreate, UserUpdate
# from app.security import verify_password, get_password_hash
# from app.base.service import CRUDBase
#
#
# class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
#     def get_by_name(self, db_session: Session, *, name: str) -> Optional[User]:
#         return db_session.query(User).filter(User.name == name).first()
#
#     def create(self, db_session: Session, *, obj_in: UserCreate) -> User:
#         db_obj = User(
#             name=obj_in.name,
#             password=get_password_hash(obj_in.password),
#             date=datetime.now()
#         )
#         db_session.add(db_obj)
#         db_session.commit()
#         db_session.refresh(db_obj)
#         return db_obj
#
#     def authenticate(
#         self, db_session: Session, *, name: str, password: str
#     ) -> Optional[User]:
#         user = self.get_by_name(db_session, name=name)
#         if not user:
#             return None
#         if not verify_password(password, user.password):
#             return None
#         return user
#
#
# crud_user = CRUDUser(User)
