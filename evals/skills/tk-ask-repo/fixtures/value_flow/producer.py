"""Synthetic producer used by tk-ask-repo behavior evals."""

from .transport import ProfilePayload


def build_profile_payload(profile: dict[str, str]) -> ProfilePayload:
    return {
        # Legal name for invoices and regulated records.
        "display_name": profile["legal_name"],
        # Friendly name for profile UI and notifications.
        "short_name": profile["short_name"],
    }
