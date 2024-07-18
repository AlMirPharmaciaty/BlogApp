from fastapi import APIRouter, Depends, HTTPException, Query
from ..utils.database import get_db
from ..schemas.blog import BlogDetails, BlogCreate, BlogUpdate
from sqlalchemy.orm import Session
from ..controllers.blog import (
    create_blog,
    get_all_blogs,
    delete_blog,
    update_blog,
    BlogSortingOptions,
)
from ..models import User
from .auth import get_current_user

blogs = APIRouter(prefix="/blogs")


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
    id: int = None,
    title: str = None,
    description: str = None,
    content: str = None,
    tag: str = None,
    author: str = None,
    sort: BlogSortingOptions = Query(BlogSortingOptions.new, alias="Sort by"),
    skip: int = 0,
    limit: int = 10,
):
    blogs = get_all_blogs(
        db=db,
        id=id,
        title=title,
        description=description,
        content=content,
        tag=tag,
        author=author,
        sort=sort,
        skip=skip,
        limit=limit,
    )
    return blogs


@blogs.put("/{blog_id}", response_model=BlogDetails)
def update_item(
    blog_id: int,
    blog: BlogUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        blog = update_blog(db=db, blog_id=blog_id, blog=blog, user_id=user.id)
        return blog
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Blog not found")


@blogs.delete("/{blog_id}", response_model=BlogDetails)
def blog_delete(
    blog_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    try:
        blog = delete_blog(db=db, blog_id=blog_id, user_id=user.id)
        return blog
    except:
        raise HTTPException(status_code=404, detail="Blog not found")
