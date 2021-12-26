import re
from pyproject.lib import render_template
from pyproject.errors import ErrorResponse

# Build router for request method and give 403 is wrong
def router(environ, response):
    URL = environ["PATH_INFO"]
    HTTP_METHOD = environ["REQUEST_METHOD"]

    if HTTP_METHOD == "GET":
        if re.compile("^\/$").match(URL):
            return render_template("index.html", response, {"title": "Home"})
        if re.compile("\/new(\/)?").match(URL):
            return render_template("new-post.html", response, {"title": "Write a post"})
    else:
        errorMessage = f"{HTTP_METHOD} is not ALLOWED on {URL}"
        raise ErrorResponse(405, errorMessage)
