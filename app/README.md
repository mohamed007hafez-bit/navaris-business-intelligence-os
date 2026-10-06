# NAVARIS App Layer

The app is a **Task Control Center**, not a chat-first interface.

## Primary UX

**TASKS → EXECUTION → HUMAN GATE → RESULTS → NEXT ACTION**

Chat may be used as an optional command/input surface, but the system of record is the task object and its audit trail.

## Core screens

1. **Command / New Task** — create or ingest a task.
2. **Active Tasks** — Ready, Running and Waiting work.
3. **Execution View** — plan, agent, steps, live state, evidence and exceptions.
4. **Human Gate** — decisions requiring owner approval.
5. **Results** — completed outputs, files, reports and commercial impact.
6. **Opportunity Queue** — buyer, seller, supplier, partner, representation, training, consulting and tender/RFQ opportunities.
7. **Cash Board** — prioritized tasks and opportunities by expected cash impact.
8. **Audit / History** — immutable task events and decisions.

## Task lifecycle

`DRAFT → READY → RUNNING → WAITING / HUMAN_GATE → COMPLETED / FAILED / CLOSED`

## Architecture

The UI consumes the NAVARIS task schema from `data/task.schema.json`. Core business logic remains independent of the UI. Agent workflows live in `agents/`, deterministic business logic in `engines/`, evidence and structured data in `data/`, and reusable outputs in `templates/`.

## Result-first rule

Every task ends with:

**Result → Evidence → KPI / Cash impact → Next action**

See `docs/task-operating-system.md` for the full task-first operating model.
