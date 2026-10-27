"""Explicit feature switches. Change these values deliberately before enabling features."""

# Local calculations can be invoked explicitly through the router; no agent runs on import.
ENABLED_AGENTS = {
    "shipping": False,
    "oilfield": False,
    "financial": False,
}

# No external model/API call is implemented or permitted by default.
ALLOW_CLOUD_AI = False

# Human approval is required for any future outbound action. This package currently
# has no email, messaging, bid-submission, booking, or payment side effects.
REQUIRE_HUMAN_APPROVAL_FOR_EXTERNAL_ACTIONS = True
