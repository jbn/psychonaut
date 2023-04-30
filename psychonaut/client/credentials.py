from contextlib import contextmanager
from dotenv import load_dotenv


import json
import os
from pathlib import Path
from typing import Tuple


def load_creds(
    inject_dot_env: bool = True, allow_homedir_creds: bool = True
) -> Tuple[str, str]:
    """
    Load credentials from the environment or from ~/.bsky.json
    :param inject_dot_env: If true, injects the .env file into the environment.
        expects BSKY_USERNAME and BSKY_PASSWORD to be set
    :param allow_homedir_creds: If true, allows ~/.bsky.json to be used for credentials
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

    return username, password



@contextmanager
def write_homedir_creds(username: str, allow_overwrite: bool):
    """
    Write credentials to ~/.bsky.json

    :param username: The username to write
    :param allow_overwrite: If true, allows overwriting the file otherwise 
        raises FileExistsError
    """
    print("......")
    file_path = Path().home() / ".psychonaut.json"

    if file_path.exists() and not allow_overwrite:
        raise FileExistsError(f"File {file_path} exists")

    user_input = []
    def set_password(password: str):
        user_input.append(password)

    yield set_password

    # write the file
    file_path.write_text(
        json.dumps({
            "username": username,
            "password": user_input[0],
        })
    )
