import typing as t

from .error_handlers import global_error_handler


class ExceptionMiddleware:
    """
    A middleware to catch errors in the server and pass it to handler

    Attributes
    ----------
    app : function
        Function called by WSGI server when a request is made
    """

    def __init__(self, app) -> None:
        self.app = app

    def __call__(self, environ: dict, response: t.Callable) -> t.Any:
        """
        When the object is called upon a request, the attribute app is called

        The attribute app is inside a try/except block and errors are caught and passed to error handler

        Parameters
        ----------
        environ (dict): A dictionary populated with information of the request (Given by the WSGI server)
        response (function): A callable accepting a status code,
                a list of headers, and an optional exception context to
                start the response.

        Returns
        -------
        response List[bytes]: Iterable byte which sent to the client as a response
        """
        try:
            return self.app(environ, response)
        except Exception as error:
            return global_error_handler(error, response)
