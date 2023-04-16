import re
from psychonaut.nsid.nsid import ensure_valid_nsid, InvalidNsidError, ensure_valid_nsid_regex
from psychonaut.identifier.handle import ensure_valid_handle, InvalidHandleError, ensure_valid_handle_regex
from psychonaut.identifier.did import ensure_valid_did, InvalidDidError, ensure_valid_did_regex

def ensure_valid_at_uri(uri: str):
    # JSON pointer is pretty different from rest of URI, so split that out first
    uri_parts = uri.split('#')
    if len(uri_parts) > 2:
        raise ValueError('ATURI can have at most one "#", separating fragment out')
    fragment_part = uri_parts[1] if len(uri_parts) == 2 else None
    uri = uri_parts[0]

    # check that all chars are boring ASCII
    if not re.match(r'^[a-zA-Z0-9._~:@!$&\')(*+,;=%/-]*$', uri):
        raise ValueError('Disallowed characters in ATURI (ASCII)')

    parts = uri.split('/')
    if len(parts) >= 3 and (parts[0] != 'at:' or len(parts[1]) != 0):
        raise ValueError('ATURI must start with "at://"')
    if len(parts) < 3:
        raise ValueError('ATURI requires at least method and authority sections')

    try:
        ensure_valid_handle(parts[2])
    except InvalidHandleError:
        try:
            ensure_valid_did(parts[2])
        except InvalidDidError:
            raise ValueError('ATURI authority must be a valid handle or DID')

    if len(parts) >= 4:
        if len(parts[3]) == 0:
            raise ValueError(
                'ATURI cannot have a slash after authority without a path segment'
            )
        try:
            ensure_valid_nsid(parts[3])
        except InvalidNsidError:
            raise ValueError(
                'ATURI requires first path segment (if supplied) to be valid NSID'
            )

    if len(parts) >= 5:
        if len(parts[4]) == 0:
            raise ValueError(
                'ATURI cannot have a slash after collection, unless record key is provided'
            )
        # would validate rkey here, but there are basically no constraints!

    if len(parts) >= 6:
        raise ValueError(
            'ATURI path can have at most two parts, and no trailing slash'
        )

    if len(uri_parts) >= 2 and fragment_part is None:
        raise ValueError('ATURI fragment must be non-empty and start with slash')

    if fragment_part is not None:
        if len(fragment_part) == 0 or fragment_part[0] != '/':
            raise ValueError('ATURI fragment must be non-empty and start with slash')
        # NOTE: enforcing *some* checks here for sanity. Eg, at least no whitespace
        if not re.match(r'^\/[a-zA-Z0-9._~:@!$&\')(*+,;=%[\]/-]*$', fragment_part):
            raise ValueError('Disallowed characters in ATURI fragment (ASCII)')

    if len(uri) > 8 * 1024:
        raise ValueError('ATURI is far too long')


_aturi_re = r"""^at:\/\/(?P<authority>[a-zA-Z0-9._:%-]+)(\/(?P<collection>[a-zA-Z0-9-.]+)(\/(?P<rkey>[a-zA-Z0-9._~:@!$&%')(*+,;=-]+))?)?(#(?P<fragment>\/[a-zA-Z0-9._~:@!$&%')(*+,;=\-[\]/\\]*))?$"""



def ensure_valid_at_uri_regex(uri: str):
    # simple regex to enforce most constraints via just regex and length.
    # hand wrote this regex based on above constraints. whew!
    aturi_regex = re.compile(_aturi_re)
    rm = aturi_regex.match(uri)
    if not rm or not rm.groupdict():
        raise ValueError("ATURI didn't validate via regex")
    groups = rm.groupdict()

    try:
        ensure_valid_handle_regex(groups['authority'])
    except ValueError:
        try:
            ensure_valid_did_regex(groups['authority'])
        except ValueError:
            raise ValueError('ATURI authority must be a valid handle or DID')

    if groups['collection']:
        try:
            ensure_valid_nsid_regex(groups['collection'])
        except ValueError:
            raise ValueError('ATURI collection path segment must be a valid NSID')

    if len(uri) > 8 * 1024:
        raise ValueError('ATURI is far too long')
