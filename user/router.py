from datetime import timedelta

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import config
from database import get_db
from . import schema, models, auth
from user.auth import Password

router = APIRouter(
    tags=['user'],
    prefix='/user'
)

settings = config.get_settings()


# Create user
@router.post(path='/register', status_code=status.HTTP_201_CREATED, response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(get_db)):
    user = (models.User(name=request.name, email=request.email, password=Password(request.password).encrypt()))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Login user
@router.post(path='/login', status_code=status.HTTP_201_CREATED)
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    if not Password(password=request.password, hashed_password=user.password).verify():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect email or password')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires,)
    return {"access_token": access_token, "token_type": "bearer"}

