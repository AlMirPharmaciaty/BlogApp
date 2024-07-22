from fastapi.responses import HTMLResponse
from src import blog_app

app = blog_app()


@app.get("/", response_class=HTMLResponse)
def home():
    content = """
    <h1>BlogApp - API</h1>
    <ul>
    <li><h3><a href="/docs">API Documentation</a></h3></li>
    <li><h3><a href="/admin">Administrative Interface</a></h3></li>
    </ul>
    """
    return content
