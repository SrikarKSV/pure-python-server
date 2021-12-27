from urllib.parse import parse_qs
from html import escape


def parse_get_form(environ):
    # Get query strings and parse them
    query_string = parse_qs(environ["QUERY_STRING"])

    # Clean the dict
    for key, value in query_string.items():
        if len(value) == 1:
            query_string[key] = value[0]

        query_string[key] = escape(query_string[key])

    return query_string
