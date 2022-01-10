import os
import traceback
import typing as t

from ..lib import render_template


def global_error_handler(error: Exception, response: t.Callable) -> t.List[bytes]:
    """A global error handler, which directs the error based on mode"""
    # Assigning status code to exception objects
    try:
        error.status_code = error.status_code
    except:
        error.status_code = 500

    if os.getenv("MODE") == "development":
        return send_dev_error(error, response)
    elif os.getenv("MODE") == "production":
        return send_prod_error(error, response)


def send_dev_error(error: Exception, response: t.Callable) -> t.List[bytes]:
    """An error handler for development mode, sends the traceback along with response"""
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


def send_prod_error(error: Exception, response: t.Callable) -> t.List[bytes]:
    """An error handler for production mode"""

    context = {
        "title": f"{error.status_code} Error",
        "status": error.status_code,
        "msg": error,
    }

    return render_template(
        "error.html", response, context, status_code=error.status_code
    )
