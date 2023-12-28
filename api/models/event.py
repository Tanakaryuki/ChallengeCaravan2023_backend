from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from api.db import Base, generate_uuid


class Event(Base):
    __tablename__ = "Events"

    uuid = Column(String(48), primary_key=True,
                  default=generate_uuid, index=True)
    id = Column(String(48), unique=True, nullable=False, index=True)
    administrator_id = Column(String(48), ForeignKey(
        "Users.id"), nullable=False, index=True)
    title = Column(String(48), nullable=False)
    image_url = Column(String(255), nullable=False)
    winning_number = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    detail = Column(String(96), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, index=True)
    is_published = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    administrator = relationship("User", back_populates="events_administered")
    participants = relationship("Participant", back_populates="event")
    tags = relationship("Tag", secondary="EventTag",
                        back_populates="event_tags")


class Tag(Base):
    __tablename__ = "Tags"

    uuid = Column(String(48), primary_key=True, default=generate_uuid)
    name = Column(String(96), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    event_tags = relationship(
        "Event", secondary="EventTag", back_populates="tags")


class EventTag(Base):
    __tablename__ = "EventTag"

    uuid = Column(String(48), primary_key=True,
                  default=generate_uuid, index=True)
    event_uuid = Column(String(48), ForeignKey("Events.uuid"))
    tag_uuid = Column(String(48), ForeignKey("Tags.uuid"))


class Participant(Base):
    __tablename__ = "Participants"

    uuid = Column(String(48), primary_key=True,
                  default=generate_uuid, index=True)
    event_id = Column(String(48), ForeignKey(
        "Events.id"), nullable=False, index=True)
    participant_id = Column(String(48), ForeignKey(
        "Users.id"), nullable=False, index=True)
    join_txid = Column(String(96), nullable=True)
    received_txid = Column(String(96), nullable=True)
    join_id = Column(Integer, nullable=False)
    received_id = Column(Integer, nullable=True)
    is_winner = Column(Boolean, nullable=True)
    is_received = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    event = relationship("Event", back_populates="participants")
    participant = relationship("User", back_populates="events_participated")
