from sqlalchemy import func, Column, Integer, String, Boolean, DateTime, Unicode
from sqlalchemy.orm import relationship
from api.db import Base, generate_uuid


class User(Base):
    __tablename__ = "Users"

    uuid = Column(String(48), default=generate_uuid,
                  primary_key=True, index=True)
    id = Column(String(48), unique=True, nullable=False, index=True)
    email = Column(String(48), unique=True, nullable=False)
    hashed_password = Column(String(96), nullable=False)
    display_name = Column(Unicode(96), nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String(48), nullable=False)
    address = Column(Unicode(96), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    introduction = Column(Unicode(96), nullable=True)
    sns_url = Column(String(48), nullable=True)
    homepage_url = Column(String(48), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    events_administered = relationship("Event", back_populates="administrator")
    events_participated = relationship(
        "Participant", back_populates="participant")
