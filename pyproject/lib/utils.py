import re

HTTP_MESSAGE = {
    200: "200 OK",
    303: "303 See Other",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    500: "500 Internal Server Error",
}


def route_url(regexes, url):
    matches = [bool(re.compile(regex).match(url)) for regex in regexes]
    return any(matches)
