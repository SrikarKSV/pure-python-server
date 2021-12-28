from urllib.parse import parse_qs


def parse_post_form(environ):
    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0

    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ["wsgi.input"].read(request_body_size).decode("utf-8")
    data = parse_qs(request_body)

    # Clean the dict, as values come in ["value"]
    decoded_values = {key: value[0] for key, value in data.items() if len(value) == 1}

    return decoded_values
