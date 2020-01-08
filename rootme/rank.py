"""Ranking utilities."""

import argparse
import json
from typing import Dict, List

import requests
from colorama import Fore, Style

from rootme.types import Searchresult, Userinfo
from rootme.utils import get_global_ranking, get_user_info, search_user


def rank(args: argparse.Namespace, cookie: str) -> None:
    """Display ranking for one or several users.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments passed to the command line.
    cookie : str
        Content of the 'spip_session' cookie.

    Raises
    ------
    ValueError
        If the username provided in command line is not found in the first
        50 results of the search. The username provided may be mispelled.

    """
    cookies = {
        "spip_session": cookie,
    }

    max_len_user = max((len(x) for x in args.user))

    for username in args.user:

        users: Dict[str, Searchresult] = search_user(username, cookies)

        userids = []
        # Parse API search results in order to find the correct users
        for user in users:
            if users[user]["nom"] == username:
                userids.append(users[user]["id_auteur"])

        if not userids:
            raise ValueError(
                (
                    "User %s not found in 50 first search terms."
                    " Did you mispell it? "
                ),
                username,
            )

        for userid in userids:
            userinfo = get_user_info(userid, cookies)
            if userinfo is None:
                continue

            print(
                f"[{Fore.GREEN}+{Style.RESET_ALL}] "
                f"{userinfo['nom']:<{max_len_user + 2}} "
                f"Score: {userinfo['score']:<6} "
                f"Position: {userinfo['position']}"
            )


def display_ranking(args: argparse.Namespace, cookie: str) -> None:
    """Display ranking of x users, starting at offset y.

    The number of users to display can be set in command line arguments with
    the -n option. The amount of users to display cannot exceed 49 for now.
    The offset can be set in command line arguments with the -o option.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments passed to the command line.
    cookie : str
        Content of the 'spip_session' cookie.

    Raises
    ------
    ValueError
        If the username provided in command line is not found in the first
        50 results of the search. The username provided may be mispelled.

    """
    number: int = args.number
    if not number:
        return

    if number >= 50:
        print("Number of users to display cannot exceed 49 for now. Exiting.")
        return

    cookies = {
        "spip_session": cookie,
    }

    ranking = get_global_ranking(args.offset, cookies)

    for counter, entry in enumerate(ranking):

        if counter >= number:
            break

        userid = ranking[entry]["id_auteur"]
        userinfo = get_user_info(userid, cookies)
        if userinfo is None:
            continue

        print(
            f"{Fore.YELLOW}{ranking[entry]['place']:>4}{Style.RESET_ALL}. "
            f"{userinfo['nom']:<25} "
            f"{userinfo['score']} "
        )

    return
