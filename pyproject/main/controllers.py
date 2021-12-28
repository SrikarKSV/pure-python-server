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

    context = {"popular_posts": popular_posts}
    return render_template("index.html", response, context)
