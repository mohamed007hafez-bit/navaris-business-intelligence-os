#!/usr/bin/env python3
"""NAVARIS lead CSV bridge: normalize, deduplicate, and draft follow-ups for review.

No network calls, no email sending, no paid APIs, no automatic external actions.
Python standard library only.
"""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

APPROVAL = "DRAFT_ONLY_REQUIRES_MASTER_APPROVAL"
ALIASES = {
    "name": ("name", "full name", "contact", "person", "lead name"),
    "title": ("title", "job title", "role", "position"),
    "company": ("company", "company name", "organization", "organisation", "employer"),
    "email": ("email", "work email", "email address"),
    "website": ("website", "company website", "domain", "url"),
    "profile_url": ("profile_url", "profile url", "linkedin", "linkedin url", "person url"),
    "reason": ("reason", "qualification reason", "why selected", "fit reason"),
    "source": ("source", "source url", "source_url"),
}
def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").strip().lower()).strip()

def pick(row: dict, aliases: tuple[str, ...]) -> str:
    indexed = {norm(k): (v or "").strip() for k, v in row.items() if k}
    for alias in aliases:
        if indexed.get(norm(alias)):
            return indexed[norm(alias)]
    return ""

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python integrations/lead_pipeline.py <input.csv>", file=sys.stderr)
        return 2
    source = Path(sys.argv[1]).expanduser()
    if not source.is_file():
        print(f"Input file not found: {source}", file=sys.stderr)
        return 2
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            print("Input CSV has no header row.", file=sys.stderr)
            return 2
        rows = list(reader)

    normalized, seen = [], set()
    for raw in rows:
        item = {key: pick(raw, aliases) for key, aliases in ALIASES.items()}
        identity = item["email"].lower() or item["profile_url"].lower()
        if not identity:
            identity = (item["company"] + "|" + item["name"]).strip("|").lower()
        if not identity or identity in seen:
            continue
        seen.add(identity)
        item["review_status"] = "NEEDS_HUMAN_QUALIFICATION"
        item["approval_status"] = APPROVAL
        normalized.append(item)

    review_path = source.with_name("navaris_leads_review.csv")
    draft_path = source.with_name("navaris_followup_drafts.csv")
    fields = list(ALIASES.keys()) + ["review_status", "approval_status"]
    with review_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(normalized)

    draft_fields = ["name", "title", "company", "email", "subject", "draft_body", "approval_status"]
    with draft_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=draft_fields)
        writer.writeheader()
        for item in normalized:
            greeting = item["name"] or "Hello"
            company = item["company"] or "your team"
            reason = item["reason"] or "exploring potential fit for industrial supply, petroleum/oilfield services, or logistics cooperation"
            body = (
                f"Dear {greeting},\n\n"
                f"I'm contacting you on behalf of NAVARIS Business Operations & Development in Alexandria, Egypt. "
                f"We are reviewing potential cooperation related to {reason}. "
                f"Would you be the appropriate person for a brief introductory discussion, or could you direct me to the relevant colleague?\n\n"
                f"Regards,\nDr. Mohamed Hafez Khalifa\nNAVARIS Business Operations & Development\n"
                f"\nDRAFT ONLY — review recipient, relevance, source, and wording before sending."
            )
            writer.writerow({
                "name": item["name"], "title": item["title"], "company": company,
                "email": item["email"], "subject": f"Potential cooperation with NAVARIS — {company}",
                "draft_body": body, "approval_status": APPROVAL,
            })
    print(f"Input rows: {len(rows)}")
    print(f"Unique leads exported: {len(normalized)}")
    print(f"Review file: {review_path}")
    print(f"Follow-up drafts (NOT SENT): {draft_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
