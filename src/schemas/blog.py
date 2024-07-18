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
    is_active: bool
    datetime_created: datetime
    datetime_updated: datetime
    author_id: int
    slug: str
    author: UserDetails


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BlogBase):
    pass
