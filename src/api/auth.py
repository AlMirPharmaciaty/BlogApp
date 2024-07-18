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

auth = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "asdasfasfasfesdfsd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


class Token(BaseModel):
    """
    Represents an authentication token object

    Attributes:
        access_token: The actual token string used for authentication
        token_type: The type of the token, typically "Bearer" for OAuth tokens
    """

    access_token: str
    token_type: str


@auth.post("/login/", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Endpoint to let users log into the system
    they are first authenticated by username and password
    if verified, a token is created and sent to them
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


def get_user(email: str, db: Session):
    """
    Function to get the active user from db by email
    """
    user = db.query(User).filter(User.email == email, User.is_active).first()
    return user


def authenticate_user(email: str, password: str, db: Session):
    """
    Function to authenticate user by email and password
    the given password is verified using md5 encryption
    see utils/encryption
    """
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not verify(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Function to create a JWT token
    - expiry time is set to provided mins from request
    - a data which is user credentials are encrypted
        - by a secret key using HS256 algorithm
    """
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
    """
    Function to get active user
    a token is retrieved from the client
    and decoded using the same secret key and algorithm as the above function
    then the user credentials are matched with the existing records in the db
    """
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
