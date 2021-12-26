from pyproject.errors.ErrorResponse import ErrorResponse
from pyproject.lib import parse_post_form
from pyproject.models import Post, session
from pyproject.lib import HTTP_MESSAGE


def create_post(environ, response):
    data = parse_post_form(environ)
    title = data.get("title", "")
    content = data.get("content", "")
    if not title or not content:
        raise ErrorResponse(422, "Fill both title and article body before submitting")
    post = Post(title=title, content=content)
    session.add(post)
    session.commit()
    response(HTTP_MESSAGE[303], [("Location", f"/posts/{post.id}")])
    return [b""]
