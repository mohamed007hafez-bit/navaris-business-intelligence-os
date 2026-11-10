# NAVARIS Product Assembly & Delivery Plan

**المالك / Owner:** محمد حافظ / Mohamed Hafez  
**الحالة / Status:** خطة تنفيذ التطوير / Development execution plan  
**قاعدة العمل / Working rule:** إعادة الاستخدام بعد الفحص، وعدم إعادة البناء لمجرد اختلاف أسماء الأدوات. / Reuse after review; do not rebuild solely because tools have different names.

## 1. قرار المنتج / Product decision

NAVARIS will be assembled as one governed business-operations product, not as a collection of unrelated HTML prototypes, toolkits, agents, and app shells.

تُبنى NAVARIS كمنتج واحد لإدارة الأعمال والتسليم، وليس كمجموعة نماذج HTML وأدوات ووكلاء وواجهات منفصلة لا رابط بينها.

- **Founder / Nucleus:** Mohamed Hafez owns the operating method, priorities, and approval decisions.
- **Workflow branches / فروع سير العمل:** intake, evidence, project delivery, financial analysis, risk, strategy, reporting, and quality checks.
- **One application shell / واجهة تطبيق واحدة:** reuse the existing Next.js client portal for the web experience; do not start a second frontend unless a proven requirement justifies it.
- **One local API / واجهة خلفية واحدة:** reuse the existing FastAPI backend for explicitly requested, deterministic workflows.
- **One canonical data contract / عقد بيانات موحد:** every workflow uses stable record IDs, owner, status, timestamps, evidence references, and review state.

## 2. Deployment boundary / حدود النشر

- GitHub Pages can serve a static public information site; it cannot run the FastAPI backend or provide a production database, authentication, or private client workspace by itself.
- A dynamic customer portal requires a server-capable deployment target and securely configured data store.
- The current `next.config.mjs` uses Next.js standalone output. Keep this application on a compatible server host unless the architecture is deliberately changed and tested for static export.
- Local preview is for synthetic/sample data only. Do not put confidential customer, financial, bank, or credentials data into the current browser-only form or unencrypted local storage.

## 3. Reuse strategy / استراتيجية إعادة الاستخدام

Do not import whole repositories blindly. For each candidate toolkit, record its exact URL, license file, relevant file paths, and proposed use. Preserve attribution and license notices when copying any content. A description saying "public use" is not sufficient license verification.

The user-described Project Management Playbook may contribute candidate artifacts, subject to source and license verification:

| Candidate artifact / الأداة المقترحة | NAVARIS workflow / سير العمل | Integration / طريقة الإدماج |
|---|---|---|
| Project Charter / ميثاق المشروع | Intake and scope / الاستقبال والنطاق | Structured project record and approval fields / سجل مشروع منظم وحقول اعتماد |
| WBS / هيكل تقسيم العمل | Delivery plan / خطة التسليم | Tasks, owner, dependency, due date, completion evidence / مهام ومسؤول واعتماديات وتاريخ ودليل إنجاز |
| RAID Log / سجل المخاطر والافتراضات والمشكلات والاعتماديات | Risk and issue management / إدارة المخاطر والمشكلات | One register with category, impact, response, owner, status, review date / سجل موحد بالفئة والأثر والاستجابة والمسؤول والحالة |
| Stakeholder Map / خريطة أصحاب المصلحة | Governance / الحوكمة | Stakeholder role, influence, interest, communication plan / الدور والتأثير والاهتمام وخطة التواصل |
| Weekly Status Report / التقرير الأسبوعي | Reporting / التقارير | Generated from project data; draft until founder approval / يُولّد من بيانات المشروع ويبقى مسودة حتى الاعتماد |
| High-level Project Plan / الخطة العامة | Project tracking / متابعة المشروع | Milestones linked to WBS tasks and RAID items / مراحل مرتبطة بالمهام والمخاطر |
| Sample project / المشروع النموذجي | QA and onboarding / الاختبار والتعريف | Synthetic data only, clearly marked fictional / بيانات وهمية معلّمة بوضوح |

