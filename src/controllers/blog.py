from ..models import Blog, User
from ..schemas.blog import BlogCreate, BlogUpdate
from sqlalchemy.orm import Session
from urllib import parse
from sqlalchemy import func
from enum import Enum
from fastapi import Query


# Function to create a blog
def create_blog(blog: BlogCreate, db: Session, author_id: int):
    slug = create_slug(blog.title, db)
    new_blog = Blog(**blog.model_dump(), slug=slug, author_id=author_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Function to generate a slug URL for the blog
def create_slug(title, db: Session):
    # replace spaces with hyphen
    slug = title.replace(" ", "-").lower()
    # make url safe
    slug = parse.quote(slug)
    # get number of blogs with same url
    existing_blogs = db.query(Blog).filter(Blog.slug.startswith(slug)).count()
    # if there are blogs with same url
    if existing_blogs > 0:
        # increment by one
        slug += f"-{str(existing_blogs + 1)}"
    return slug


class BlogSortingOptions(str, Enum):
    new = "Latest"
    old = "Oldest"


# Function to filter (optional) and get all blogs
def get_all_blogs(
    db: Session,
    id: int = None,
    title: str = None,
    description: str = None,
    content: str = None,
    tag: str = None,
    author: str = None,
    sort: BlogSortingOptions = Query(BlogSortingOptions.new),
    skip: int = 0,
    limit: int = 10,
):

    query = db.query(Blog).filter(Blog.is_active == True)
    if id:
        query = query.filter(Blog.id == id)
    if title:
        query = query.filter(func.lower(Blog.title).contains(title.lower()))
    if description:
        query = query.filter(func.lower(Blog.description).contains(description.lower()))
    if content:
        query = query.filter(func.lower(Blog.content).contains(content.lower()))
    if tag:
        query = query.filter(func.lower(Blog.tags).contains(tag.lower()))
    if author:
        query = query.join(User).filter(
            func.lower(User.username).contains(author.lower())
        )
    if sort.name == "old":
        query = query.order_by(Blog.datetime_created.asc())
    else:
        query = query.order_by(Blog.datetime_created.desc())
    blogs = query.offset(skip).limit(limit).all()
    return blogs


# Function to update a blog
def update_blog(db: Session, blog_id: int, blog: BlogUpdate, user_id: int):
    old_blog = (
        db.query(Blog)
        .filter(Blog.id == blog_id, Blog.author_id == user_id, Blog.is_active == True)
        .first()
    )

    if old_blog:
        # Check if blog title has changed
        if old_blog.title != blog.title:
            # Update blog URL
            old_blog.slug = create_slug(blog.title, db)
        old_blog.title = blog.title
        old_blog.description = blog.description
        old_blog.content = blog.content
        old_blog.tags = blog.tags
        db.commit()
        db.refresh(old_blog)
    return old_blog


# Function to delete a blog
def delete_blog(db: Session, blog_id: int, user_id: int):
    blog = (
        db.query(Blog)
        .filter(Blog.id == blog_id, Blog.author_id == user_id, Blog.is_active == True)
        .first()
    )
    if blog:
        blog.is_active = False
        db.commit()
    return blog
