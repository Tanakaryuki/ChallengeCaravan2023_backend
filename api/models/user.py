from sqlalchemy import func, Column, Integer, String, Boolean, DateTime, Unicode
from sqlalchemy.orm import relationship
import uuid
from api.db import Base


class User(Base):
    __tablename__ = "Users"

    uuid = Column(String(48), primary_key=True,
                  default=str(uuid.uuid4()), index=True)
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
