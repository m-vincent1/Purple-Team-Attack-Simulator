"""Security utilities — input sanitization for lab safety."""

import re


_SAFE_ID_RE = re.compile(r"^[a-zA-Z0-9_\-]{1,64}$")


def validate_safe_id(value: str) -> bool:
    """Return True if value is a safe alphanumeric/dash/underscore identifier."""
    return bool(_SAFE_ID_RE.match(value))


def sanitize_run_id(run_id: str) -> str:
    if not validate_safe_id(run_id):
        raise ValueError(f"Invalid run_id format: {run_id!r}")
    return run_id
