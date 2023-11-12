from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.user as user_model
import api.schemas.user as user_schema

from passlib.context import CryptContext


async def creatr_user(db: AsyncSession, signup: user_schema.UserSignupRequest) -> user_model.User | None:
    signup_dict = signup.model_dump()
    signup_dict.pop("password", None)
    hashed_password = CryptContext(["bcrypt"]).hash(signup.password)
    user = user_model.User(
        hashed_password=hashed_password, **signup_dict)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def read_user_by_id(db: AsyncSession, id: str) -> user_model.User | None:
    result: Result = await (db.execute(select(user_model.User).filter(user_model.User.id == id)))
    user: user_model.User | None = result.first()
    if user is None:
        return None
    else:
        return user[0]
