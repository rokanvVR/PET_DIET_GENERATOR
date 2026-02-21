from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from petnutri_backend.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    pets = relationship("Pet", back_populates="owner")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    public_pet_id = Column(String, unique=True, index=True)
    name = Column(String)
    breed = Column(String)
    age = Column(Integer)
    weight = Column(Integer)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="pets")


class DietPlan(Base):
    __tablename__ = "diet_plans"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    plan_data = Column(Text)

    pet = relationship("Pet")