import datetime

from ..db import Post, create_session
from ..lib.serve_files import render_template


def get_popular_posts(environ, response):
    session = create_session()
    today = datetime.datetime.utcnow()
    week_ago = today - datetime.timedelta(days=7)
    # Get most viewed posts in last 7 days
    popular_posts = (
        session.query(Post)
        .filter(Post.created_at > week_ago)
        .order_by(Post.view_count.desc())
        .limit(5)
        .all()
    )

    url = f"https://{environ['REMOTE_HOST']}{environ['PATH_INFO']}"
    title = "Home"
    description = "A blogging platform written in pure python (no web frameworks used!) for developer to share their coding knowledge"
    context = {
        "popular_posts": popular_posts,
        "title": title,
        "url": url,
        "description": description,
    }
    return render_template("index.html", response, context)
