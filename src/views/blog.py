from abc import abstractmethod
from sqlalchemy.orm import Session
from starlette_admin.contrib.sqla import ModelView
from starlette.requests import Request
from ..models.blog import Blog


class BlogView(ModelView):
    """
    Blog admin UI configuration
    """

    exclude_fields_from_create = exclude_fields_from_edit = [
        Blog.slug,
        Blog.datetime_created,
        Blog.datetime_updated,
        Blog.deleted,
    ]

    # @abstractmethod
    # async def find_all(
    #     self,
    #     request: Request,
    #     skip: int = 0,
    #     limit: int = 10,
    #     where: list[dict[str, any], str, None] = None,
    #     order_by: list[str] = ["datetime_created desc"],
    # ):
    #     db: Session = request.state.session
    #     user_id = request.state.user
    #     query = db.query(Blog).filter(Blog.author_id == user_id, Blog.deleted == False)
    #     if where:
    #         pass
    #     query = query.order_by(Blog.datetime_created.desc())
    #     return query.offset(skip).limit(limit).all()

    async def before_create(self, request: Request, data: dict[str, any], obj: Blog):
        await slug_maker(request, blog=obj)

    async def before_edit(self, request: Request, data: dict[str, any], obj: Blog):
        await slug_maker(request, blog=obj)

    async def delete(self, request: Request, pks: list[int]):
        from ..controllers.blog import delete_blog

        db: Session = request.state.session
        delete_blog(db=db, blog_id=pks[0], user_id=request.state.user)


async def slug_maker(request: Request, blog: Blog):
    from ..utils.database import session
    from ..controllers.blog import create_slug

    db: Session = session()
    blog.slug = create_slug(blog.title, db=db)
