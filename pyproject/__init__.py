from .lib.serve_files import isRequestFile, render_template, serve_static_files


def app(environ, response):
    # Serve static file
    if isRequestFile(environ):
        return serve_static_files(environ, response)

    response("200 OK", [("Content-Type", "text/html")])
    return render_template("index.html")
