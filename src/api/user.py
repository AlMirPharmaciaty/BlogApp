from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..schemas.user import UserDetails, UserUpdate
from ..controllers.user import update_user, delete_user
from ..models import User
from ..controllers.auth import get_current_user

user = APIRouter(prefix="/user", tags=["User"])


@user.put("/", response_model=UserDetails)
def user_update(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_user(db=db, user=user, user_id=current_user.id)


@user.delete("/", response_model=UserDetails)
def user_delete(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return delete_user(db=db, user_id=user.id)
