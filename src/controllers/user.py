from sqlalchemy.orm import Session
from ..models import User
from ..utils.encryption import encrypt
from ..schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    user = User(**user.model_dump())
    user.password = encrypt(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: UserUpdate, user_id=int):
    old_user = db.query(User).filter(User.id == user_id).first()
    if old_user:
        if user.username:
            old_user.username = user.username
        if user.email:
            old_user.email = user.email
        if user.password:
            if old_user.password != user.password:
                old_user.password = encrypt(user.password)
        db.commit()
        db.refresh(old_user)
    return old_user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = False
        db.commit()
    return user
