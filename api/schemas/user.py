from pydantic import BaseModel, Field, HttpUrl, EmailStr
from datetime import datetime


class UserSignupRequest(BaseModel):
    email: EmailStr = Field(..., example="example@example.com")
    password: str = Field(..., example="password")
    id: str = Field(..., example="admin")
    display_name: str = Field(..., example="福岡太郎")
    age: int = Field(..., example=20)
    phone_number: str = Field(..., example="070-0123-4567")
    address: str = Field(..., example="〒123-4567 東京都港区浜松町1-2-3 サクラビル205号室")
    is_admin: str = Field(..., example=True)
    introduction: str | None = Field(
        example="グルメフェア株式会社は、美味しさと幸せを提供することに情熱を傾ける食品会社です。")
    sns_url: HttpUrl | None = Field(example="https://x.com/Elonmusk")
    homepage_url: str | None = Field(example="https://example.com")

    class Config:
        from_attributes = True


class UserSigninRequest(BaseModel):
    id: str = Field(..., example="admin")
    password: str = Field(..., example="password")


class UserNavigateResponse(BaseModel):
    id: str
    display_name: str
