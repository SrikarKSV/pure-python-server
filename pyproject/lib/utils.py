import re

HTTP_MESSAGE = {
    200: "200 OK",
    303: "303 See Other",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    422: "422 Unprocessable Entity",
    500: "500 Internal Server Error",
}

ALLOWED_TAGS = [
    "ul",
    "ol",
    "li",
    "p",
    "pre",
    "code",
    "blockquote",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "br",
    "strong",
    "em",
    "a",
    "img",
    "div",
    "span",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "title", "alt"],
    "abbr": ["title"],
    "span": ["class"],
    "div": ["class"],
    "td": ["class"],
}


def route_url(regexes, url):
    matches = [bool(re.compile(regex).match(url)) for regex in regexes]
    return any(matches)
