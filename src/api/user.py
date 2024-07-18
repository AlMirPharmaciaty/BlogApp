from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..schemas.user import UserDetails, UserCreate, UserUpdate
from ..controllers.user import create_user, update_user, delete_user
from ..models import User
from .auth import get_current_user

users = APIRouter(prefix="/users", tags=["Users"])


@users.post("/", response_model=UserDetails)
def user_create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@users.put("/", response_model=UserDetails)
def user_update(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_user(db=db, user=user, user_id=current_user.id)


@users.delete("/", response_model=UserDetails)
def user_delete(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return delete_user(db=db, user_id=user.id)
