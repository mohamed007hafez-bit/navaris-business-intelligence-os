'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { createProject, loadProjects, NavarisProject, saveProjects } from '@/lib/projects';
import styles from './projects.module.css';

export default function ProjectsPage() {
  const [projects, setProjects] = useState<NavarisProject[]>([]);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState('');
  const [name, setName] = useState('');
  const [client, setClient] = useState('');
  const [objective, setObjective] = useState('');
  const [owner, setOwner] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    setProjects(loadProjects());
    setReady(true);
  }, []);

  useEffect(() => {
    if (!ready) return;
    if (!saveProjects(projects)) setError('تعذر الحفظ. قد تكون مساحة المتصفح ممتلئة. / Could not save; browser storage may be full.');
    else setError('');
  }, [projects, ready]);

  const visible = useMemo(() => projects.filter((project) => filter === 'all' || project.status === filter), [projects, filter]);

  function addProject(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const cleanName = name.trim();
    if (!cleanName) return;
    setProjects((current) => [createProject({
      name: cleanName,
      client: client.trim(),
      objective: objective.trim(),
      owner: owner.trim(),
    }), ...current]);
    setName(''); setClient(''); setObjective(''); setOwner('');
  }

  const statusLabel: Record<NavarisProject['status'], string> = {
    draft: 'مسودة / Draft', active: 'نشط / Active', on_hold: 'متوقف مؤقتًا / On hold', completed: 'مكتمل / Completed',
  };

  return (
    <main className={styles.page} dir="rtl">
      <header className={styles.topbar}>
        <Link className={styles.brand} href="/"><span className={styles.logo}>N</span><span>NAVARIS<small>PROJECT DELIVERY</small></span></Link>
        <nav><Link href="/tasks">قائمة المهام / To-do list</Link><Link href="/">الموقع / Website</Link></nav>
      </header>
      <section className={styles.container}>
        <div className={styles.heading}><span className={styles.eyebrow}>PROJECT DELIVERY WORKSPACE · LOCAL PREVIEW</span><h1>مساحة المشاريع <span>/ Project workspace</span></h1><p>أنشئ مشروعًا، ثم نظّم النطاق والمهام والمخاطر وأصحاب المصلحة في مكان واحد.</p><p className={styles.en} dir="ltr">Create a project and organize scope, tasks, RAID items, and stakeholders in one place.</p></div>
        <div className={styles.privacy}><strong>نسخة محلية تجريبية / Local preview</strong><span>البيانات محفوظة في هذا المتصفح فقط. لا تستخدم معلومات سرية أو بيانات عميل حقيقية. / Data stays in this browser. Do not enter confidential or real client information.</span></div>
        <section className={styles.panel}>
          <h2>مشروع جديد / New project</h2>
          <form className={styles.form} onSubmit={addProject}>
            <label>اسم المشروع / Project name<input value={name} onChange={(e) => setName(e.target.value)} required maxLength={120} placeholder="مثال: تحسين دورة التسليم / e.g. Delivery improvement" /></label>
            <label>العميل (اختياري) / Client (optional)<input value={client} onChange={(e) => setClient(e.target.value)} maxLength={120} placeholder="اسم تجريبي فقط / Demo name only" /></label>
            <label className={styles.wide}>الهدف / Objective<input value={objective} onChange={(e) => setObjective(e.target.value)} maxLength={300} placeholder="ما النتيجة التي تريد تحقيقها؟ / What outcome is needed?" /></label>
            <label>مسؤول المشروع / Project owner<input value={owner} onChange={(e) => setOwner(e.target.value)} maxLength={100} placeholder="المسؤول / Owner" /></label>
            <button type="submit" className={styles.primary}>إنشاء مساحة / Create workspace <span>＋</span></button>
          </form>
        </section>
        {error && <p className={styles.error} role="alert">{error}</p>}
        <div className={styles.listHead}><h2>المشاريع / Projects <small>{ready ? projects.length : '—'}</small></h2><label><span className={styles.srOnly}>تصفية حسب الحالة / Filter by status</span><select value={filter} onChange={(e) => setFilter(e.target.value)}><option value="all">كل الحالات / All statuses</option><option value="draft">مسودة / Draft</option><option value="active">نشط / Active</option><option value="on_hold">متوقف / On hold</option><option value="completed">مكتمل / Completed</option></select></label></div>
        {!ready ? <div className={styles.empty}>جارٍ تحميل المشاريع… / Loading…</div> : visible.length === 0 ? <div className={styles.empty}><strong>لا توجد مشاريع هنا بعد / No projects yet</strong><span>أنشئ أول مساحة مشروع من النموذج أعلاه. / Create your first workspace above.</span></div> : (
          <div className={styles.grid}>{visible.map((project) => <Link className={styles.card} href={`/projects/${encodeURIComponent(project.id)}`} key={project.id}>
            <div className={styles.cardTop}><span className={styles.projectMark}>PRJ</span><span className={styles.status}>{statusLabel[project.status]}</span></div>
            <h3>{project.name}</h3><p className={styles.client}>{project.client || 'عميل غير محدد / Client not specified'}</p><p className={styles.objective}>{project.objective || 'الهدف غير محدد بعد / Objective not set yet'}</p>
            <div className={styles.cardMeta}><span>المهام / Tasks <b>{project.tasks.length}</b></span><span>RAID <b>{project.raid.filter((item) => item.status !== 'closed').length}</b></span></div>
            <span className={styles.open}>فتح مساحة المشروع / Open project <b>←</b></span>
          </Link>)}</div>
        )}
      </section>
    </main>
  );
}
