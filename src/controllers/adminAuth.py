from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed
from sqlalchemy.orm import Session
from ..utils.encryption import encrypt
from ..models.user import User


class MyAuthProvider(AuthProvider):
    """
    This is for demo purpose, it's not a better
    way to save and validate user credentials
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        email = username
        db: Session = request.state.session
        user = (
            db.query(User)
            .filter(User.email == email, User.password == encrypt(password))
            .first()
        )
        if user:
            request.session.update({"user": user.id})
            return response

        raise LoginFailed("Incorrect email or password")

    async def is_authenticated(self, request) -> bool:
        user = request.session.get("user", None)
        db: Session = request.state.session
        if user:
            user = db.query(User).filter(User.id == user).first()
        if user:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = user.id
            return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        # Update app title according to current_user
        db: Session = request.state.session
        user: User | None = db.query(User).filter(User.id == user).first()
        custom_app_title = "Hello, " + user.username + "!"
        # Update logo url according to current_user
        custom_logo_url = None
        return AdminConfig(
            app_title=custom_app_title,
            logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        db: Session = request.state.session
        user: User | None = db.query(User).filter(User.id == user).first()
        photo_url = None
        return AdminUser(username=user.username, photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
