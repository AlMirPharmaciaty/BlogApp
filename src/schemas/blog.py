from datetime import datetime
from pydantic import BaseModel
from ..schemas.user import UserDetails


class BlogBase(BaseModel):
    title: str
    description: str
    content: str
    tags: str


class BlogDetails(BlogBase):
    id: int
    deleted: bool
    datetime_created: datetime
    datetime_updated: datetime
    author_id: int
    slug: str
    author: UserDetails


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BlogBase):
    title: str | None = None
    description: str | None = None
    content: str | None = None
    tags: str | None = None
