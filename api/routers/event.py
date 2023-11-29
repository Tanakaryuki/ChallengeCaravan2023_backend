from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

import api.schemas.event as event_schema
import api.cruds.event as event_crud
import api.models.event as event_model
from api.db import get_db


router = APIRouter()


@router.get("/events/participant", response_model=event_schema.ParticipantEventListResponse, description="参加者向けに利用可能な全てのイベント一覧を取得するために使用されます。", tags=["events"])
def get_events_participant(db: Session = Depends(get_db)) -> event_schema.ParticipantEventListResponse:
    pass


@router.get("/events/search", response_model=event_schema.ParticipantEventListResponse, description="イベントをキーワードやタグを使用して絞り込み検索するために使用されます。", tags=["events"])
def search_events(
    db: Session = Depends(get_db),
    keyword: str = Query(None, description="Search keyword"),
    tags: list[str] = Query(None, description="Search tags")
) -> event_schema.ParticipantEventListResponse:
    pass


@router.get("/event/{id}", response_model=event_schema.EventDetailResponse, description="指定されたイベントの詳細情報を取得するために使用されます。idパラメータによってイベントIDを指定します。", tags=["events"])
def get_event(id: str, db: Session = Depends(get_db)) -> event_schema.EventDetailResponse:
    pass


@router.post("/event", description="イベントに参加するために利用されます。", tags=["events"])
def register_events(request: event_schema.EventRegistrationRequest, db: Session = Depends(get_db)):
    pass


@router.get("/event/{id}/results", response_model=event_schema.EventResultListResponse, description="指定されたイベントの抽選結果を取得するために使用されます。idパラメータによってイベントIDを指定します。", tags=["events"])
def get_result(id: str, db: Session = Depends(get_db)) -> event_schema.EventResultListResponse:
    pass


@router.get("/event/{id}/receipt", response_model=event_schema.EventReceiptResponse, description="指定されたイベントの参加者が受け取り確認するために使用されます。idパラメータによってイベントIDを指定します。", tags=["events"])
def get_receipt(id: str, db: Session = Depends(get_db)) -> event_schema.EventReceiptResponse:
    pass


@router.post("/event/{id}/receipt", description="指定されたイベントの参加者が景品を受け取ったことを確認するために使用されます。idパラメータによってイベントIDを指定します。", tags=["events"])
def post_receipt(request: event_schema.EventReceiptRequest, db: Session = Depends(get_db)):
    pass


@router.get("/event/{id}/receipts", response_model=event_schema.EventReceiptListResponse, description="指定されたイベントの受領一覧を取得するために使用されます。idパラメータによってイベントIDを指定します。", tags=["events"])
def get_receipt(id: str, db: Session = Depends(get_db)) -> event_schema.EventReceiptListResponse:
    pass


@router.get("/event/tags", response_model=event_schema.EventTagResponse, description="利用可能なタグ一覧を取得するために使用されます。", tags=["events"])
def get_tags(db: Session = Depends(get_db)) -> event_schema.EventTagResponse:
    pass


@router.post("/event/tag", description="新しいタグを作成するために使用されます。", tags=["events"])
def post_tag(request: event_schema.EventTagRequest, db: Session = Depends(get_db)):
    tag = event_crud.creatr_tag(db, request)
    if not tag:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED


@router.get("/events/administrator", response_model=event_schema.AdministratorEventListResponse, description="主催者向けに利用可能な全てのイベント一覧を取得するために使用されます。", tags=["events"])
def get_events_administrator(db: Session = Depends(get_db)) -> event_schema.AdministratorEventListResponse:
    pass


@router.post("/event/draft", description="新しいイベントの下書きを作成するために使用されます。", tags=["events"])
def draft_event(request: event_schema.EventDraftRequest, db: Session = Depends(get_db)):
    pass


@router.post("/event/publish", description="下書き状態にあるイベントを公開するために使用されます。", tags=["events"])
def publish_event(request: event_schema.EventPublicationRequest, db: Session = Depends(get_db)):
    pass
