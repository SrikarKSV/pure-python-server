class ErrorResponse(Exception):
    """
    A custom Exception to raise when server has to respond with an error response

    ...

    Attributes
    ----------
    status_code : int
        HTTP status code with which to respond
    message : str
        A message sent along with error to the client
    """

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        return str(self.message)
