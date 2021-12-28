import re

from ..errors import ErrorResponse
from ..lib import render_template
from ..main.controllers import get_popular_posts


# Build router for request method and give 403 is wrong
def router(environ, response):
    url = environ["PATH_INFO"]
    http_method = environ["REQUEST_METHOD"]

    if http_method == "GET":
        if re.compile("^\/$").match(url):  # Accepts "/"
            return get_popular_posts(environ, response)
        if re.compile("\/new(\/)?").match(url):  # Accepts /new
            return render_template("new-post.html", response, {"title": "Write a post"})
    else:
        # If noting matched then show 405
        error_message = f"{http_method} is not ALLOWED on {url}"
        raise ErrorResponse(405, error_message)
