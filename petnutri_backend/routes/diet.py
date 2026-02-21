from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from petnutri_backend.database.db import SessionLocal
from petnutri_backend.database import models
from petnutri_backend.core.security import decode_access_token
from petnutri_backend.diet_engine import generate_meal_plan
from fastapi import Header
import json

router = APIRouter(prefix="/diet", tags=["Diet"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    email = decode_access_token(token)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()
    return user


@router.post("/generate/{public_pet_id}")
def generate_diet(
    public_pet_id: str,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(
        models.Pet.public_pet_id == public_pet_id,
        models.Pet.owner_id == user.id
    ).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    user_data = {
        "pet_type": "dog",  # You can improve this later
        "age_group": "adult",
        "breed": pet.breed,
        "weight": pet.weight,
        "activity_level": "moderate",
        "health_conditions": [],
        "allergies": [],
        "diet_type": "nonveg",
        "budget_limit": 5000
    }

    plan = generate_meal_plan(user_data)

    new_plan = models.DietPlan(
        pet_id=pet.id,
        plan_data=json.dumps(plan)
    )

    db.add(new_plan)
    db.commit()
@router.get("/history/{public_pet_id}")
def diet_history(
    public_pet_id: str,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(
        models.Pet.public_pet_id == public_pet_id,
        models.Pet.owner_id == user.id
    ).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    plans = (
        db.query(models.DietPlan)
        .filter(models.DietPlan.pet_id == pet.id)
        .order_by(models.DietPlan.created_at.desc())
        .all()
    )

    return [
        {
            "id": plan.id,
            "created_at": plan.created_at,
            "plan_data": json.loads(plan.plan_data)
        }
        for plan in plans
    ]
    return plan