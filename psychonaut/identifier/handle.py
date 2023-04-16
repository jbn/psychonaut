import re

from psychonaut.identifier.reserved import RESERVED_SUBDOMAINS


class InvalidHandleError(ValueError):
    pass


class ReservedHandleError(ValueError):
    pass


class UnsupportedDomainError(ValueError):
    pass


def ensure_valid_handle(handle: str) -> None:
    if not re.match(r"^[a-zA-Z0-9.-]*$", handle):
        raise InvalidHandleError(
            "Disallowed characters in handle (ASCII letters, digits, dashes, periods only)"
        )

    if len(handle) > 253:
        raise InvalidHandleError("Handle is too long (253 chars max)")

    labels = handle.split(".")
    if len(labels) < 2:
        raise InvalidHandleError("Handle domain needs at least two parts")

    for i, label in enumerate(labels):
        if len(label) < 1:
            raise InvalidHandleError("Handle parts cannot be empty")
        if len(label) > 63:
            raise InvalidHandleError("Handle part too long (max 63 chars)")
        if label.endswith("-") or label.startswith("-"):
            raise InvalidHandleError("Handle parts cannot start or end with hyphens")
        if i + 1 == len(labels) and not re.match(r"^[a-zA-Z]", label):
            raise InvalidHandleError(
                "Handle final component (TLD) must start with ASCII letter"
            )


def ensure_valid_handle_regex(handle: str) -> None:
    if not re.match(
        r"^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$",
        handle,
    ):
        raise InvalidHandleError("Handle didn't validate via regex")
    if len(handle) > 253:
        raise InvalidHandleError("Handle is too long (253 chars max)")


def normalize_handle(handle: str) -> str:
    return handle.lower()


def normalize_and_ensure_valid_handle(handle: str) -> str:
    normalized = normalize_handle(handle)
    ensure_valid_handle(normalized)
    return normalized


def is_valid_handle(handle: str) -> bool:
    try:
        ensure_valid_handle(handle)
    except InvalidHandleError:
        return False
    return True


def ensure_handle_service_constraints(
    handle: str, available_user_domains: list, reserved=None
) -> None:
    if reserved is None:
        reserved = RESERVED_SUBDOMAINS

    supported_domain = next(
        (domain for domain in available_user_domains if handle.endswith(domain)), None
    )

    if not supported_domain:
        raise UnsupportedDomainError("Not a supported handle domain")

    front = handle[: -len(supported_domain)]

    if "." in front:
        raise InvalidHandleError("Invalid characters in handle")

    if len(front) < 3:
        raise InvalidHandleError("Handle too short")

    if len(handle) > 30:
        raise InvalidHandleError("Handle too long")

    if front in reserved:
        raise ReservedHandleError("Reserved handle")


def fulfills_handle_service_constraints(
    handle: str, available_user_domains: list, reserved=None
) -> bool:
    try:
        ensure_handle_service_constraints(handle, available_user_domains, reserved)
    except (InvalidHandleError, ReservedHandleError, UnsupportedDomainError):
        return False
    return True
