from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Unicode, Boolean
from sqlalchemy.orm import relationship
import uuid
from api.db import Base


class Event(Base):
    __tablename__ = "Events"

    uuid = Column(String(48), primary_key=True,
                  default=str(uuid.uuid4()), index=True)
    id = Column(String(48), unique=True, nullable=False, index=True)
    administrator_id = Column(String(48), ForeignKey(
        "Users.id"), nullable=False, index=True)
    title = Column(String(48), nullable=False)
    image_url = Column(String(48), nullable=False)
    winning_number = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    detail = Column(Unicode(96), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, index=True)
    is_published = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship(
        "User", back_populates="administrator", uselist=False)
    participants = relationship("Participant", back_populates="event")
    tags = relationship("Tag", secondary="EventTag", back_populates="events")


class Tag(Base):
    __tablename__ = "Tags"

    uuid = Column(String(48), primary_key=True, default=str(uuid.uuid4()))
    name = Column(Unicode(96), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    events = relationship("Event", secondary="EventTag", back_populates="tags")


class EventTag(Base):
    __tablename__ = "EventTag"

    uuid = Column(String(48), primary_key=True,
                  default=str(uuid.uuid4()), index=True)
    event_uuid = Column(String(48), ForeignKey("Events.uuid"))
    tag_uuid = Column(String(48), ForeignKey("Tags.uuid"))


class Participant(Base):
    __tablename__ = "Participants"

    uuid = Column(String(48), primary_key=True,
                  default=str(uuid.uuid4()), index=True)
    event_id = Column(String(48), ForeignKey("Events.id"),
                      nullable=False, index=True)
    participant_id = Column(String(48), ForeignKey(
        "Users.id"), nullable=False, index=True)
    txid = Column(String(48), nullable=False)
    is_winner = Column(Boolean, nullable=True)
    is_received = Column(Boolean, nullable=False, default=False, index=True)

    event = relationship("Event", back_populates="participants")
    user = relationship("User", back_populates="participant", uselist=False)
