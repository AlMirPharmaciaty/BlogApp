# Importing modules from the 'src' folder
# 'blog_app' is an FastAPI application
# 'admin' is a Starlette application
from src import blog_app, admin


app = blog_app()
# app = admin()


# Home/landing page
@app.get("/")
def home():
    return "Blog App - See APIs at /docs"
