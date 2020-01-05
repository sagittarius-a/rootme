"""Module related to 'connect' command for rootme cli."""

import argparse
import getpass
import json
from typing import Optional

import requests


def connect(args: argparse.Namespace) -> str:
    """Connect a user to the root-ne.org api.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments passed to the command line.

    Returns
    -------
    str
        Value of the 'spip_session' cookie.

    Raises
    ------
    ValueError
        If connection to the api is not successfull.

    """
    username: str = args.username
    password: Optional[str] = args.password
    if not password:
        password = getpass.getpass("Password: ")

    payload = {
        "login": username,
        "password": password,
    }
    url = "https://api.www.root-me.org/login"
    r = requests.post(url, data=payload)

    if r.status_code != 200:
        raise ValueError("Cannot login to the api.")

    print("Authentication successfull")
    response = json.loads(r.content)[0]
    return str(response["info"]["spip_session"])
