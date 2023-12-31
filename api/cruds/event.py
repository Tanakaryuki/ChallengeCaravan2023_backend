from sqlalchemy.orm import Session
from sqlalchemy import and_

import api.models.event as event_model
import api.schemas.event as event_schema

import os
import requests


def record_timestamp(content: str):

    url = os.environ["TAPYRUS_API_ENDPOINT_URL"] + '/api/v1/timestamps'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["ACCESS_TOKEN"]
    }

    data = {
        "content": content,
        "digest": "none",
        "prefix": "TMESTAMPAPP",
        "type": "simple"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        response_json = response.json()
        return response_json
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "ERROR"


def show_timestamp(id: int) -> str:

    url = os.environ["TAPYRUS_API_ENDPOINT_URL"] + \
        '/api/v1/timestamps/' + str(id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["ACCESS_TOKEN"]
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return "ERROR"


def create_tag(db: Session, tag: event_schema.EventTagRequest) -> event_model.Tag | None:
    tag_dict = tag.model_dump()
    tag = event_model.Tag(**tag_dict)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def draft_event(db: Session, id: str, event: event_schema.EventDraftRequest) -> event_model.Event | None:
    event_dict = event.model_dump()
    tag_uuids = event_dict.pop("tags", [])
    tags = db.query(event_model.Tag).filter(
        event_model.Tag.uuid.in_(tag_uuids)).all()

    event = event_model.Event(administrator_id=id, **event_dict)
    event.tags = tags

    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def read_event_by_id(db: Session, id: str) -> event_model.Event | None:
    return db.query(event_model.Event).filter(event_model.Event.id == id).first()


def read_participant_by_event_id_and_participant_id(db: Session, event_id: str, participant_id: str) -> event_model.Participant | None:
    return db.query(event_model.Participant).filter(and_(event_model.Participant.event_id == event_id, event_model.Participant.participant_id == participant_id)).first()


def join_event(db: Session, event_id: str, participant_id: str) -> event_model.Participant | None:
    response = record_timestamp(
        content=event_id + "_" + participant_id + "_join")
    if response == "ERROR":
        return None

    participant = event_model.Participant(
        event_id=event_id, participant_id=participant_id, join_id=response["id"])
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def update_participant_join_txid(db: Session, id: int, txid: str) -> event_model.Participant | None:
    participant = db.query(event_model.Participant).filter(
        event_model.Participant.join_id == id).first()
    participant.join_txid = txid
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def update_participant_received_txid(db: Session, id: int, txid: str) -> event_model.Participant | None:
    participant = db.query(event_model.Participant).filter(
        event_model.Participant.received_id == id).first()
    participant.received_txid = txid
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def publish_event(db: Session, id: str) -> event_model.Event | None:
    event = read_event_by_id(db, id)
    event.is_published = True
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def receipt_event(db: Session, event_id: str, participant_id: str) -> event_model.Participant | None:
    response = record_timestamp(
        content=event_id + "_" + participant_id + "_received")
    if response == "ERROR":
        return None

    participant = read_participant_by_event_id_and_participant_id(
        db, event_id, participant_id)
    participant.is_received = True
    participant.received_id = response["id"]
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def read_participants_by_event_id(db: Session, event_id: str) -> event_model.Participant | None:
    return db.query(event_model.Participant).filter(event_model.Participant.event_id == event_id).all()


def update_is_winner(db: Session, event_id: str, participant_id: str, is_winner: bool) -> event_model.Participant | None:
    participant = read_participant_by_event_id_and_participant_id(
        db, event_id, participant_id)
    participant.is_winner = is_winner
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


def update_is_active(db: Session, id: str, is_active: bool) -> event_model.Event | None:
    event = read_event_by_id(db, id)
    event.is_active = is_active
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def read_is_winner_participants_by_event_id(db: Session, event_id: str) -> event_model.Participant | None:
    return db.query(event_model.Participant).filter(and_(event_model.Participant.event_id == event_id, event_model.Participant.is_winner == True)).all()


def read_events_by_participant(db: Session) -> event_model.Event | None:
    return db.query(event_model.Event).filter(event_model.Event.is_published == True).all()


def read_draft_events_by_Administrator(db: Session, administrator_id: str) -> event_model.Event | None:
    return db.query(event_model.Event).filter(and_(event_model.Event.is_published == False, event_model.Event.administrator_id == administrator_id)).all()


def read_active_events_by_Administrator(db: Session, administrator_id: str) -> event_model.Event | None:
    return db.query(event_model.Event).filter(and_(event_model.Event.is_published == True, event_model.Event.administrator_id == administrator_id, event_model.Event.is_active == True)).all()


def read_finished_events_by_Administrator(db: Session, administrator_id: str) -> event_model.Event | None:
    return db.query(event_model.Event).filter(and_(event_model.Event.is_published == True, event_model.Event.administrator_id == administrator_id, event_model.Event.is_active == False)).all()


def read_tags(db: Session) -> event_model.Tag | None:
    return db.query(event_model.Tag).all()
