from sqlalchemy.ext.asyncio import AsyncSession
import api.models.user as user_model
import api.schemas.user as user_schema

from passlib.context import CryptContext


async def creatr_user(db: AsyncSession, signup: user_schema.UserSignupRequest) -> user_model.User | None:
    signup_dict = signup.dict()
    signup_dict.pop("password", None)
    hashed_password = CryptContext(["bcrypt"]).hash(signup.password)
    user = user_model.User(
        hashed_password=hashed_password, **signup_dict)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
