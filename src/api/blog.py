from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..schemas.blog import BlogDetails, BlogCreate, BlogUpdate
from ..utils.database import get_db
from ..controllers.blog import (
    create_blog,
    get_all_blogs,
    delete_blog,
    update_blog,
    BlogSortingOptions,
)
from ..models import User
from ..controllers.auth import get_current_user

blogs = APIRouter(prefix="/blogs", tags=["Blogs"])


@blogs.post("/", response_model=BlogDetails)
def blog_create(
    blog: BlogCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    blog = create_blog(blog=blog, db=db, author_id=user.id)
    return blog


@blogs.get("/", response_model=list[BlogDetails])
def blog_get_all(
    db: Session = Depends(get_db),
    blog_id: int = None,
    title: str = None,
    description: str = None,
    content: str = None,
    tag: str = None,
    author: str = None,
    sort: BlogSortingOptions = Query(BlogSortingOptions.NEW, alias="Sort by"),
    skip: int = 0,
    limit: int = 10,
):
    blog_list = get_all_blogs(
        db=db,
        blog_id=blog_id,
        title=title,
        description=description,
        content=content,
        tag=tag,
        author=author,
        sort=sort,
        skip=skip,
        limit=limit,
    )
    return blog_list


@blogs.put("/{blog_id}", response_model=BlogDetails)
def blog_update(
    blog_id: int,
    blog: BlogUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    blog = update_blog(db=db, blog_id=blog_id, blog=blog, user_id=user.id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@blogs.delete("/{blog_id}", response_model=BlogDetails)
def blog_delete(
    blog_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    blog = delete_blog(db=db, blog_id=blog_id, user_id=user.id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
