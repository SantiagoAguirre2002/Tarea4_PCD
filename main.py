from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn
from typing import Optional

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    name: str = Field(min_length=1)
    id: int = Field(gt=-1, lt=101)
    email: str = Field(min_length=1, max_length=5000)
    age: Optional[int] = None
    recommendations: str = Field(default_factory=list)
    zip:Optional[str]= None

@app.post("/")
def create_user(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        # Si el usuario ya existe, devuelve un mensaje de error
        raise HTTPException(
            status_code=400,
            detail=f"The email {user.email} was registered ."
        )

    user_model = models.Users()
    user_model.name = user.name
    user_model.id = user.id
    user_model.email = user.email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.zip = user.zip

    db.add(user_model)
    db.commit()


    return user

@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

#operación put es para ACTUALIZAR
@app.put("/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
#where la columna de id coincida con la que yo le estoy dando
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )
    #user_model = models.Users()
    user_model.name = user.name
    user_model.id = user.id
    user_model.email = user.email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.zip = user.zip

    db.add(user_model)
    db.commit()

    return user_model

@app.get("/{user_id}")
def read_api(user_id: int,db: Session = Depends(get_db)):
    user_id = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )
    return db.query(models.Users).all()


@app.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    book_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    db.query(models.Users).filter(models.Users.id == user_id).delete()

    db.commit()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=50, log_level="info", reload=True)