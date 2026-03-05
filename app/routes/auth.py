from fastapi import APIRouter,Depends, app
from app.models.auth import Signup
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated
from app.database.schema.user_schema import UserSchema
from fastapi.responses import JSONResponse

router=APIRouter(prefix="/auth")

@router.post("/signup")
def signup(data:Signup, db:Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if user:
        return JSONResponse(status_code=400, content={"message":"Email already exists"})
    user = UserSchema(
        name=data.name,
        email=data.email,
        hashed_password=data.hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#@router.post("/login")
#def login():