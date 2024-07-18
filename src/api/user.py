from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..schemas.user import UserDetails, UserCreate
from ..controllers.user import create_user

users = APIRouter(prefix="/users")


@users.post("/", response_model=UserDetails)
def user_create(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db=db, user=user)
    return new_user
