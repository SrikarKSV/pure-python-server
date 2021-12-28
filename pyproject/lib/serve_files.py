import mimetypes
import os
from pathlib import Path
from wsgiref import util

from jinja2 import Environment, FileSystemLoader

from ..errors import ErrorResponse
from .utils import HTTP_MESSAGE


def is_request_file(environ):
    return bool(Path(environ["PATH_INFO"]).suffix)


def serve_static_files(environ, response):
    """
    Responds with a static file if found, else gives 404

        Parameters:
            environ (dict): Dictionary filled with request details (Given by WSGI)
            response (function): Function given by WSGI, to respond

        Returns:
            static_file (List[bytes]): Static file, if found converted to iterable bytes
    """
    static_file = (
        Path.resolve(Path.cwd())
        / "pyproject"
        / "static"
        / environ["PATH_INFO"].lstrip("/")
    )

    # If requested file does not exist
    if not Path(static_file).is_file():
        response(HTTP_MESSAGE[404], [("Content-Type", "text/plain")])
        return [b"404 Not Found"]

    # Only GET requests are accepted for static files
    if environ["REQUEST_METHOD"] != "GET":
        response(HTTP_MESSAGE[405], [("Content-Type", "text/plain")])
        return [b"405 Method Not Allowed"]

    try:
        file_type = mimetypes.guess_type(static_file.name)[0] or "text/plain"
        response(HTTP_MESSAGE[200], [("Content-Type", file_type)])
        return util.FileWrapper(open(static_file, "rb"))
    except Exception as error:
        msg = (
            error
            if os.getenv("MODE") == "development"
            else f"We are having problems in serving {environ['PATH_INFO']}, come again later"
        )
        response(HTTP_MESSAGE[500], [("Content-Type", "text/html")])
        res = f"500 Server error<br>{msg}"
        return [bytes(res, "utf-8")]


def render_template(file: str, response, context: dict = {}, status_code: int = 200):
    """
    Accepts jinja file and returns the template

        Parameters:
            file (str): Name of the Jinja file, inside templates folder
            response (function): Function given by WSGI
            context (dict): Dict filled with variables to embed in template
            status_code (int): HTTP status code, to respond

        Returns:
            template (List[bytes]): Template filled with data converted to iterable bytes
    """
    try:
        templates_directory = Path.cwd() / "pyproject" / "templates"
        template = Environment(
            loader=FileSystemLoader(templates_directory.absolute())
        ).get_template(file)
        html = template.render(context)
        response(HTTP_MESSAGE[status_code], [("Content-Type", "text/html")])
        return [bytes(html, "utf-8")]
    except Exception as error:
        raise ErrorResponse(500, error)
