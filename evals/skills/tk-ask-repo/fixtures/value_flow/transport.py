"""Synthetic transport contract used by tk-ask-repo behavior evals."""

from typing import TypedDict


class ProfilePayload(TypedDict):
    display_name: str
    short_name: str
