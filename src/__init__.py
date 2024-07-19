"""
This module initializes and configures the application components

It contains two main functions:
- `blog_app()`: Initializes the FastAPI application
- `admin_app()`: Sets up the Starlette Admin interface

Both functions call `init_db()` to ensure the database is properly
initialized before setting up the application components.
"""

from fastapi import FastAPI
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView
from .utils.database import init_db
from .utils.database import engine
from .api import blog, auth, user
from .models import Blog, User


def blog_app():
    """
    Initialize and configure the FastAPI application with necessary routes and database setup.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI()
    init_db()
    app.include_router(blog.blogs)
    app.include_router(auth.auth)
    app.include_router(user.user)
    return app


def admin_app():
    """
    Set up the Starlette Admin interface for database model management.

    Returns:
        Starlette: The Starlette application instance with the admin interface mounted.
    """
    init_db()
    app = Starlette()
    admin = Admin(engine, title="Blog App Admin")
    admin.add_view(ModelView(Blog))
    admin.add_view(ModelView(User))
    admin.mount_to(app)
    return app
