"""root-me.org cli utility.

It offers some basic utility to interact with the root-me.org API.

Available features:

    * connect to the root-me.org. Can be used to access challenges without
      authenticating to the web portal.
    * display ranking for one or more users
    * display ranking, for x elements, starting with an offset of y.
    * check if the connection to root-me.org is active

The cookie created on login is saved on disk. The path can be customized thanks
to the ROOTME_COOKIE_PATH environment variable. By default, the file created is
$HOME/.rootme-spip-session. If HOME environment variable is not available, the
cookie is created in /tmp.

"""

import argparse
import json
from typing import Dict, Optional

import requests
from colorama import Fore, Style

from rootme import __version__
from rootme.connect import connect
from rootme.cookies import load_cookie, save_cookie
from rootme.rank import display_ranking, rank
from rootme.status import status


def get_args() -> argparse.ArgumentParser:
    """Parse command line arguments.

    Returns
    -------
    arparse.ArgumentParser
        argparse.ArgumentParser object.

    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=__version__)

    subparsers = parser.add_subparsers(dest="command")

    connect = subparsers.add_parser("connect")
    connect.add_argument(
        "-u", "--username", required=True, help="Username is required",
    )
    connect.add_argument(
        "-p",
        "--password",
        required=False,
        help="Asked interactively if omitted",
    )

    rank = subparsers.add_parser("rank")
    rank_user = rank.add_argument_group(
        "user", "Show rank for one or more users"
    )
    rank_user.add_argument(
        "-u",
        "--user",
        nargs="*",
        help="Search user(s) in ranking. Note: case sensitive",
    )

    ranking = rank.add_argument_group("ranking", "List users in ranking")
    ranking.add_argument(
        "-n",
        "--number",
        type=int,
        help="Show the <n> top challengers. Cannot exceed 49.",
    )
    ranking.add_argument(
        "-o", "--offset", type=int, help="Start displaying at <offset>",
    )

    status = subparsers.add_parser("status")

    return parser


def main() -> int:
    """Execute rootme command line application.

    Returns
    -------
    int
        On success, returns 0. The following list contains the
        possible return values:
        - 0: success
        - 1: no command used
        - 2: no cookie file found
        - 3: user not connected

    """
    parser = get_args()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "connect":
        cookie = connect(args)
        save_cookie(cookie)

    if args.command == "rank":

        try:
            cookie = load_cookie()
        except FileNotFoundError:
            return 2

        if args.user and (args.offset or args.number):
            print("Use user group OR ranking group. See rootme rank -h")

        if args.user:
            rank(args, cookie)

        if args.number:
            display_ranking(args, cookie)

    if args.command == "status":

        try:
            cookie = load_cookie()
        except FileNotFoundError:
            return 2

        connected = status(cookie)
        if not connected:
            return 3
        print("Connected")

    return 0
