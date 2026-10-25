# Change log — 2026-10-25

## 3.1 Quality Gate Fix
- Added minimal `gateway.html` visual showcase; `index.html` was not modified.
- Added fund-representation retainer-plus-success-fee calculator and ReportLab PDF generation script.
- Added hotel corporate-rate calculator and ReportLab PDF generation script.
- Hotel lead notes (Fouad Hotel, 15 El Shohadaa St, 290–1,000 EGP; Aelat Adaa near Raml Station) are user-supplied leads, not independently verified by this commit. No current price, address, availability or affiliation is certified.
- Financial-diagnosis and freight-forwarding calculation helpers have deterministic formula tests in `tests/test_cash_first_integrity.py`; check CI before treating their TESTED status as fully validated. No claim is made that pdfplumber extraction was tested by these formula tests.
- Hotel-energy is TESTED PARTIAL for the rate formula only; real-world property details remain unverified. Business-diagnosis, restructuring, ISO audit and fund representation remain PROPOSED pending client data.
- PDF outputs are generated at runtime under `reports/`; no generated client report is committed.
