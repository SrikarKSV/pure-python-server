import re

from pyproject.errors import ErrorResponse

from .controllers import create_post, get_all_posts, get_edit, get_post, post_edit


# Build router for request method and give 403 is wrong
def router(environ, response):
    url = environ["PATH_INFO"]
    http_method = environ["REQUEST_METHOD"].upper()

    if http_method == "GET":
        if re.compile("^\/posts(\/)?$").match(url):
            return get_all_posts(environ, response)
        if re.compile("^\/posts\/\d{1,}(\/)?$").match(url):
            return get_post(environ, response)
        if re.compile("^\/posts\/\d{1,}\/edit(\/)?$").match(url):
            return get_edit(environ, response)
    elif http_method == "POST":
        if re.compile("^\/posts(\/)?$").match(url):
            return create_post(environ, response)
        if re.compile("^\/posts\/\d{1,}\/edit(\/)?$").match(url):
            return post_edit(environ, response)
        if re.compile("^\/posts\/\d{1,}\/delete(\/)?$").match(url):
            return [b"Post deleted"]
    else:
        error_message = f"{http_method} is not ALLOWED on {url}"
        raise ErrorResponse(405, error_message)
