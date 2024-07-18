from datetime import datetime
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from ..models import User
from ..utils.encryption import verify
from ..utils.database import get_db

auth = APIRouter(prefix="/auth")

SECRET_KEY = "asdasfasfasfesdfsd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


class Token(BaseModel):
    access_token: str
    token_type: str


@auth.post("/login/", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email, User.is_active).first()
    return user


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not verify(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except InvalidTokenError as e:
        raise credentials_exception from e
    user = get_user(email=user_email, db=db)
    if user is None:
        raise credentials_exception
    return user
