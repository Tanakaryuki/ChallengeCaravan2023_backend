from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.engine import Result

import api.models.event as event_model
import api.schemas.event as event_schema


def creatr_tag(db: Session, tag: event_schema.EventTagRequest) -> event_model.Tag | None:
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
