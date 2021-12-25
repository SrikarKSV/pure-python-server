from wsgiref import util
from jinja2 import Template
from pathlib import Path
import mimetypes


def isRequestFile(environ):
    return bool(Path(environ["PATH_INFO"]).suffix)


def serve_static_files(environ, response):
    static_file = (
        Path.resolve(Path.cwd())
        / "pyproject"
        / "static"
        / environ["PATH_INFO"].lstrip("/")
    )

    # If requested file does not exist
    if not Path(static_file).is_file():
        response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"404 Not Found"]

    file_type = mimetypes.guess_type(static_file.name)[0]
    response("200 OK", [("Content-Type", file_type)])
    return util.FileWrapper(open(static_file, "rb"))


def render_template(file):
    templates_directory = Path.cwd() / "pyproject" / "templates"
    print(templates_directory)
    with open(templates_directory / file, "r", encoding="utf-8") as f:
        template = Template(f.read())
        html = template.render()
        return [bytes(html, "utf-8")]
