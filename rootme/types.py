"""Custom types for root-me.org api."""

from typing import Dict, List

from typing_extensions import TypedDict


class Searchresult(TypedDict, total=True):
    """Definition of a search result."""

    id_auteur: str
    nom: str


class Userinfo(TypedDict, total=True):
    """Definition of information about a user."""

    nom: str
    score: str
    position: str
    challenges: List[Dict[str, str]]
    solutions: List[Dict[str, str]]
    validation: List[Dict[str, str]]


class Rankingentry(TypedDict, total=True):
    """Definition of an entry in the global root-me.org ranking."""

    place: str
    id_auteur: str
    score: str
