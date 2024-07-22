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
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from .utils.database import init_db
from .utils.database import engine
from .api import blog, auth, user
from .models.blog import Blog, BlogView
from .models.user import User
from .starlette_files.auth import MyAuthProvider


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
    app.include_router(user.users)
    return app


def admin_app():
    """
    Set up the Starlette Admin interface for database model management.

    Returns:
        Starlette: The Starlette application instance with the admin interface mounted.
    """
    init_db()
    app = Starlette()
    admin = Admin(
        engine,
        title="Blog App Admin",
        auth_provider=MyAuthProvider(),
        middlewares=[Middleware(SessionMiddleware, secret_key="123456")],
    )
    admin.add_view(BlogView(Blog))
    admin.add_view(ModelView(User))
    admin.mount_to(app)
    return app
