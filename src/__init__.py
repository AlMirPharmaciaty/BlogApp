from fastapi import FastAPI
from .utils.database import init_db
from .api import blog, auth, user

app = FastAPI()


def blog_app():
    init_db()
    app.include_router(blog.blogs)
    app.include_router(auth.auth)
    app.include_router(user.users)

    return app
