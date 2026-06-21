import re

POLICIES: dict[str, dict] = {
    "HR": {
        "allowed_categories": None,  # None = no filter, all categories
        "redact_pii": False,
    },
    "Hiring Manager": {
        "allowed_categories": ["ENGINEERING", "INFORMATION-TECHNOLOGY"],
        "redact_pii": False,
    },
    "Recruiter": {
        "allowed_categories": None,
        "redact_pii": True,
    },
}

ROLES = list(POLICIES.keys())

_EMAIL_RE = re.compile(r'\b[\w.+-]+@[\w-]+\.\w{2,}\b')
_PHONE_RE = re.compile(r'\b(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b')
_ADDRESS_RE = re.compile(r'\b\d{1,5}\s+\w[\w\s]{2,40}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Place|Pl)\.?\b', re.IGNORECASE)


def get_policy(role: str) -> dict:
    return POLICIES.get(role, POLICIES["HR"])


def redact(text: str, role: str) -> str:
    """Strip PII from text for roles with redact_pii=True."""
    if not get_policy(role)["redact_pii"]:
        return text
    text = _EMAIL_RE.sub("[EMAIL REDACTED]", text)
    text = _PHONE_RE.sub("[PHONE REDACTED]", text)
    text = _ADDRESS_RE.sub("[ADDRESS REDACTED]", text)
    return text
