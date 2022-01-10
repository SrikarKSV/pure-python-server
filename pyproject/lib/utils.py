import re
import typing as t
from datetime import datetime

HTTP_MESSAGE = {
    200: "200 OK",
    303: "303 See Other",
    304: "304 Not Modified",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    422: "422 Unprocessable Entity",
    500: "500 Internal Server Error",
}


# Checks if any regex matches with given URL
def route_url(regexes: t.List[str], url: str) -> bool:
    matches = [bool(re.compile(regex).match(url)) for regex in regexes]
    return any(matches)


def pretty_date(time: t.Union[int, datetime]) -> str:
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', '3 months ago',
    'just now', etc
    """

    now = datetime.utcnow()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "1 day ago"
    if day_diff < 7:
        return str(int(day_diff)) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"


# Tags allowed in markdown to HTML
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
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
]

# Attributes allowed in markdown to HTML
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "title", "alt"],
    "abbr": ["title"],
    "span": ["class"],
    "div": ["class"],
    "td": ["class"],
}
