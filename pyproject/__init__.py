from .lib.serve_files import isRequestFile, render_template, serve_static_files


def app(environ, response):
    # Serve static file
    if isRequestFile(environ):
        return serve_static_files(environ, response)

    return render_template("index.html", response, status_code=200)
