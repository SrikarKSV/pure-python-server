import typing as t

from .errors import ErrorResponse
from .lib import route_url
from .lib.serve_files import is_request_file, serve_static_files
from .main import router as home_router
from .posts import router as posts_router


def app(environ: dict, response: t.Callable) -> t.Any:
    """
    A callable Python object which is called for every request along with two parameters and returns a response

        Parameters:
            environ (dict): A dictionary populated with information of the request (Given by the WSGI server)
            response (function): A callable accepting a status code,
                a list of headers, and an optional exception context to
                start the response.
    """
    # Serve static file
    if is_request_file(environ):
        return serve_static_files(environ, response)

    url = environ["PATH_INFO"]

    if route_url(["^\/$", "\/new(\/)?"], url):  # Accepts ['/', '/new']
        return home_router(environ, response)
    if route_url(
        [
            "^\/posts(\/)?$",
            "^\/posts\/\d{1,}(\/)?$",
            "^\/posts\/\d{1,}\/edit(\/)?$",
            "^\/posts\/\d{1,}\/delete(\/)?$",
        ],
        url,
    ):  # Accepts ['/posts', '/posts/id', '/posts/id/edit', '/posts/id/delete']
        return posts_router(environ, response)
    else:
        # If noting matched then show 404
        message = f"The requested URL {environ['PATH_INFO']} was not found!"
        raise ErrorResponse(404, message)
