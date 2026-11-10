# NAVARIS Launch Roadmap

Status: Active implementation plan
Owner: Mohamed Hafez
Repository: mohamed007hafez-bit/navaris-business-intelligence-os

## 1. Mission

NAVARIS is a business operations and intelligence platform for managing client intake, evidence-backed diagnosis, execution planning, KPI tracking, and controlled business communication.

The platform must follow these rules:
- one source of truth for business data
- evidence before claims
- human approval before outbound client communication
- no invented numbers
- cash and performance metrics must be traceable

## 2. Implementation Principles

1. Canonical records first
   - client records
   - opportunity records
   - evidence log
   - cash ledger
   - supplier register

2. Human approval gate
   - no message, offer, or proposal is sent externally without review

3. Formula-first operations
   - all dashboards use formulas with source tags
   - missing data is marked DATA MISSING, not guessed

4. Modular architecture
   - app/client portal
   - backend logic
   - data layer
   - evidence and claims registry
   - dashboard and reporting

## 3. Target Product Structure

- Public gateway / landing site
- Client intake and qualification workflow
- Business diagnostic workspace
- Decision dashboard
- Evidence registry
- Proposal and approval layer
- Cash and KPI monitor

## 4. Launch Phases

### Phase 0 — Repository stabilization
Goal: remove duplication risk and clarify canonical files.

Actions:
- keep `index.html` as canonical public website entry
- keep `navaris_core_engine.py` as the definitive formula engine
- keep `docs/NAVARIS_MASTER_STRATEGY_EXECUTION_BLUEPRINT.md` as policy source
- archive legacy duplicates after comparison
- enforce one canonical workflow per purpose

Deliverables:
- authoritative file registry
- de-duplication register
- implementation ownership map

### Phase 1 — Core data model and evidence schema
Goal: establish the minimum working structure that can support real business processes.

Core entities:
- Client
- Opportunity
- Supplier
- EvidenceRecord
- CashReceipt
- KPIRecord
- DecisionNote
- Offer

Required fields:
- id
- owner
- status
- created_at
- updated_at
- source_reference
- approved_by

Deliverables:
- `data/clients.json`
- `data/opportunities.json`
- `data/suppliers.json`
- `data/evidence.json`
- `data/cash-receipts.json`
- `data/kpis.json`

### Phase 2 — Client portal and intake workflow
Goal: create a clean client-facing flow with approval constraints.

Features:
- landing page
- intake form
- qualification status
- business problem capture
- source upload placeholder
- draft proposal generation
- only founder-approved send action

Scope:
- app shell in `app/`
- form schema, validation, and state
- secure storage via Supabase or local-safe placeholder
- no external payment processing yet

### Phase 3 — Diagnostics and strategy engine
Goal: convert raw inputs into actionable analysis.

Modules:
- company profile
- market and competition review
- financial and risk analysis
- turnaround options
- scenario planning

Rules:
- no metric without source
- all outputs marked DRAFT until human approval
- derived values must show formula and source

### Phase 4 — Dashboard and KPI controls
Goal: produce a reliable operational business view.

Dashboard blocks:
- cash collected
- qualified opportunities
- conversion rate
- SLA compliance
- evidence coverage
- risk alerts

Every metric must include:
- definition
- source
- period
- owner
- status

### Phase 5 — Launch readiness
Goal: prepare the product for public release in a controlled, trust-safe form.

Release checks:
- all claims verified
- external communication disabled except approved actions
- no confidential financial data in repo
- validation tests for formulas and data integrity
- one-page executive summary for investor / client briefing

## 5. First Execution Sequence

### Immediate next tasks
1. Confirm canonical app shell and data schema
2. Build the `data` layer and JSON models
3. Create the intake form and qualification checklist
4. Connect the dashboard to the KPI model
5. Add approval gating and audit trail

### Current focus (Phase 1)
- create the canonical data directory
- define the client and opportunity schema
- define evidence and cash rules
- create validation rules for missing data

## 6. Minimal MVP Definition

The first launchable MVP must include:
- one client intake flow
- one evidence registry
- one financial diagnostic model
- one KPI dashboard
- one approval gate before sending

This MVP is enough to test the value proposition without exposing the business to unverified claims.

## 7. Quality Gates

Before any release:
- all formulas pass tests
- all numbers are source-traceable
- all public claims have evidence tags
- no fake or copied client data
- all outbound actions require explicit approval

## 8. Delivery Timeline

Week 1
- finalize data schemas and file ownership
- define MVP pages and workflows

Week 2
- implement intake + evidence layer
- test formula and dashboard logic

Week 3
- add client-facing diagnostics and approvals
- prepare launch checklist

Week 4
- harden release process and launch

## 9. Decision

The business should launch as a governed operating system, not as a free-form tool pack. The first release is a controlled intelligence layer for structured client work, diagnostics, and execution oversight.

This roadmap is the working baseline for the next implementation step.
