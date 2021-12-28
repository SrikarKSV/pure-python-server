from .error_handlers import global_error_handler


class ExceptionMiddleware:
    """
    A middleware to catch errors in the server and pass it to handler

    Attributes
    ----------
    app : function
        Function called by WSGI server when a request is made
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, response):
        """
        When the object is called upon a request, the attribute app is called

        The attribute app is inside a try/except block and errors are caught and passed to error handler

        Parameters
        ----------
        environ (dict): Dictionary filled with request details (Given by WSGI)
        response (function): Function given by WSGI, to respond

        Returns
        -------
        response List[bytes]: Iterable byte which sent to the client as a response
        """
        try:
            return self.app(environ, response)
        except Exception as error:
            return global_error_handler(error, response)
