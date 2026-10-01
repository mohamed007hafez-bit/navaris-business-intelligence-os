# NAVARIS Data Model

## Canonical entities
Company; Contact; Need; Opportunity; Partner; Supplier/OEM; Competitor/Peer; Tender/RFQ; Project; Document; Evidence; Financial Period; KPI; Task; Decision; Action; Cash Event.

## Opportunity minimum schema
Opportunity ID | Company | Country | Sector | Need | Buyer | Decision Maker | Supplier/Partner | Product/Service | RFQ/Tender | Value | Probability | Stage | Technical Fit | Commercial Fit | Strategic Fit | Risk | Expected Cash | Days to Cash | Next Action | Owner | Evidence IDs | Last Reviewed.

## Evidence schema
Evidence ID | Entity ID | Claim | Source | Source Date | Extracted Value | Source Location | Confidence | Reviewer | Last Reviewed.

## Separation rule
Reported Data, Assumption, Derived Metric and Analyst Judgment are separate data types. Never overwrite reported data with a calculation.

## Deduplication
Use stable IDs and normalized names. A company may have multiple opportunities; an opportunity may have multiple evidence records and partners.

## Status discipline
Every active record has a status and next action. Closed records retain outcome and learning.