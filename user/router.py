from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from database import get_db
from . import schema, models
from user.passwords import Password

router = APIRouter()


# Create user
@router.post(path='/user', status_code=status.HTTP_201_CREATED, response_model=schema.ShowUser, tags=['user'])
def create_user(request: schema.User, db: Session = Depends(get_db)):
    user = (models.User(name=request.name, email=request.email, password=Password(request.password).encrypt()))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
