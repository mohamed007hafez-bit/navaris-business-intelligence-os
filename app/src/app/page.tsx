'use client';

import { FormEvent, useState } from 'react';

type IntakeDraft = {
  id: string;
  createdAt: string;
  sector: string;
  need: string;
  contact: string;
};

const services = [
  {
    number: '01',
    title: 'تشخيص وتحسين الأعمال / Business Diagnostic',
    text: 'حوّل المشكلة التشغيلية أو الإدارية إلى تشخيص منظم، أدلة مطلوبة، وخطوات قابلة للمتابعة. / Turn a business or operations problem into a structured diagnosis, evidence needs, and trackable next steps.',
  },
  {
    number: '02',
    title: 'جاهزية المعدات والطلبات / Equipment & RFQ Readiness',
    text: 'رتّب المواصفات والمستندات والفجوات قبل بدء التنسيق مع الأطراف المناسبة. / Organize specifications, documents, and gaps before coordinating with suitable parties.',
  },
  {
    number: '03',
    title: 'العمليات واللوجستيات / Operations & Logistics',
    text: 'وضّح المسؤوليات والتكاليف والمراحل والمخاطر مع توثيق مصدر كل معلومة. / Clarify responsibilities, costs, milestones, and risks while recording the source of each fact.',
  },
];

