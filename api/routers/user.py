from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.user as user_schema
from api.db import get_db

router = APIRouter()


@router.post("/signup", description="新しいアカウントを作成するために使用されます。", tags=["users"])
def singup(request: user_schema.UserSignupRequest, db: AsyncSession = Depends(get_db)):
    pass


@router.post("/signin", description="既存ユーザがアカウントにサインインするために使用されます。", tags=["users"], response_model=user_schema.UserTokenResponse)
def singup(request: user_schema.UserSigninRequest, db: AsyncSession = Depends(get_db)):
    pass
