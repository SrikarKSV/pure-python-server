import re

import bleach
import markdown

from ..db import Post, create_session
from ..errors.ErrorResponse import ErrorResponse
from ..lib import HTTP_MESSAGE, parse_get_form, parse_post_form, render_template
from ..lib.utils import ALLOWED_ATTRIBUTES, ALLOWED_TAGS


def get_all_posts(environ, response):
    session = create_session()
    total_posts = session.query(Post).count()
    per_page = 5
    query_strings = parse_get_form(environ)
    try:
        page = int(query_strings.get("page", 1))
    except:
        page = 1
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

    url = f"https://{environ['REMOTE_HOST']}{environ['PATH_INFO']}"
    title = "All posts"
    description = "Browse all the articles of PyProject!"
    context = {
        "title": title,
        "posts": posts,
        "prev_page": prev_page,
        "next_page": next_page,
        "url": url,
        "description": description,
    }
    return render_template("all-posts.html", response, context)


def get_post(environ, response):
    try:
        post_id = int(
            re.compile("^\/posts\/(?P<id>\d{1,})(\/)?$")
            .search(environ["PATH_INFO"])
            .groupdict()["id"]
        )
    except:
        raise ErrorResponse(400, "There was an error when parsing article id")

    session = create_session()
    post = session.query(Post).get(post_id)
    if not post:
        raise ErrorResponse(404, "Post not found")

    # Increment view count by 1
    post.view_count += 1
    session.commit()

    url = f"https://{environ['REMOTE_HOST']}{environ['PATH_INFO']}"
    description = "Read an article on PyProject"
    context = {
        "title": post.title,
        "post": post,
        "url": url,
        "description": description,
    }
    return render_template("post.html", response, context)


def create_post(environ, response):
    data = parse_post_form(environ)
    title = data.get("title", "")
    name = data.get("name", "")
    content = data.get("content", "")
    if not title or not content or not name:
        raise ErrorResponse(422, "Fill all fields before submitting")

    if len(title) > 100:
        raise ErrorResponse(422, "Title should have a maximum length of 100 characters")

    if len(name) > 8:
        raise ErrorResponse(422, "Name should have a maximum length of 100 characters")

    session = create_session()
    # Convert HTML to markdown and sanitize
    html_content = markdown.markdown(
        content, extensions=["fenced_code", "codehilite", "tables", "abbr"]
    )
    sanitized_html = bleach.clean(
        html_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
    )
    post = Post(title=title, name=name, markdown=content, content=sanitized_html)
    session.add(post)
    session.commit()
    # Redirect to /posts/id
    response(HTTP_MESSAGE[303], [("Location", f"/posts/{post.id}")])
    return [b""]


def get_edit(environ, response):
    try:
        post_id = int(
            re.compile("^\/posts\/(?P<id>\d{1,})\/edit(\/)?$")
            .search(environ["PATH_INFO"])
            .groupdict()["id"]
        )
    except:
        raise ErrorResponse(400, "There was an error when parsing article id")

    session = create_session()
    post = session.query(Post).get(post_id)
    if not post:
        raise ErrorResponse(404, "Post not found")

    url = f"https://{environ['REMOTE_HOST']}{environ['PATH_INFO']}"
    description = "Edit a post on PyProject"
    title = "Edit post"
    context = {"title": title, "post": post, "url": url, "description": description}
    return render_template("edit-post.html", response, context)


def post_edit(environ, response):
    data = parse_post_form(environ)
    post_id = data.get("id", "")
    title = data.get("title", "")
    name = data.get("name", "")
    content = data.get("content", "")
    if not title or not content:
        raise ErrorResponse(422, "Fill all fields before submitting")
    if not post_id:
        raise ErrorResponse(422, "Id of the post not given")

    if len(title) > 100:
        raise ErrorResponse(422, "Title should have a maximum length of 100 characters")

    if len(name) > 8:
        raise ErrorResponse(422, "Name should have a maximum length of 100 characters")

    session = create_session()
    post = session.query(Post).get(post_id)
    if not post:
        raise ErrorResponse(404, "Post not found to edit")

    # Convert HTML to markdown and sanitize
    html_content = markdown.markdown(content, extensions=["fenced_code", "codehilite"])
    sanitized_html = bleach.clean(
        html_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
    )
    post.title = title
    post.name = name
    post.markdown = content
    post.content = sanitized_html
    session.commit()
    # Redirect to /posts/id
    response(HTTP_MESSAGE[303], [("Location", f"/posts/{post.id}")])
    return [b""]


def delete_post(environ, response):
    post_id = int(
        re.compile("^\/posts\/(?P<id>\d{1,})\/delete(\/)?$")
        .search(environ["PATH_INFO"])
        .groupdict()["id"]
    )
    session = create_session()
    session.query(Post).filter(Post.id == post_id).delete(synchronize_session=False)
    session.commit()
    # Redirect to /posts
    response(HTTP_MESSAGE[303], [("Location", "/posts")])
    return [b""]
