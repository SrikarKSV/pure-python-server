from .error_handlers import global_error_handler


class ExceptionMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, response):
        try:
            return self.app(environ, response)
        except Exception as error:
            return global_error_handler(error, response)
