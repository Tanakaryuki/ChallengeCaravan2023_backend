from sqlalchemy.orm import Session
from sqlalchemy import select
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
