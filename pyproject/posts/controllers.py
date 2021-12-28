import re

import bleach
import markdown
from pyproject.errors.ErrorResponse import ErrorResponse
from pyproject.lib import HTTP_MESSAGE, parse_get_form, parse_post_form, render_template
from pyproject.lib.utils import ALLOWED_ATTRIBUTES, ALLOWED_TAGS
from pyproject.models import Post, session


def get_all_posts(environ, response):
    total_posts = session.query(Post).count()
    per_page = 5
    query_strings = parse_get_form(environ)
    page = int(query_strings.get("page", 1))
    skip = per_page * (page - 1)
    # If page exceeds total posts count then it's reset to 1
    page = page if total_posts >= skip else 1
    skip = per_page * (page - 1)
    query = (
        session.query(Post)
        .order_by(Post.created_at.desc())
        .limit(per_page)
        .offset(skip)
    )
    posts = session.execute(query).scalars().all()

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if skip + len(posts) < total_posts else None

    context = {
        "title": "All posts",
        "posts": posts,
        "prev_page": prev_page,
        "next_page": next_page,
    }

    return render_template("all-posts.html", response, context)


def get_post(environ, response):
    post_id = int(
        re.compile("^\/posts\/(?P<id>\d{1,})(\/)?$")
        .search(environ["PATH_INFO"])
        .groupdict()["id"]
    )
    post = session.query(Post).get(post_id)
    if not post:
        raise ErrorResponse(404, "Post not found")

    post.view_count += 1
    session.commit()
    context = {"title": post.title, "post": post}
    return render_template("post.html", response, context)


def create_post(environ, response):
    data = parse_post_form(environ)
    title = data.get("title", "")
    content = data.get("content", "")
    if not title or not content:
        raise ErrorResponse(422, "Fill both title and article body before submitting")
    html_content = markdown.markdown(content, extensions=["fenced_code", "codehilite"])
    sanitized_html = bleach.clean(
        html_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
    )
    post = Post(title=title, content=sanitized_html)
    session.add(post)
    session.commit()
    response(HTTP_MESSAGE[303], [("Location", f"/posts/{post.id}")])
    return [b""]


def get_edit(environ, response):
    post_id = int(
        re.compile("^\/posts\/(?P<id>\d{1,})\/edit(\/)?$")
        .search(environ["PATH_INFO"])
        .groupdict()["id"]
    )
    post = session.query(Post).get(post_id)
    if not post:
        raise ErrorResponse(404, "Post not found")
    context = {"title": "Edit post", "post": post}
    return render_template("edit-post.html", response, context)


def post_edit(environ, response):
    data = parse_post_form(environ)
    post_id = data.get("id", "")
    title = data.get("title", "")
    content = data.get("content", "")
    if not title or not content:
        raise ErrorResponse(422, "Fill both title and article body before submitting")
    if not post_id:
        raise ErrorResponse(422, "Id of the post not given")

    post = session.query(Post).get(post_id)
    if not post:
        raise ErrorResponse(404, "Post not found to edit")

    html_content = markdown.markdown(content, extensions=["fenced_code", "codehilite"])
    sanitized_html = bleach.clean(
        html_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
    )
    post.title = title
    post.content = sanitized_html
    session.commit()
    response(HTTP_MESSAGE[303], [("Location", f"/posts/{post.id}")])
    return [b""]


def delete_post(environ, response):
    post_id = int(
        re.compile("^\/posts\/(?P<id>\d{1,})\/delete(\/)?$")
        .search(environ["PATH_INFO"])
        .groupdict()["id"]
    )
    session.query(Post).filter(Post.id == post_id).delete(synchronize_session=False)
    session.commit()
    response(HTTP_MESSAGE[303], [("Location", "/posts")])
    return [b""]
