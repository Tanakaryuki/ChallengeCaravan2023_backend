from pydantic import BaseModel, Field, HttpUrl, EmailStr
from datetime import datetime


class UserSignupRequest(BaseModel):
    email: EmailStr = Field(..., examples="example@example.com")
    password: str = Field(..., examples="password")
    id: str = Field(..., examples="admin")
    display_name: str = Field(..., examples="福岡太郎")
    age: int = Field(..., examples=20)
    phone_number: str = Field(..., examples="070-0123-4567")
    address: str = Field(..., examples="〒123-4567 東京都港区浜松町1-2-3 サクラビル205号室")
    introduction: str | None = Field(
        examples="グルメフェア株式会社は、美味しさと幸せを提供することに情熱を傾ける食品会社です。")
    sns_url: HttpUrl | None = Field(examples="https://x.com/Elonmusk")
    homepage_url: str | None = Field(examples="https://example.com")

    class Config:
        orm_mode = True


class UserSigninRequest(BaseModel):
    email: EmailStr = Field(..., examples="example@example.com")
    password: str = Field(..., examples="password")


class UserNavigateResponse(BaseModel):
    id: str
    display_name: str
