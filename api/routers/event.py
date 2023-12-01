from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import api.schemas.event as event_schema
import api.cruds.event as event_crud
import api.models.event as event_model
import api.cruds.user as user_crud
import api.models.user as user_model
from api.db import get_db

from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.base import JobLookupError


router = APIRouter()

trigger = IntervalTrigger(minutes=5)
scheduler = BackgroundScheduler()
scheduler.start()


def job_wrapper(id: int, db: Session = Depends(get_db)):
    result = event_crud.show_timestamp(id)

    try:
        if result["txid"]:
            event_crud.update_participant_txid(db, id=id, txid=result["txid"])
            scheduler.remove_job(str(id))
    except JobLookupError:
        pass


def _get_current_user(access_token: str = Depends(OAuth2PasswordBearer("/api/signin")), db: Session = Depends(get_db)):
    try:
        data = jwt.decode(access_token, os.environ["SECRET_KEY"], "HS256")
        username = data.get("sub")
        if not username:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user = user_crud.read_user_by_id(db, id=username)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user


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
def get_event(id: str, current_user: user_model.User = Depends(_get_current_user), db: Session = Depends(get_db)) -> event_schema.EventDetailResponse:
    user = user_crud.read_user_by_id(db, id=current_user.id)
    event = event_crud.read_event_by_id(db, id=id)

    if (event is None):
        raise HTTPException(status_code=404, detail="Event not found")

    administrator = user_crud.read_user_by_id(db, id=event.administrator_id)
    event_participant = event_crud.read_participant_by_event_id_and_participant_id(
        db, event_id=id, participant_id=current_user.id)

    common_properties: dict = {
        'id': event.id,
        'title': event.title,
        'image_url': event.image_url,
        'administrator_id': event.administrator_id,
        'start_time': event.start_time,
        'end_time': event.end_time,
        'detail': event.detail,
        'winning_number': event.winning_number,
        'is_active': event.is_active,
        'tags': event.tags,
        'is_published': event.is_published
    }

    if event_participant is None:
        common_properties.update(
            {'is_winner': None, 'has_applied': False, 'is_received': False})
    else:
        common_properties.update({
            'is_winner': event_participant.is_winner,
            'has_applied': True,
            'is_received': event_participant.is_received
        })

    # EventItemオブジェクトの作成
    event = event_schema.EventItem(**common_properties)

    return event_schema.EventDetailResponse(user=user, event=event, administrator=administrator)


@router.post("/event", description="イベントに参加するために利用されます。", tags=["events"])
def register_events(request: event_schema.EventRegistrationRequest, current_user: user_model.User = Depends(_get_current_user), db: Session = Depends(get_db)):
    event = event_crud.read_event_by_id(db, request.event_id)
    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    participant = event_crud.read_participant_by_event_id_and_participant_id(
        db, request.event_id, current_user.id)
    if participant:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    participant = event_crud.join_event(db, request.event_id, current_user.id)
    if not participant:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    scheduler.add_job(job_wrapper, id=str(participant.id), args=[
                      participant.id, db], trigger=trigger)

    return status.HTTP_201_CREATED


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
def post_tag(request: event_schema.EventTagRequest, current_user: user_model.User = Depends(_get_current_user), db: Session = Depends(get_db)):
    tag = event_crud.create_tag(db, request)
    if not tag:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED


@router.get("/events/administrator", response_model=event_schema.AdministratorEventListResponse, description="主催者向けに利用可能な全てのイベント一覧を取得するために使用されます。", tags=["events"])
def get_events_administrator(db: Session = Depends(get_db)) -> event_schema.AdministratorEventListResponse:
    pass


@router.post("/event/draft", description="新しいイベントの下書きを作成するために使用されます。", tags=["events"])
def draft_event(request: event_schema.EventDraftRequest, current_user: user_model.User = Depends(_get_current_user), db: Session = Depends(get_db)):
    event = event_crud.draft_event(db, current_user.id, request)
    if not event:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return status.HTTP_201_CREATED


@router.post("/event/publish", description="下書き状態にあるイベントを公開するために使用されます。", tags=["events"])
def publish_event(request: event_schema.EventPublicationRequest, db: Session = Depends(get_db)):
    pass


@router.get("/get_jobs", description="スケジューリングされたjobを確認するために使用されます。", tags=["scheduler"])
def get_jobs():
    jobs = scheduler.get_jobs()
    return {"jobs": [str(job) for job in jobs]}
