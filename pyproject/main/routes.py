import re

from pyproject.errors import ErrorResponse
from pyproject.lib import render_template
from pyproject.main.controllers import get_popular_posts


# Build router for request method and give 403 is wrong
def router(environ, response):
    url = environ["PATH_INFO"]
    http_method = environ["REQUEST_METHOD"]

    if http_method == "GET":
        if re.compile("^\/$").match(url):
            return get_popular_posts(environ, response)
        if re.compile("\/new(\/)?").match(url):
            return render_template("new-post.html", response, {"title": "Write a post"})
    else:
        error_message = f"{http_method} is not ALLOWED on {url}"
        raise ErrorResponse(405, error_message)
