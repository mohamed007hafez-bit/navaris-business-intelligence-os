# NAVARIS Toolkit / Playbook — quick-start for the existing repository

**Version:** 1.0 draft | **Language:** Arabic + English | **Audience:** Mohamed Hafez and authorized internal users

> **Status note:** This playbook organizes and connects existing NAVARIS components; it does not assert that every agent, integration, source feed, or deployment is complete. Missing evidence remains missing. Do not contact a client or send an output externally without Mohamed Hafez's explicit approval of that exact output and recipient.

## 1. Product split / فصل المنتج

| Surface / المساحة | Purpose / الغرض | Access / الوصول |
|---|---|---|
| Public website / الموقع العام | Explain services and receive qualified inquiries / شرح الخدمات واستقبال طلبات العملاء | Public; marketing only / عام؛ للتسويق فقط |
| NAVARIS Toolkit / الأدوات الداخلية | Reusable checklists, formulas, source evidence, working files, QA and draft outputs / قوائم الفحص والمعادلات والمصادر وملفات العمل وضبط الجودة والمسودات | Mohamed Hafez and authorized team / محمد حافظ والفريق المصرح له |
| Client preview / المعاينة للعميل | Approved limited summary only / ملخص محدود ومعتمد فقط | Share only after human review / لا يُشارك إلا بعد المراجعة البشرية |

## 2. Start here / ابدأ من هنا

1. Read `NAVARIS_FORMULA_FIRST_PROTOCOL.md` before performing analysis. / اقرأ بروتوكول Formula-First قبل التحليل.
2. Check `toolkit/index.json` for toolkit phases and evidence/status definitions. / راجع فهرس الأدوات لمعرفة المراحل وحالة التحقق.
3. Use `docs/NAVARIS_TOOLKIT_87.md` as an internal control checklist; checkpoints are not passed until evidence, owner, date and reviewer are recorded. / استخدم قائمة الـ87 نقطة داخليًا ولا تعتبرها مجتازة دون دليل ومسؤول وتاريخ ومراجع.
4. Select an existing domain folder under `toolkit/` and read its README before editing or generating a deliverable. / اختر مجلد المجال الموجود واقرأ README قبل التعديل أو إنشاء مخرج.
5. For existing local workbook workflows, follow `docs/NAVARIS-LOCAL-HYBRID-OPERATING-MANUAL.md`; run demo inputs first. / لتشغيل ملفات Excel الحالية، اتبع الدليل المحلي وابدأ ببيانات تجريبية.
6. Record every source as a dated, attributable evidence record; distinguish verified fact, user-provided input, assumption, calculation and unknown. / سجّل كل مصدر بتاريخه ونسبته، وافصل الحقيقة عن مدخل المستخدم والافتراض والحساب والمعلومة المجهولة.
7. Run tests and inspect workbook outputs before any proposed internal use. Mark all unreviewed output **DRAFT — INDICATIVE ONLY**. / شغّل الاختبارات وافحص الملف، واجعل كل مخرج غير معتمد مسودة استرشادية.

## 3. Use existing tools / الاستفادة من الموجود

| Need / الاحتياج | Existing asset / الأصل الموجود | Current boundary / الحد الحالي |
|---|---|---|
| Business/financial toolkit methods / منهجيات الأعمال والمال | `toolkit/` and `toolkit/index.json` | Status may be proposed or partial; inspect evidence and tests per method. / قد تكون الحالة مقترحة أو جزئية؛ افحص أدلة كل منهجية واختباراتها. |
| Formula and evidence discipline / انضباط المعادلات والأدلة | `NAVARIS_FORMULA_FIRST_PROTOCOL.md` | State formula, units, inputs, evidence, calculation, limits, action and validation. / أظهر الصيغة والوحدات والمدخلات والدليل والحساب والحدود والإجراء والتحقق. |
| Local Excel/workbook operation / تشغيل Excel محليًا | `main.py`, `run_navaris_local.bat`, `run_navaris_local.sh`, `engines/legacy_route_pricing.py` | Demo/supplied-input workflow; not live tender discovery or verified client finance. / يعمل على بيانات تجريبية أو مدخلة؛ لا يعني البحث الحي أو التحقق المالي للعميل. |
| Local screening interface / واجهة فحص أولي محلية | `navaris_all_in_one.py` | Its own header says deterministic planning scenarios; it does not perform external research. Validate assumptions before use. / سيناريوهات تخطيط حتمية ولا تجري بحثًا خارجيًا؛ راجع الافتراضات قبل الاستخدام. |
| Internal API / واجهة API داخلية | `backend/main.py` | Preliminary/evidence-required service; review identity, security, endpoint contracts and tests before production. / واجهة أولية تتطلب أدلة؛ راجع الهوية والأمان والعقود والاختبارات قبل الإنتاج. |
| Public site / الموقع العام | Root `index.html` plus `WEBSITE.md` | Reuse existing page and styling; do not expose internal console or private tools. / طوّر الصفحة والتصميم الموجودين ولا تكشف لوحة التشغيل أو الأدوات الخاصة. |
| Cross-platform workspace / مساحة متعددة المنصات | `cross-platform/` | Scaffold, not a production-ready integrated application. / هيكل أولي وليس تطبيقًا متكاملًا جاهزًا للإنتاج. |

