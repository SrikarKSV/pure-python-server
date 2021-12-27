import datetime

from pyproject.lib.serve_files import render_template
from pyproject.models import Post, session


def get_popular_posts(environ, response):
    today = datetime.datetime.utcnow()
    week_ago = today - datetime.timedelta(days=7)
    popular_posts = (
        session.query(Post)
        .filter(Post.created_at > week_ago)
        .order_by(Post.view_count.desc())
        .limit(5)
        .all()
    )

    context = {"popular_posts": popular_posts}
    return render_template("index.html", response, context)