from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from api.schemas.user import UserNavigateResponse, UserAdministratorResponse


class EventDraftRequest(BaseModel):
    title: str | None = Field(None, example="抽選で10名様に美食ツアーをプレゼント")
    image_url: HttpUrl = Field(...,
                               example="https://storage.googleapis.com/...")
    tags: list[str] | None = Field(None, example=["tag_uuid", "tag_uuid"])
    winning_number: int = Field(..., example=10)
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)
    detail: str = Field(..., example="抽選で10名の幸運な参加者に、豪華な美食ツアーをプレゼントします!!")
    id: str = Field(..., example="oishi_o_123", description="Event.id")

    class Config:
        from_attributes = True


class EventTagItem(BaseModel):
    uuid: str
    name: str

    class Config:
        from_attributes = True


class EventTagRequest(BaseModel):
    name: str


class EventTagResponse(BaseModel):
    tags: list[EventTagItem]


class EventPublicationRequest(BaseModel):
    id: str = Field(..., example="oishi_o_123", description="Event.id")


class EventRegistrationRequest(BaseModel):
    event_id: str = Field(..., example="oishi_o_123", description="Event.id")


class EventReceiptRequest(BaseModel):
    id: str = Field(..., example="oishi_o_123", description="Event.id")
    participant_id: str = Field(..., example="admin", description="User.id")


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
    tags: list[EventTagItem]


class EventItem(EventListItem):
    detail: str
    tags: list[EventTagItem]
    winning_number: int
    is_active: bool
    is_winner: bool | None
    has_applied: bool
    is_received: bool
    is_published: bool


class EventDetailResponse(BaseModel):
    user: UserNavigateResponse
    event: EventItem
    administrator: UserAdministratorResponse

    class Config:
        from_attributes = True


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


class EventReceiptResponse(BaseModel):
    user: UserNavigateResponse
    title: str
    address: str


class AdministratorEventListResponse(BaseModel):
    user: UserNavigateResponse
    draft_events: list[EventListItem]
    active_events: list[EventListItem]
    finished_events: list[EventListItem]
