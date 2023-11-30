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
    is_admin: bool = Field(..., example=True)
    introduction: str | None = Field(
        example="グルメフェア株式会社は、美味しさと幸せを提供することに情熱を傾ける食品会社です。")
    sns_url: HttpUrl | None = Field(example="https://x.com/Elonmusk")
    homepage_url: str | None = Field(example="https://example.com")

    class Config:
        from_attributes = True


class UserNavigateResponse(BaseModel):
    id: str
    display_name: str

    class Config:
        from_attributes = True


class UserAdministratorResponse(BaseModel):
    display_name: str
    introduction: str
    sns_url: str
    homepage_url: str

    class Config:
        from_attributes = True


class UserInformationResponse(BaseModel):
    uuid: str
    email: EmailStr
    id: str
    display_name: str
    age: int
    phone_number: str
    address: str
    is_admin: bool
    introduction: str | None
    sns_url: HttpUrl | None
    homepage_url: str | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class UserTokenResponse(BaseModel):
    access_token: str
