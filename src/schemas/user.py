from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    pass


class UserDetails(UserBase):
    id: int
    username: str
    email: str
    password: str
    is_active: bool


class UserCreate(UserBase):
    username: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(min_length=4)
