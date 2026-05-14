import re

_SAFE_ID = re.compile(r"^[a-zA-Z0-9_\-]{1,64}$")


def is_safe_id(value: str) -> bool:
    return bool(_SAFE_ID.match(value))
