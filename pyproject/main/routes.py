from pyproject.lib import render_template

# Build router for request method and give 403 is wrong
def router(environ, response):
    URL = environ["PATH_INFO"]
    HTTP_METHOD = environ["REQUEST_METHOD"]

    return render_template("index.html", response, {"title": "Home"})
