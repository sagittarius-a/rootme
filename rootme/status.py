"""Connection status utilities."""

import requests


def status(cookie: str) -> bool:
    """Check if the current user is connected.

    Parameters
    ----------
    cookie : str
        Content of the 'spip_session' cookie to write to disk.


    Returns
    -------
    bool
        True if the current user is connected, False otherwise.
    """
    cookies = {
        "spip_session": cookie,
    }

    try:
        url = f"https://api.www.root-me.org/classement"
        r = requests.get(url, cookies=cookies)

        if r.status_code == 401:
            return False

        return True

    except ValueError:
        print("Error trying to determine if connected")
        return False
