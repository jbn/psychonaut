# async context manager
from contextlib import asynccontextmanager
import os
import aiohttp
from psychonaut.api.session import Session, SessionFactory
from dotenv import load_dotenv
from pathlib import Path
import json


@asynccontextmanager
async def get_simple_client_session(
    inject_dot_env: bool = True, 
    allow_homedir_creds: bool = True
) -> Session:
    """
    Initialize a simple client session for use with the api.

    :param inject_dot_env: If true, injects the .env file into the environment.
        expects BSKY_USERNAME and BSKY_PASSWORD to be set
        TODO: the new password thing
    """
    if inject_dot_env:
        load_dotenv()

    username = os.getenv("BSKY_USERNAME", "")
    password = os.getenv("BSKY_PASSWORD", "")

    # attempt to lookup ~/.bsky.json for credentials
    if allow_homedir_creds and not username and not password:
        cred_path = Path.home() / ".psychonaut.json"
        if cred_path.exists():
            with cred_path.open("r") as fp:
                cred = json.load(fp)
                username = cred["username"]
                password = cred["password"]

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
