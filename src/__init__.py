from fastapi import FastAPI
from .utils.database import init_db
from .api import blog, auth, user

from .models import Blog, User
from .utils.database import engine
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView


def blog_app():
    app = FastAPI()
    init_db()
    app.include_router(blog.blogs)
    app.include_router(auth.auth)
    app.include_router(user.users)
    return app


def admin():
    init_db()
    app = Starlette()
    admin = Admin(engine, title="Blog App Admin")
    admin.add_view(ModelView(Blog))
    admin.add_view(ModelView(User))
    admin.mount_to(app)
    return app
