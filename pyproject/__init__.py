from .lib.serve_files import isRequestFile, render_template, serve_static_files
from .lib.utils import HTTP_MESSAGE


def app(environ, response):
    # Serve static file
    if isRequestFile(environ):
        return serve_static_files(environ, response)

    response(HTTP_MESSAGE[200], [("Content-Type", "text/html")])
    return render_template("index.html")
