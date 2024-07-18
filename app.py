from src import blog_app, admin


app = blog_app()
# app = admin()


@app.get("/")
def home():
    return "Blog App - See APIs at /docs"