**Required before reuse / مطلوب قبل إعادة الاستخدام:** exact GitHub URL, confirm current license and license scope, inspect actual template files and formats, then map only useful artifacts to the NAVARIS schema. Do not ingest a fictional sample as a real client record.

## 4. MVP scope / نطاق النسخة الأولى

Build only the smallest coherent release that demonstrates the full founder-controlled workflow:

1. Public landing page / صفحة تعريف عامة.
2. Local or authenticated intake / استقبال الطلبات محليًا أو عبر حساب موثوق.
3. Project workspace / مساحة مشروع with Charter, WBS, RAID, stakeholders, and milestones.
4. Evidence registry / سجل الأدلة with source ID, document reference, page/section, date, and verification state.
5. Deterministic calculations / حسابات محددة with formula, units, inputs, and explicit missing-data states.
6. Draft report / تقرير مسودة with a human approval gate.
7. Audit trail / سجل مراجعة for data changes and approval decisions.

Do not build payment collection, external messaging, supplier marketplace, automatic web research, or unsupervised agent execution into the first release.

## 5. Agent implementation policy / سياسة تنفيذ الوكلاء

Treat agent names as workflow responsibilities, not proof that independent AI agents already exist. Implement the following order:

1. Deterministic intake and validation.
2. Evidence and completeness checks.
3. Deterministic financial, risk, and project calculations with tests.
4. Strategy/report drafts that cite supplied evidence and label assumptions.
5. Optional AI assistance only behind a server-side provider configuration, explicit user action, privacy review, usage/cost limits, and evaluation tests.
6. External communications remain disabled unless an explicit founder approval control is implemented and tested.

Each workflow returns its inputs, missing information, calculations, source references, limitations, review state, and next actions. No invented numbers, source claims, approvals, or client contact.

## 6. Phased completion gates / مراحل الإكمال ومعاييرها

### Gate A — Baseline and remove false readiness
- Confirm canonical app, API, website entry point, and active release workflow.
- Identify hard-coded sample values and brand conflicts; keep demo material clearly fictional or remove it from client-facing screens.
- Run existing tests and record the actual results; do not report tests as passed unless executed.

### Gate B — Reusable delivery toolkit
- Obtain and review the exact Project Management Playbook repository and license.
- Select and normalize the six artifacts listed above into one bilingual project schema.
- Add synthetic examples and schema validation tests.

### Gate C — Working local MVP
- Connect UI forms to the local API and validated data records.
- Implement project workspace and review queue.
- Add unit/API/UI tests for primary workflows, missing evidence, permissions, and approval blocking.
- Provide Windows setup and one-command local startup; verify it in CI and request founder device logs only when local-environment validation is needed.

### Gate D — Production readiness
- Decide server host, domain, database, authentication, tenant isolation, secrets handling, backups, retention, privacy notice, terms, support, and legal review.
- Complete security and accessibility checks; validate production build, restore procedure, and operational monitoring.
- Keep real customer intake and external services off until required controls are reviewed.

### Gate E — Founder release approval
- Mohamed Hafez reviews the production candidate, sample client view, claims, data handling, and release checklist.
- Publish only after explicit approval. Development changes do not constitute permission to contact clients or launch publicly.

## 7. Autonomous development boundaries / حدود التطوير التلقائي

The coding agent may continue reversible, low-risk work on the development branch without asking for confirmation at every small step: code, schemas, documentation, tests, local previews, and CI fixes. It must report checkpoints and distinguish implemented, tested, and unverified items.

Founder approval remains required before: merging or pushing release changes to `main`, public deployment, enabling collection of real client data, paying for services, using credentials, deleting legacy workflows/data, contacting clients, or sending proposals/contracts. Never commit secrets, raw customer documents, or bank records.

## 8. Immediate next action / الخطوة التالية

Inspect the supplied Project Management Playbook source before importing anything. The user-provided description does not include its exact repository URL or license text. Request that URL once, then audit the license and template tree; meanwhile continue only source-independent, testable work on the existing NAVARIS development branch.
