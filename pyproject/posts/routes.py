import re
import typing as t

from ..errors import ErrorResponse
from .controllers import (
    create_post,
    delete_post,
    get_all_posts,
    get_edit,
    get_post,
    post_edit,
)


# Build router for request method and give 403 is wrong
def router(environ: dict, response: t.Callable) -> t.List[bytes]:
    url = environ["PATH_INFO"]
    http_method = environ["REQUEST_METHOD"].upper()

    if http_method == "GET":
        if re.compile("^\/posts(\/)?$").match(url):  # Accepts /posts
            return get_all_posts(environ, response)
        if re.compile("^\/posts\/\d{1,}(\/)?$").match(url):  # Accepts /posts/id
            return get_post(environ, response)
        if re.compile("^\/posts\/\d{1,}\/edit(\/)?$").match(
            url
        ):  # Accepts /posts/id/edit
            return get_edit(environ, response)
    elif http_method == "POST":
        if re.compile("^\/posts(\/)?$").match(url):  # Accepts /posts
            return create_post(environ, response)
        if re.compile("^\/posts\/\d{1,}\/edit(\/)?$").match(
            url
        ):  # Accepts /posts/id/edit
            return post_edit(environ, response)
        if re.compile("^\/posts\/\d{1,}\/delete(\/)?$").match(
            url
        ):  # Accepts /posts/id/delete
            return delete_post(environ, response)
    else:
        # If noting matched then show 405
        error_message = f"{http_method} is not ALLOWED on {url}"
        raise ErrorResponse(405, error_message)