export default function Home() {
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  function saveDraft(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    const form = new FormData(event.currentTarget);
    const draft: IntakeDraft = {
      id: `NAV-${Date.now()}`,
      createdAt: new Date().toISOString(),
      sector: String(form.get('sector') ?? ''),
      need: String(form.get('need') ?? '').trim(),
      contact: String(form.get('contact') ?? '').trim(),
    };

    try {
      const existing = JSON.parse(localStorage.getItem('navaris-intake-drafts') ?? '[]');
      const drafts = Array.isArray(existing) ? existing : [];
      localStorage.setItem('navaris-intake-drafts', JSON.stringify([...drafts, draft]));
      setSubmitted(true);
      event.currentTarget.reset();
    } catch {
      setError('تعذر حفظ المسودة على هذا الجهاز. / Could not save the draft on this device.');
    }
  }

  return (
    <main className="site-shell" dir="rtl">
      <header className="site-nav">
        <a className="site-brand" href="#home" aria-label="NAVARIS home">
          <span className="site-brand-mark">N</span>
          <span>NAVARIS <small>BUSINESS OPERATIONS</small></span>
        </a>
        <nav aria-label="التنقل الرئيسي / Main navigation">
          <a href="#services">الخدمات / Services</a>
          <a href="#method">طريقة العمل / How it works</a>
          <a className="site-nav-cta" href="#intake">ابدأ طلبك / Start an enquiry</a>
        </nav>
      </header>

      <section className="site-hero" id="home">
        <div className="site-hero-copy">
          <span className="site-eyebrow">منهج واضح. أدلة موثقة. تنفيذ منظم. / CLEAR METHOD · TRACEABLE EVIDENCE · CONTROLLED EXECUTION</span>
          <h1>حوّل تعقيد الأعمال<br /><em>إلى خطوات واضحة.</em></h1>
          <p className="site-lead">NAVARIS تساعدك على تنظيم المشكلة، جمع الأدلة، وتحديد الخطوة التالية — مع مراجعة بشرية قبل أي مخرجات أو تواصل خارجي.</p>
          <p className="site-lead site-lead-en" dir="ltr">NAVARIS helps structure the problem, organize evidence, and identify next steps—with human review before any client-facing output or external communication.</p>
          <div className="site-actions">
            <a className="site-button site-button-primary" href="#intake">ابدأ بطلب منظم / Start a structured enquiry <span>←</span></a>
            <a className="site-text-link" href="#method">اعرف طريقة العمل / See the process</a>
          </div>
          <div className="site-trust-note"><span className="site-dot" /> لا نخمّن البيانات. المعلومات الناقصة تظل واضحة. / No invented figures. Missing information stays visible.</div>
        </div>

        <aside className="site-preview" aria-label="NAVARIS workflow preview">
          <div className="preview-top"><span>WORKSPACE PREVIEW</span><span className="preview-status">● REVIEW-GATED</span></div>
          <div className="preview-title">مساحة عملك / Your workspace</div>
          <p className="preview-caption">تنتقل كل حالة عبر خطوات واضحة، لا وعود تلقائية. / Every case moves through defined steps, not automated promises.</p>
          <div className="preview-step"><span>01</span><div><b>استلام الطلب / Intake</b><small>النطاق والاحتياج / Scope and need</small></div><i>✓</i></div>
          <div className="preview-step"><span>02</span><div><b>مراجعة الأدلة / Evidence review</b><small>المصادر والفجوات / Sources and gaps</small></div><i>···</i></div>
          <div className="preview-step"><span>03</span><div><b>توصيات للمراجعة / Recommendations</b><small>مسودة — تنتظر المراجعة / Draft — pending review</small></div><i>○</i></div>
          <div className="preview-footer"><span>DECISION CONTROL</span><strong>موافقة بشرية قبل الإرسال / Human approval before sending</strong></div>
        </aside>
      </section>

      <section className="site-proof-strip" aria-label="Operating principles">
        <div><b>01</b><span>البيانات لها مصدر / Source-backed data</span></div>
        <div><b>02</b><span>المخرجات مسودات / Outputs stay drafts</span></div>
        <div><b>03</b><span>لا إرسال آلي للعملاء / No automated client outreach</span></div>
      </section>

      <section className="site-section" id="services">
        <div className="site-section-heading"><span className="site-eyebrow">WHAT WE HELP ORGANIZE</span><h2>خدمات تبدأ من المشكلة<br />وتنتهي بخطوة قابلة للتنفيذ.</h2><p>النطاق النهائي يُحدّد بعد فهم الطلب والأدلة المتاحة. / Final scope is agreed after understanding the request and available evidence.</p></div>
        <div className="site-services">{services.map((service) => <article className="site-service-card" key={service.number}><span>{service.number}</span><h3>{service.title}</h3><p>{service.text}</p><a href="#intake">ناقش احتياجك / Discuss your need <b>←</b></a></article>)}</div>
      </section>

      <section className="site-method" id="method">
        <div><span className="site-eyebrow">A CONTROLLED WORKFLOW</span><h2>من الطلب إلى القرار.<br />كل خطوة قابلة للمراجعة.</h2></div>
        <ol><li><b>افهم الاحتياج / Understand</b><span>نحدد المشكلة والنطاق والبيانات المتاحة.</span></li><li><b>راجع الأدلة / Verify</b><span>نُظهر المصادر والمعلومات الناقصة بدل التخمين.</span></li><li><b>نظّم الخيارات / Structure</b><span>مسودة توصيات وخطوات ومؤشرات مناسبة للحالة.</span></li><li><b>اعتمد قبل الإرسال / Approve</b><span>لا تواصل خارجي ولا التزام دون موافقة بشرية.</span></li></ol>
      </section>

      <section className="site-intake" id="intake">
        <div className="intake-copy"><span className="site-eyebrow">START WITH THE FACTS</span><h2>احكِ لنا عن احتياجك.</h2><p>ابدأ بملخص عام. لا تضع كلمات مرور أو بيانات بنكية أو ملفات سرية في هذا النموذج التجريبي.</p><div className="intake-privacy">🔒 <span>هذه النسخة تحفظ المسودة على هذا المتصفح فقط، ولا ترسلها إلى NAVARIS. / This preview stores the draft in this browser only; it does not send it to NAVARIS.</span></div></div>
        <form className="site-form" onSubmit={saveDraft}>
          <label>مجال العمل / Business area<select name="sector" required defaultValue=""><option value="" disabled>اختر المجال / Select an area</option><option>تشخيص الأعمال / Business diagnostic</option><option>الطاقة والمعدات / Energy & equipment</option><option>العمليات واللوجستيات / Operations & logistics</option><option>أخرى / Other</option></select></label>
          <label>ما التحدي الذي تريد تنظيمه؟ / What challenge do you want to address?<textarea name="need" required minLength={10} maxLength={1200} placeholder="اكتب وصفاً عاماً، دون بيانات حساسة... / Describe it briefly; do not include sensitive data..." /></label>
          <label>وسيلة تواصل (اختياري) / Contact (optional)<input name="contact" maxLength={160} placeholder="بريد إلكتروني أو رقم عمل / Business email or phone" /></label>
          <button className="site-button site-button-primary" type="submit">حفظ مسودة على هذا الجهاز / Save a local draft <span>←</span></button>
          {submitted && <p className="form-success" role="status">تم حفظ المسودة على هذا الجهاز فقط. لم يتم إرسالها. / Draft saved on this device only. Nothing was sent.</p>}
          {error && <p className="form-error" role="alert">{error}</p>}
        </form>
      </section>

      <footer className="site-footer"><a className="site-brand" href="#home"><span className="site-brand-mark">N</span><span>NAVARIS <small>BUSINESS OPERATIONS</small></span></a><p>منصة لتنظيم الأعمال والقرارات — بأدلة ومراجعة بشرية. / A system for structured business operations and decisions—grounded in evidence and human review.</p><span>© NAVARIS · Mohamed Hafez</span></footer>
    </main>
  );
}
