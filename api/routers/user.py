from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

import api.schemas.user as user_schema
import api.cruds.user as user_crud
import api.models.user as user_model
from api.db import get_db

load_dotenv()
router = APIRouter()


def _get_current_user(access_token: str = Depends(OAuth2PasswordBearer("/api/signin")), db: Session = Depends(get_db)):
    try:
        data = jwt.decode(access_token, os.environ["SECRET_KEY"], "HS256")
        username = data.get("sub")
        if not username:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user = user_crud.read_user_by_id(db, id=username)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user


@router.post("/signup", description="新しいアカウントを作成するために使用されます。", tags=["users"])
def signup(request: user_schema.UserSignupRequest, db: Session = Depends(get_db)):
    user = user_crud.read_user_by_id(db, id=request.id)
    if user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user = user_crud.creatr_user(db, request)
    return status.HTTP_201_CREATED


@router.post("/signin", description="既存ユーザがアカウントにサインインするために使用されます。", tags=["users"], response_model=user_schema.UserTokenResponse)
def signin(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> user_schema.UserTokenResponse:
    user = user_crud.read_user_by_id(db, id=request.username)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if not CryptContext(["bcrypt"]).verify(request.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    token = user_schema.UserTokenResponse(
        access_token=jwt.encode(
            {"sub": request.username}, os.environ["SECRET_KEY"], "HS256")
    )

    return token


@router.post("/me", description="ログインしているユーザの情報を取得するために使用されます", tags=["users"], response_model=user_schema.UserInformationResponse)
def signin(current_user: user_model.User = Depends(_get_current_user), db: Session = Depends(get_db)) -> user_schema.UserInformationResponse:
    user = user_crud.read_user_by_id(db, id=current_user.id)

    return user
