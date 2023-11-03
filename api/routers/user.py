from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.user as user_schema
import api.cruds.user as user_crud
from api.db import get_db

router = APIRouter()


@router.post("/signup", description="新しいアカウントを作成するために使用されます。", tags=["users"])
async def singup(request: user_schema.UserSignupRequest, db: AsyncSession = Depends(get_db)):
    user = await user_crud.creatr_user(db, request)
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED


@router.post("/signin", description="既存ユーザがアカウントにサインインするために使用されます。", tags=["users"], response_model=user_schema.UserTokenResponse)
def singup(request: user_schema.UserSigninRequest, db: AsyncSession = Depends(get_db)):
    pass
