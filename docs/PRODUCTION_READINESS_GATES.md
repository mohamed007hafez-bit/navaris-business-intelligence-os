# NAVARIS Production-Readiness Gates

**Status:** Acceptance criteria; not a production certification.  
**Applies to:** NAVARIS Business Intelligence OS repository and its connected operating processes.

## 1. Release decision

NAVARIS may be described as production-ready only after the owner has reviewed evidence for every mandatory gate below. A green GitHub Actions run is necessary engineering evidence for the checks it executes, but it is not proof of live business operations, security certification, customer adoption, or bank integration.

Until all mandatory gates pass, use the status **ACTIVE DEVELOPMENT / SUPERVISED LOCAL USE**.

## 2. Mandatory gates

| Gate | Required evidence | Pass condition | Current interpretation |
|---|---|---|---|
| Source integrity | Main branch commit, reviewed change history, clean CI | All required checks pass on the exact release commit | CI must be run; do not infer from workflow YAML |
| Reproducible installation | Fresh environment setup record | A new machine can install documented dependencies and start the selected product surface | Python CLI documented; desktop/web surfaces require separate validation |
| Automated tests | Test report and retained CI run | Full test suite passes; failures and skips are explained | Workflow runs pytest; result remains unverified until executed |
| Calculation integrity | Formula source, test cases, input/output fixtures | Formula, units, currency, period, missing-data and boundary cases tested | Only tested formulas may be labelled TESTED |
| Cash integrity | Receipt source, reconciliation evidence, reviewer identity and approval log | Cash is zero by default and becomes recognized only after independent verification, reconciliation and human approval | No live bank connection is established by the repository alone |
| Commercial human gate | Approval event and immutable audit record | No external communication, quote, tender, contract, purchase, investment or commitment without written owner approval | Drafting is permitted; autonomous execution is not |
| Data protection | Threat model, access controls, backup and retention policy, secret scan | Sensitive client/bank data is excluded from public repository and protected in any deployed environment | Repository is public; never place confidential records here |
| Integration safety | Integration inventory, permission review, sandbox tests | Each external integration has documented scope, credentials handling, least privilege and manual fallback | MCP/config files do not prove integrations are live |
| Deployment | Environment-specific deployment record, health check, rollback procedure | Exact release commit deployed and health-checked in a controlled environment | CI and GitHub Pages do not certify the complete operating system |
| Operational acceptance | Named operator, SOP, incident path, monitoring, user acceptance | Owner signs off on actual end-to-end workflows with synthetic data first | Requires explicit owner review |

## 3. Cash recognition state machine

The following states must remain distinct:

1. **FORECAST** — estimated or scenario amount; never included in cash collected.
2. **INVOICED** — invoice issued; not cash.
3. **RECEIVABLE** — amount due; not cash.
4. **PENDING_VERIFICATION** — receipt document or reference supplied but not independently checked; cash collected remains zero.
5. **RECEIVED_VERIFIED** — independent bank evidence reconciled to payer, amount, currency, date and transaction; still subject to the required approval control.
6. **APPROVED** — authorized reviewer approves recognition in the cash ledger.
7. **REJECTED / REVERSED** — evidence invalid, duplicate, mismatched, reversed or otherwise not eligible; cash collected is zero or adjusted through a documented reversal.

A non-empty receipt reference, a screenshot without independent reconciliation, a self-reported boolean, an invoice, or a contract is not sufficient proof of cash receipt.

## 4. Commercial matching state machine

- **HOLD_UNVERIFIED:** one or more demand/supply evidence gates are missing.
- **NO_MATCH:** specification, destination, currency, quantity or another mandatory compatibility condition fails.
- **MATCHED_FOR_HUMAN_REVIEW:** all required evidence is present and matching rules pass; this is a recommendation only.
- **APPROVED_FOR_EXTERNAL_ACTION:** an authorized human has approved a specific action, counterparty, scope and communication.
- **CLOSED:** outcome and evidence are recorded.

A matching engine must not turn a match into an order, purchase, quotation, contract, or payment automatically.

## 5. Release checklist

Before any production label or external launch:

- [ ] Run the supervised quality workflow against the exact release commit.
- [ ] Review all failed, skipped, and warning checks.
- [ ] Install and launch the intended product surface on a clean machine.
- [ ] Test backup and restore using non-sensitive synthetic data.
- [ ] Verify that secrets and confidential data are absent from Git history and current tracked files.
- [ ] Test cash and commercial controls against missing, invalid, duplicate, mismatched and reversed evidence.
- [ ] Verify that no external action can bypass the human approval gate.
- [ ] Review privacy, access control, encryption, retention and incident response for the actual deployment.
- [ ] Complete end-to-end user acceptance with synthetic data.
- [ ] Record owner approval, release commit, environment, date and known limitations.

## 6. Explicit non-goals of CI

The GitHub Actions workflow in this repository performs source validation, automated tests and a demo workbook build. It does not:

- discover or verify live tenders, buyers, suppliers or market demand;
- connect to a bank or verify a real bank receipt;
- send emails or WhatsApp messages;
- submit tenders or RFQs;
- issue binding quotations, sign agreements, purchase, invest or make payments;
- deploy and operate every web, desktop, API, MCP or local application surface;
- prove revenue, customer usage, or cash collected.

## 7. Evidence and change control

For each release, retain the commit SHA, CI run URL, test summary, build artifact identifier, deployment environment (if any), reviewer, owner approval and known limitations. Never label a proposed control as implemented or a test as passed without a corresponding result.