## 4. Standard work sequence / تسلسل العمل القياسي

**Intake → Evidence → Formula → Analysis → Risk → QA → Human approval → Limited client output**

**الاستقبال ← الأدلة ← المعادلة ← التحليل ← المخاطر ← ضبط الجودة ← موافقة بشرية ← مخرج محدود للعميل**

- Intake: define the decision, scope, period, owner, permission and required files. / الاستقبال: عرّف القرار والنطاق والفترة والمسؤول والإذن والملفات.
- Evidence: assign source IDs and capture document, page/sheet, date, currency, unit and verification status. / الأدلة: أعطِ كل مصدر رقمًا وسجّل المستند والصفحة/الورقة والتاريخ والعملة والوحدة وحالة التحقق.
- Formula: show the governing equation and define each variable before calculating. / المعادلة: اعرض الصيغة وعرّف متغيراتها قبل الحساب.
- Analysis: use only supplied/verified inputs. Do not turn blank into zero or assume a live market value. / التحليل: استخدم المدخلات المتاحة أو المتحقق منها؛ لا تحوّل الفراغ إلى صفر ولا تفترض سعر سوق حي.
- QA: independently check arithmetic, formula, currency, source coverage, assumptions, and client-safe disclosure. / الجودة: راجع الحساب والصيغة والعملة وتغطية المصادر والافتراضات وسلامة الإفصاح للعميل.
- Human gate: Mohamed Hafez reviews the exact recipient, channel and final content. No agent sends or publishes to a client. / بوابة الإنسان: يراجع محمد حافظ المستلم والقناة والنص النهائي؛ لا يرسل أي وكيل للعميل.

## 5. Excel vs database / Excel مقابل قاعدة البيانات

Use Excel for editable analysis templates, input collection, controlled calculations, and deliverable exports. Keep formula/version/source notes in the workbook. Do not use Excel files as the only multi-user system of record for client, pipeline, approval or audit data. The existing repository documents local SQLite as a placeholder and warns against storing confidential client/bank data in unencrypted storage. Do not use Microsoft Access as the new platform's core database. Choose a properly secured, backed-up database only after authentication, authorization, privacy, retention and recovery requirements are designed and tested.

استخدم Excel للتحليل القابل للتعديل وجمع المدخلات والحسابات والمخرجات، مع توثيق المعادلة والإصدار والمصدر. لا تجعله سجلًا مركزيًا متعدد المستخدمين للعملاء أو الموافقات. توثيق المستودع يذكر أن SQLite محلي تجريبي ويحذر من تخزين بيانات العملاء أو البنوك الحساسة دون تشفير. لا تعتمد Access قاعدةً جديدة للمنصة. لا تختَر قاعدة إنتاج قبل تصميم واختبار الدخول والصلاحيات والخصوصية والنسخ الاحتياطي والاستعادة.

## 6. Seven-hour focused sprint / سبرنت عمل مركز لسبع ساعات

This is a proposed work sequence, not a claim that seven hours of autonomous work continue in the background. / هذا ترتيب مقترح للعمل وليس ادعاءً بوجود تنفيذ تلقائي في الخلفية.

