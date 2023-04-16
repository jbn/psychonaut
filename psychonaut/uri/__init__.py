import re
from urllib.parse import parse_qs, urlencode
from more_itertools import nth

ATP_URI_REGEX = re.compile(
    r"^(at:\/\/)?((?:did:[a-z0-9:%-]+)|(?:[a-z0-9][a-z0-9.:-]*))(\/[^?#\s]*)?(\?[^#\s]+)?(#[^\s]+)?$",
    re.IGNORECASE,
)
RELATIVE_REGEX = re.compile(r"^(\/[^?#\s]*)?(\?[^#\s]+)?(#[^\s]+)?$", re.IGNORECASE)


class AtUri:
    def __init__(self, uri, base=None):
        if base:
            parsed = parse(base)
            if not parsed:
                raise ValueError(f"Invalid at uri: {base}")
            relative_parsed = parse_relative(uri)
            if not relative_parsed:
                raise ValueError(f"Invalid path: {uri}")
            parsed.update(relative_parsed)
        else:
            parsed = parse(uri)
            if not parsed:
                raise ValueError(f"Invalid at uri: {uri}")

        self.hash = parsed["hash"]
        self.host = parsed["host"]
        self.pathname = parsed["pathname"]
        self.search_params = parsed["search_params"]

    @classmethod
    def make(cls, handle_or_did, collection=None, rkey=None):
        uri_str = handle_or_did
        if collection:
            uri_str += f"/{collection}"
        if rkey:
            uri_str += f"/{rkey}"
        return cls(uri_str)

    @property
    def protocol(self):
        return "at:"

    @property
    def origin(self):
        return f"at://{self.host}"

    @property
    def hostname(self):
        return self.host

    @hostname.setter
    def hostname(self, value):
        self.host = value

    @property
    def search(self):
        return urlencode(self.search_params, doseq=True)

    @search.setter
    def search(self, value):
        self.search_params = parse_qs(_no_leading_question_mark(value))

    @property
    def collection(self):
        return nth(self.pathname.split("/"), 1, default="")

    @collection.setter
    def collection(self, value):
        parts = self.pathname.split("/")
        parts[0] = value
        self.pathname = "/".join(parts)

    @property
    def rkey(self):
        return nth(self.pathname.split("/"), 2, default="")

    @rkey.setter
    def rkey(self, value):
        parts = self.pathname.split("/")
        if not parts[0]:
            parts[0] = "undefined"
        if len(parts) == 1:
            parts.append(value)
        else:
            parts[1] = value
        self.pathname = "/".join(parts)

    @property
    def href(self):
        return self.__str__()

    def __str__(self):
        path = self.pathname or "/"
        if not path.startswith("/"):
            path = f"/{path}"
        qs = urlencode(self.search_params, doseq=True)
        if qs and not qs.startswith("?"):
            qs = f"?{qs}"
        hash = self.hash
        if hash and not hash.startswith("#"):
            hash = f"#{hash}"
        return f"at://{self.host}{path}{qs}{hash}"

def _no_leading_question_mark(qs):
    if qs.startswith("?"):
        return qs[1:]
    return qs

def _parse_search_params(m: re.Match, group_idx: int):
    if m.group(group_idx):
        return parse_qs(_no_leading_question_mark(m.group(group_idx)))
    return {}

def parse(uri_str):
    match = ATP_URI_REGEX.match(uri_str)
    if match:
        return {
            "hash": match.group(5) or "",
            "host": match.group(2) or "",
            "pathname": match.group(3) or "",
            "search_params": _parse_search_params(match, 4),
        }
    return None


def parse_relative(uri_str):
    match = RELATIVE_REGEX.match(uri_str)
    if match:
        return {
            "hash": match.group(3) or "",
            "pathname": match.group(1) or "",
            "search_params": _parse_search_params(match, 2),
        }
    return None
