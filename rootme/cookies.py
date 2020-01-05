"""Cookie management utilities."""

import os
from pathlib import Path


def load_cookie() -> str:
    """Load cookie content from disk.

    The path where the cookie is stored can be customized thanks to the
    ROOTME_COOKIE_PATH environment variable.

    Returns
    -------
    str
        Content of the 'spip_session' cookie.

    Raises
    ------
    FileNotFoundError
        If the file containing the cookie value is not found.

    """
    root = (
        os.environ.get("ROOTME_COOKIE_PATH")
        or os.environ.get("HOME")
        or "/tmp"
    )
    cookie_file = Path(root, ".rootme-spip-session")
    if not cookie_file.exists():
        print("Cookie not found. Try login again")
        raise FileNotFoundError

    with open(cookie_file, "r") as pfile:
        data = pfile.read()

    return data


def save_cookie(cookie: str) -> None:
    """Write the cookie to disk.

    The file containing cookie is not accessible by other users. Hence it
    requires the use of os.open and os.fdopen functions. The context
    manager of fdopen is used in order to automatically manager file
    descriptor destruction.

    Parameters
    ----------
    cookie : str
        Content of the 'spip_session' cookie to write to disk.

    """
    root = (
        os.environ.get("ROOTME_COOKIE_PATH")
        or os.environ.get("HOME")
        or "/tmp"
    )
    fd = os.open(
        Path(root, ".rootme-spip-session"),
        os.O_WRONLY | os.O_CREAT,
        mode=0o600,
    )
    with os.fdopen(fd, "w+") as pfile:
        pfile.write(cookie)
