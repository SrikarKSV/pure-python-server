from urllib.parse import parse_qs


def parse_get_form(environ: dict) -> dict:
    """Accepts environ and returns key-value pairs parsed from a form submitted through POST request"""

    # Get query strings and parse them
    query_string = parse_qs(environ["QUERY_STRING"])

    # Clean the dict
    decoded_query_string = {
        key: value[0] for key, value in query_string.items() if len(value) == 1
    }

    return decoded_query_string
