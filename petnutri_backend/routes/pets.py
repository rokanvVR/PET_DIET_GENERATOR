from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from petnutri_backend.database.db import SessionLocal
from petnutri_backend.database import models
from petnutri_backend.core.security import verify_password
import uuid

router = APIRouter(prefix="/pets", tags=["Pets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_pet(email: str, name: str, breed: str, age: int, weight: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    public_id = "PET-" + str(uuid.uuid4())[:8].upper()

    new_pet = models.Pet(
        public_pet_id=public_id,
        name=name,
        breed=breed,
        age=age,
        weight=weight,
        owner_id=user.id
    )

    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return {
        "message": "Pet added successfully",
        "public_pet_id": public_id
    }


@router.get("/list")
def list_pets(email: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    pets = db.query(models.Pet).filter(models.Pet.owner_id == user.id).all()

    return pets