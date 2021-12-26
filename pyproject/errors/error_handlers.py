import os
import traceback

from pyproject.lib import render_template


def global_error_handler(error, response):
    # Assigning status code to exception objects
    try:
        error.status_code = error.status_code
    except:
        error.status_code = 500

    if os.getenv("MODE") == "development":
        return sendDevError(error, response)
    elif os.getenv("MODE") == "production":
        return sendProdError(error, response)


def sendDevError(error, response):
    # Getting traceback from exception
    stack = "".join(traceback.TracebackException.from_exception(error).format())
    context = {
        "title": f"{error.status_code} Error",
        "status": error.status_code,
        "msg": error,
        "stack": stack,
    }

    return render_template(
        "error.html", response, context, status_code=error.status_code
    )


def sendProdError(error, response):
    context = {
        "title": f"{error.status_code} Error",
        "status": error.status_code,
        "msg": error,
    }

    return render_template(
        "error.html", response, context, status_code=error.status_code
    )
