# async context manager
from contextlib import asynccontextmanager
import os
import aiohttp
from psychonaut.api.session import Session, SessionFactory
from psychonaut.client.credentials import load_creds


@asynccontextmanager
async def get_simple_client_session(
    inject_dot_env: bool = True, allow_homedir_creds: bool = True
) -> Session:
    """
    Initialize a simple client session for use with the api.

    :param inject_dot_env: If true, injects the .env file into the environment.
        expects BSKY_USERNAME and BSKY_PASSWORD to be set
        TODO: the new password thing
    """
    username, password = load_creds(
        inject_dot_env=inject_dot_env, allow_homedir_creds=allow_homedir_creds
    )

    if not username or not password:
        raise ValueError(
            "BSKY_USERNAME and BSKY_PASSWORD must be set in the environment or .env file"
        )

    session_opts = dict(
        timeout=aiohttp.ClientTimeout(total=20),
    )

    async with aiohttp.ClientSession(**session_opts) as sess:
        factory = SessionFactory(
            atp_host=os.environ.get("ATP_HOST", "https://bsky.social"),
            http_session=sess,
        )
        yield await factory.create(username=username, password=password)


async def get_ipynb_client_session(
    inject_dot_env: bool = True, allow_homedir_creds: bool = True
) -> Session:
    username, password = load_creds(
        inject_dot_env=inject_dot_env, allow_homedir_creds=allow_homedir_creds
    )

    if not username or not password:
        raise ValueError(
            "BSKY_USERNAME and BSKY_PASSWORD must be set in the environment or .env file"
        )

    session_opts = dict(
        timeout=aiohttp.ClientTimeout(total=20),
    )

    http_sess = aiohttp.ClientSession(**session_opts)
    factory = SessionFactory(
        atp_host=os.environ.get("ATP_HOST", "https://bsky.social"),
        http_session=http_sess,
    )
    return await factory.create(username=username, password=password)



