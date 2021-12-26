from .errors import ErrorResponse
from .lib import route_url
from .lib.serve_files import isRequestFile, serve_static_files
from .main import router as home_router
from .posts import router as posts_router


def app(environ, response):
    # Serve static file
    if isRequestFile(environ):
        return serve_static_files(environ, response)

    URL = environ["PATH_INFO"]
    print(URL)
    if route_url(["^\/$", "\/new(\/)?"], URL):
        return home_router(environ, response)
    if route_url(
        ["^\/posts(\/)?$", "^\/posts\/\d{1,}(\/)?$", "^\/posts\/edit\/\d{1,}(\/)?$"],
        URL,
    ):
        return posts_router(environ, response)
    else:
        message = f"The requested URL {environ['PATH_INFO']} was not found!"
        raise ErrorResponse(404, message)
