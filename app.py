"""
Importing modules from the 'src' folder
- 'blog_app' is an FastAPI application
- 'admin' is a Starlette application
"""

from src import blog_app  # , admin_app


app = blog_app()
# app = admin_app()


@app.get("/")
def home():
    """
    Home/landing page
    """
    return "Blog App - See APIs at /docs"
