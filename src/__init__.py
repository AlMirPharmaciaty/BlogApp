"""
This module initializes and configures the application components
- `blog_app()`: Initializes the FastAPI application
"""

from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from .utils.database import init_db
from .utils.database import engine
from .api import blog, auth, user
from .models.blog import Blog
from .models.user import User
from .views.blog import BlogView
from .controllers.adminAuth import MyAuthProvider


def blog_app():
    """
    Initialize and configure the FastAPI application with necessary routes and database setup.
    along with starlette-admin

    Returns:
        FastAPI: The configured FastAPI application instance.
    """

    init_db()

    app = FastAPI()
    app.include_router(blog.blogs)
    app.include_router(auth.auth)
    app.include_router(user.users)

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
