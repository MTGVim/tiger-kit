"""Synthetic ambiguity used by tk-ask-repo behavior evals."""


def build_name_options(profile: dict[str, str]) -> dict[str, str]:
    return {
        # User-selected public identity.
        "alias": profile["alias"],
        # Compact form of the legal name.
        "short_name": profile["short_name"],
    }
