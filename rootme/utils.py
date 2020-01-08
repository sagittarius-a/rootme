"""root-me.org API utilities."""

import json
from typing import Dict, Optional

import requests

from rootme.types import Rankingentry, Searchresult, Userinfo


def search_user(
    username: str, cookies: Dict[str, str],
) -> Dict[str, Searchresult]:
    """Search a username in root-me.org users.

    Parameters
    ----------
    username : str
        Username to search in root-ne.org users.
    cookies : Dict[str, str]
        Cookies to use in API request.

    Returns
    -------
    Dict[str, Userinfo]
        Information about root-me users matching search.

    Raises
    ------
    ValueError
        If the search failed.

    """
    url = f"https://api.www.root-me.org/auteurs?nom={username}"
    r = requests.get(url, cookies=cookies)

    if r.status_code != 200:
        raise ValueError("Cannot get authors. Error %s", r.status_code)

    response = json.loads(r.content)

    # Load results in intermediate variable in order to check type consistency
    # Mypy is not able to infer type directly from JSON data. Typing is more
    # important than saving few bytes of memory. This is Python after all.
    results: Dict[str, Searchresult] = {}
    for entry in response[0]:
        results[entry] = response[0][entry]

    return results


def get_user_info(userid: str, cookies: Dict[str, str]) -> Optional[Userinfo]:
    """Get user information based on userid.

    Parameters
    ----------
    userif : str
        Id of the username to look up.
    cookies : Dict[str, str]
        Cookies to use in API request.

    Raises
    ------
    ValueError
        If the information about the user cannot be fetched.

    """
    url = f"https://api.www.root-me.org/auteurs/{userid}"
    r = requests.get(url, cookies=cookies)

    if r.status_code != 200:
        print(f"Cannot get info about user %s. Error %s" % (userid, r.status_code))
        return

    # Load results in intermediate variable in order to check type consistency
    # Mypy is not able to infer type directly from JSON data. Typing is more
    # important than saving few bytes of memory. This is Python after all.
    userinfo: Userinfo = json.loads(r.content)

    return userinfo


def get_global_ranking(
    offset: int, cookies: Dict[str, str]
) -> Dict[str, Rankingentry]:
    """Get global ranking, starting at offset `offset`.

    Parameters
    ----------
    userif : str
        Id of the username to look up.
    cookies : Dict[str, str]
        Cookies to use in API request.

    Raises
    ------
    ValueError
        If an error occured fetching ranking.

    """
    url = f"https://api.www.root-me.org/classement"
    if offset:
        url += f"?debut_classement={offset - 1}"

    r = requests.get(url, cookies=cookies)

    if r.status_code != 200:
        raise ValueError("Cannot get ranking. Error %s", r.status_code)

    response = json.loads(r.content)

    # Load results in intermediate variable in order to check type consistency
    # Mypy is not able to infer type directly from JSON data. Typing is more
    # important than saving few bytes of memory. This is Python after all.
    ranking: Dict[str, Rankingentry] = {}
    for entry in response[0]:
        ranking[entry] = response[0][entry]

    return ranking
