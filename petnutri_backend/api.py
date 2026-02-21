from fastapi import FastAPI
from pydantic import BaseModel
from petnutri_backend.diet_engine import generate_meal_plan
from petnutri_backend.routes import pets
from petnutri_backend.database.db import engine, Base
import petnutri_backend.database.models
from petnutri_backend.routes import auth
from petnutri_backend.routes import diet
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(pets.router)
app.include_router(diet.router)
from petnutri_backend.routes import diet
class UserInput(BaseModel):
    pet_type: str
    age_group: str
    breed: str
    weight: float
    activity_level: str
    health_conditions: list
    allergies: list
    diet_type: str
    budget_limit: float


@app.post("/generate")
def generate(user: UserInput):
    return generate_meal_plan(user.dict())