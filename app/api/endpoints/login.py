from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.utils import get_db
from app.api.auth import get_current_user
from app.models.token.schemas import Token
from app.models.user.db_model import User as DBUser
from app.models.user.schema import User
from app.models.user.service import authenticate
from app.api.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()


@router.post("/login/access-token", response_model=Token, tags=["login"])
async def login_access_token(
        username: str,
        db: Session = Depends(get_db)
):
    user = authenticate(db, name=username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get("/login/test-token", tags=["login"])
async def test_token(current_user: DBUser = Depends(get_current_user)):
    return current_user
