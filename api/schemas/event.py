from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from user import UserNavigateResponse


class EventDraftRequest(BaseModel):
    administrator_id: str = Field(..., examples="admin", description="User.id")
    title: str | None = Field(None, examples="抽選で10名様に美食ツアーをプレゼント")
    image_url: HttpUrl = Field(...,
                               examples="https://storage.googleapis.com/...")
    tags: list[str] | None = Field(None, examples=["ツアー", "グルメ体験"])
    winning_number: int = Field(..., examples=10)
    start_time: datetime = Field(..., examples=1701442800,
                                 description="UNIXTIME")
    end_time: datetime = Field(..., examples=1701486000,
                               description="UNIXTIME")
    detail: str = Field(..., examples="抽選で10名の幸運な参加者に、豪華な美食ツアーをプレゼントします!!")
    id: str = Field(..., examples="oishi_o_123", description="Event.id")

    class Config:
        orm_mode = True


class EventPublicationRequest(BaseModel):
    id: str = Field(..., examples="oishi_o_123", description="Event.id")


class EventRegistrationRequest(BaseModel):
    id: str = Field(..., examples="oishi_o_123", description="Event.id")
    participant_id: str = Field(..., examples="admin", description="User.id")


class EventListItem(BaseModel):
    id: str
    title: str
    image_url: HttpUrl
    administrator_id: str
    start_time: datetime
    end_time: datetime


class ParticipantEventListResponse(BaseModel):
    user: UserNavigateResponse
    events: list[EventListItem]
    tags: list[str]


class EventItem(EventListItem):
    detail: str
    is_active: bool
    is_winner: bool | None
    has_applied: bool
    is_published: bool


class AdministratorItem(BaseModel):
    detail: str
    sns_url: str
    homepage_url: str


class EventDetailResponse(BaseModel):
    user: UserNavigateResponse
    event: EventItem
    administrator: AdministratorItem


class EventResultItem(BaseModel):
    participant_id: str
    txid: str
    is_winner: bool


class EventResultListResponse(BaseModel):
    user: UserNavigateResponse
    results: list[EventResultItem]


class EventReceiptItem(BaseModel):
    participant_id: str
    txid: str


class EventReceiptListResponse(BaseModel):
    user: UserNavigateResponse
    receipts: list[EventReceiptItem]


class AdministratorEventListResponse(BaseModel):
    user: UserNavigateResponse
    draft_events: list[EventListItem]
    active_events: list[EventListItem]
    finished_events: list[EventListItem]
