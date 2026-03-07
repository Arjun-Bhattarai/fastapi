from fastapi import APIRouter, Depends
from app.models.auth import Signup, Login
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated
from app.database.schema.user_schema import UserSchema
from fastapi.responses import JSONResponse
from app.helper import hash_password,verify_password, create_access_token

router = APIRouter()

@router.post("/login")
def login(data: Login, db: Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        return JSONResponse(status_code=400, content={"message": "Invalid email or password"})
    payload = {
        "id": user.id,
        "name": user.name,
        "email": user.email
        }
    access_token = create_access_token(payload)
    payload["access_token"] = "Bearer " + access_token

    
    return {
        "message": "Login successful","data": payload
    }

 
@router.post("/signup")
def signup(data: Signup, db: Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.email == data.email).first()

    if user:
        return JSONResponse(status_code=400, content={"message": "Email already exists"})

    user = UserSchema(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password)  
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
