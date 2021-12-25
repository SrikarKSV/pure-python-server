from pyproject.lib.serve_files import render_template

# Build router for request method and give 403 is wrong
def router(environ, response):
    print(environ)
    return render_template("index.html", response, {"title": "Home"})
