class ErrorResponse(Exception):
    def __init__(self, status_code, message) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        return str(self.message)
