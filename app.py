from src import blog_app


app = blog_app()


@app.get("/")
def home():
    return "Blog App - See APIs at /docs"
