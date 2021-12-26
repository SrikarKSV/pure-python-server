import re

from pyproject.errors import ErrorResponse
from pyproject.lib import render_template

from .controllers import create_post


# Build router for request method and give 403 is wrong
def router(environ, response):
    URL = environ["PATH_INFO"]
    HTTP_METHOD = environ["REQUEST_METHOD"].upper()

    if HTTP_METHOD == "GET":
        if re.compile("^\/posts(\/)?$").match(URL):
            return render_template("all-posts.html", response, {"title": "All posts"})
        if re.compile("^\/posts\/\d{1,}(\/)?$").match(URL):
            return render_template("post.html", response, {"title": "Post"})
        if re.compile("^\/posts\/edit\/\d{1,}(\/)?$").match(URL):
            return render_template("edit-post.html", response, {"title": "Edit post"})
    elif HTTP_METHOD == "POST":
        if re.compile("^\/posts(\/)?$").match(URL):
            return create_post(environ, response)
    else:
        errorMessage = f"{HTTP_METHOD} is not ALLOWED on {URL}"
        raise ErrorResponse(405, errorMessage)
