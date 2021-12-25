from pyproject.lib.serve_files import render_template


def app(environ, response):
    response("200 OK", [("Content-Type", "text/html")])
    return render_template("index.html")