| Timebox | Work / العمل | Acceptance evidence / دليل القبول |
|---|---|---|
| 0:00–0:45 | Inventory current toolkit, docs, scripts, tests and active site; mark existing/deprecated/unknown. / حصر الأدوات والوثائق والاختبارات والموقع وتصنيف حالتها. | Inventory with links and actual status; no deletion by guess. / جرد بروابط وحالة حقيقية دون حذف بالتخمين. |
| 0:45–2:15 | Run existing local checks and demo workbook workflow; log failures and fix only confirmed defects. / تشغيل الاختبارات وملف Excel التجريبي وتسجيل وإصلاح العيوب المؤكدة فقط. | Test log, generated demo artifact and workbook inspection. / سجل الاختبار وملف تجريبي وفحص الأوراق. |
| 2:15–3:30 | Consolidate toolkit entry points, formula/source templates, error handling and internal run instructions. / تنظيم مداخل الأدوات وقوالب المعادلات والمصادر والأخطاء ودليل التشغيل. | Internal checklist and traceable example with non-real demo data. / قائمة تحقق ومثال قابل للتتبع ببيانات تجريبية. |
| 3:30–5:00 | Adapt the existing public page to the `WEBSITE.md` split: service story + CTA buttons; remove unsupported live/example claims. / تطوير الموقع الموجود ليكون تسويقيًا بأزرار واضحة وحذف الادعاءات التجريبية المضللة. | Mobile/link/accessibility checks and Pages workflow result. / فحص الهاتف والروابط والإتاحة ونتيجة النشر. |
| 5:00–6:00 | Prepare service offer copy and approved-content queue; leave YouTube URL blank until supplied. / تجهيز وصف الخدمات وقائمة محتوى للموافقة وترك رابط YouTube فارغًا حتى تزويده. | Drafts only; no outbound sends or fabricated social proof. / مسودات فقط دون إرسال أو إثبات اجتماعي مختلق. |
| 6:00–7:00 | Run regression/security/content checks; record remaining blockers, owner, next action and deployment state. / إعادة اختبارات الجودة والأمان والمحتوى وتسجيل العوائق والمسؤول والخطوة التالية وحالة النشر. | Evidence-based completion report; no production claim without evidence. / تقرير مثبت بالأدلة دون ادعاء جاهزية إنتاجية بلا دليل. |

## 7. Operating controls / ضوابط التشغيل

- Missing source/value: `DATA MISSING` or `UNKNOWN`; do not invent. / المصدر أو القيمة الناقصة: `DATA MISSING` أو `UNKNOWN` دون اختلاق.
- User-specified zero: retain `0`, record the specified error code where required, and request evidence. / الصفر المدخل من المستخدم يبقى صفرًا مع رمز الخطأ المناسب وطلب الدليل.
- Exchange rates, prices, tenders, vessel status, safety/regulatory facts and availability must be dated and sourced; never call a supplied scenario value an official live rate. / أسعار الصرف والأسعار والمناقصات وحالة السفن والسلامة واللوائح والتوفر تتطلب مصدرًا وتاريخًا.
- Keep source registry, full analysis, supplier details, contracts and workpapers internal; never expose them in the free client preview. / أبقِ سجل المصادر والتحليل الكامل والموردين والعقود وأوراق العمل داخلية.
- No direct client contact, no messaging automation, no bids, commitments, contracts or publishing without Mohamed Hafez's explicit human approval. / لا تواصل مباشر ولا إرسال آلي ولا عروض أو التزامات أو عقود أو نشر دون موافقة صريحة من محمد حافظ.
- Existing workflow does not imply a running scheduler, connected AI provider, live web research, active payment processor or deployed app. Verify each integration separately. / وجود ملفات لا يعني وجود جدولة أو مزود AI أو بحث حي أو دفع أو تطبيق منشور؛ تحقّق من كل تكامل على حدة.

## 8. Required output for each work item / المخرج المطلوب لكل مهمة

`TASK ID | Objective | Existing asset reused | Files changed | Formula/source | Tests run + result | Human approval state | Deployment state | Blockers | Next action`

`رقم المهمة | الهدف | الأصل الموجود المستخدم | الملفات المعدلة | المعادلة/المصدر | الاختبارات والنتيجة | حالة الموافقة البشرية | حالة النشر | العوائق | الخطوة التالية`
