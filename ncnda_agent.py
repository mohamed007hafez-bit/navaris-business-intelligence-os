"""Draft-only commercial confidentiality and non-circumvention helper."""
from __future__ import annotations


def generate_ncnda(client_name: str, grade: str, commission_pct: float = 30.0, term_years: int = 2) -> str:
    """Return a discussion draft, not a legal opinion or signed agreement."""
    if grade not in ("ممتاز", "جيد جدا"):
        return "NO DRAFT GENERATED: opportunity grade is below the NAVARIS threshold."
    if not client_name.strip():
        raise ValueError("client_name is required.")
    if not 0 < commission_pct <= 100:
        raise ValueError("commission_pct must be greater than 0 and no more than 100.")
    if term_years < 1 or term_years > 5:
        raise ValueError("term_years must be between 1 and 5.")
    return f"""DRAFT FOR LEGAL REVIEW — NOT EXECUTABLE UNTIL REVIEWED AND SIGNED

NON-DISCLOSURE AND NON-CIRCUMVENTION AGREEMENT (NCNDA)

Counterparty: {client_name}
Proposed commission: {commission_pct:.2f}% (subject to express written agreement)
Proposed term: {term_years} year(s)

1. Purpose. The parties may exchange confidential information solely to evaluate the
identified commercial opportunity described in a separately signed schedule.
2. Confidentiality. Each party will protect non-public information and use it only
for the stated purpose, subject to agreed exclusions and legally required disclosure.
3. Non-circumvention. Any scope, protected introductions, territory, duration, and
remedies must be expressly defined in the final agreement.
4. Commercial terms. The commission basis, trigger, payment date, tax treatment,
currency, invoicing, and dispute process must be specified in a signed schedule.
5. No commitment. This draft creates no obligation to purchase, supply, award, or pay
until a final agreement is reviewed and signed by authorized representatives.

Jurisdiction, enforceability, sanctions/export-control, competition, procurement, tax,
and sector-specific requirements require qualified legal review.
"""
