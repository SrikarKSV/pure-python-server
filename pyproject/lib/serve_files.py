import datetime
import email
import mimetypes
import os
from pathlib import Path
from wsgiref import util

from jinja2 import Environment, FileSystemLoader

from ..errors import ErrorResponse
from .utils import HTTP_MESSAGE, pretty_date


def is_request_file(environ):
    return bool(Path(environ["PATH_INFO"]).suffix)


def serve_static_files(environ, response):
    """
    Responds with a static file if found 0r 304 Not Modified, else gives 404

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
        f = open(static_file, "rb")
        file_type = mimetypes.guess_type(f.name)[0] or "text/plain"
        fs = os.fstat(f.fileno())
        # Use browser cache if possible
        if (
            "HTTP_IF_MODIFIED_SINCE" in environ.keys()
            and "HTTP_IF_NONE_MATCH" not in environ.keys()
        ):
            # compare If-Modified-Since and time of last file modification
            try:
                if_modified_since = email.utils.parsedate_to_datetime(
                    environ["HTTP_IF_MODIFIED_SINCE"]
                )
            except (TypeError, IndexError, OverflowError, ValueError):
                # ignore ill-formed values
                pass
            else:
                if if_modified_since.tzinfo is None:
                    # obsolete format with no timezone, cf.
                    # https://datatracker.ietf.org/doc/html/rfc7231#section-7.1.1.1
                    if_modified_since = if_modified_since.replace(
                        tzinfo=datetime.timezone.utc
                    )
                if if_modified_since.tzinfo is datetime.timezone.utc:
                    # compare to UTC datetime of last modification
                    last_modif = datetime.datetime.fromtimestamp(
                        fs.st_mtime, datetime.timezone.utc
                    )
                    # remove microseconds, like in If-Modified-Since
                    last_modif = last_modif.replace(microsecond=0)
                    if last_modif <= if_modified_since:
                        f.close()
                        response(HTTP_MESSAGE[304], [("Content-Type", "text/plain")])
                        return [b""]
        response(
            HTTP_MESSAGE[200],
            [
                ("Content-Type", file_type),
                ("Content-Length", str(fs[6])),
                ("Last-Modified", email.utils.formatdate(fs.st_mtime, usegmt=True)),
                ("Cache-Control", "public, max-age=31536000"),
            ],
        )
        return util.FileWrapper(f)
    except Exception as error:
        f.close()
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
        env = Environment(loader=FileSystemLoader(templates_directory.absolute()))
        env.globals["pretty_date"] = pretty_date
        template = env.get_template(file)
        html = template.render(context)
        response(
            HTTP_MESSAGE[status_code],
            [
                ("Content-Type", "text/html"),
                ("Cache-Control", "public, max-age=0, must-revalidate"),
            ],
        )
        return [bytes(html, "utf-8")]
    except Exception as error:
        raise ErrorResponse(500, error)
