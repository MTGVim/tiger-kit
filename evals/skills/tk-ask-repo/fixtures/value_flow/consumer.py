"""Synthetic consumers used by tk-ask-repo behavior evals."""

from .transport import ProfilePayload


def profile_heading(payload: ProfilePayload) -> str:
    return f"Display name: {payload['display_name']}"


def welcome_email(payload: ProfilePayload) -> str:
    return f"Welcome, {payload['display_name']}"


def invoice_name(payload: ProfilePayload) -> str:
    # Invoices intentionally require the legal display name.
    return payload["display_name"]
