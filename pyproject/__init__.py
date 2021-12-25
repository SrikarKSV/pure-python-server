from .lib.utils import route_url
from .lib.serve_files import isRequestFile, serve_static_files
from .main import router as home_router


def app(environ, response):
    # Serve static file
    if isRequestFile(environ):
        return serve_static_files(environ, response)

    URL = environ["PATH_INFO"]
    if route_url(["^\/$"], URL):
        return home_router(environ, response)
