from enum import Enum
from urllib import parse
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Blog, User
from ..schemas.blog import BlogCreate, BlogUpdate


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
    """
    Function to generate a slug URL for the blog by
    - replacing spaces with hyphen
    - making url safe
    - cheking if the url already exists
        - if yes, adding an incremented value at the end of the url
    """
    slug = title.replace(" ", "-").lower()
    slug = parse.quote(slug)
    existing_blogs = db.query(Blog).filter(Blog.slug.startswith(slug)).count()
    if existing_blogs > 0:
        slug += f"-{str(existing_blogs + 1)}"
    return slug


class BlogSortingOptions(str, Enum):
    """
    asc and desc sorting options for blogs by datetime
    """

    NEW = "Latest"
    OLD = "Oldest"


# Function to filter (optional) and get all blogs
def get_all_blogs(
    db: Session,
    blog_id: int = None,
    title: str = None,
    description: str = None,
    content: str = None,
    tag: str = None,
    author: str = None,
    sort: BlogSortingOptions = Query(BlogSortingOptions.NEW),
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieves a list of blog posts based on various filters and sorting parameters
    """
    query = db.query(Blog).filter(Blog.is_active)
    if blog_id:
        query = query.filter(Blog.id == blog_id)
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
    if sort.name == "OLD":
        query = query.order_by(Blog.datetime_created.asc())
    else:
        query = query.order_by(Blog.datetime_created.desc())
    blogs = query.offset(skip).limit(limit).all()
    return blogs


# Function to update a blog
def update_blog(db: Session, blog_id: int, blog: BlogUpdate, user_id: int):
    old_blog = (
        db.query(Blog)
        .filter(Blog.id == blog_id, Blog.author_id == user_id, Blog.is_active)
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
        .filter(Blog.id == blog_id, Blog.author_id == user_id, Blog.is_active)
        .first()
    )
    if blog:
        blog.is_active = False
        db.commit()
    return blog
