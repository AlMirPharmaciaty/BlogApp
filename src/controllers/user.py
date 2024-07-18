from sqlalchemy.orm import Session
from ..models import User
from ..utils.encryption import encrypt
from ..schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    user = User(**user.model_dump())
    user.password = encrypt(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
