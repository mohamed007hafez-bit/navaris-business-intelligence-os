'use client';

import { FormEvent, useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { loadProjects, NavarisProject, newRecordId, RaidItem, saveProjects, ProjectTask, Stakeholder } from '@/lib/projects';
import styles from '../projects.module.css';

type Tab = 'overview' | 'tasks' | 'raid' | 'stakeholders';

export default function ProjectDetailPage() {
  const params = useParams<{ id: string }>();
  const projectId = decodeURIComponent(params.id);
  const [projects, setProjects] = useState<NavarisProject[]>([]);
  const [ready, setReady] = useState(false);
  const [tab, setTab] = useState<Tab>('overview');
  const [taskTitle, setTaskTitle] = useState('');
  const [taskOwner, setTaskOwner] = useState('');
  const [taskDate, setTaskDate] = useState('');
  const [raidCategory, setRaidCategory] = useState<RaidItem['category']>('risk');
  const [raidDescription, setRaidDescription] = useState('');
  const [raidOwner, setRaidOwner] = useState('');
  const [raidResponse, setRaidResponse] = useState('');
  const [stakeholderName, setStakeholderName] = useState('');
  const [stakeholderRole, setStakeholderRole] = useState('');
  const [notice, setNotice] = useState('');

  useEffect(() => { setProjects(loadProjects()); setReady(true); }, []);
  useEffect(() => {
    if (!ready) return;
    setNotice(saveProjects(projects) ? '' : 'تعذر حفظ التغييرات في المتصفح. / Could not save changes in browser storage.');
  }, [projects, ready]);

  const project = projects.find((item) => item.id === projectId);
  function updateProject(update: (current: NavarisProject) => NavarisProject) {
    setProjects((current) => current.map((item) => item.id === projectId ? { ...update(item), updatedAt: new Date().toISOString() } : item));
  }

  function addTask(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const title = taskTitle.trim(); if (!title) return;
    const task: ProjectTask = { id: newRecordId(), title, owner: taskOwner.trim(), dueDate: taskDate, status: 'not_started' };
    updateProject((current) => ({ ...current, tasks: [task, ...current.tasks] }));
    setTaskTitle(''); setTaskOwner(''); setTaskDate('');
  }
  function addRaid(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const description = raidDescription.trim(); if (!description) return;
    const item: RaidItem = { id: newRecordId(), category: raidCategory, description, owner: raidOwner.trim(), response: raidResponse.trim(), status: 'open' };
    updateProject((current) => ({ ...current, raid: [item, ...current.raid] }));
    setRaidDescription(''); setRaidOwner(''); setRaidResponse('');
  }
  function addStakeholder(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const name = stakeholderName.trim(); if (!name) return;
    const stakeholder: Stakeholder = { id: newRecordId(), name, role: stakeholderRole.trim(), influence: 3, interest: 3, engagement: '' };
    updateProject((current) => ({ ...current, stakeholders: [stakeholder, ...current.stakeholders] }));
    setStakeholderName(''); setStakeholderRole('');
  }
  function changeTaskStatus(id: string, status: ProjectTask['status']) {
    updateProject((current) => ({ ...current, tasks: current.tasks.map((task) => task.id === id ? { ...task, status } : task) }));
  }
  function changeRaidStatus(id: string, status: RaidItem['status']) {
    updateProject((current) => ({ ...current, raid: current.raid.map((item) => item.id === id ? { ...item, status } : item) }));
  }
  function removeTask(id: string) { updateProject((current) => ({ ...current, tasks: current.tasks.filter((item) => item.id !== id) })); }
  function removeRaid(id: string) { updateProject((current) => ({ ...current, raid: current.raid.filter((item) => item.id !== id) })); }
  function removeStakeholder(id: string) { updateProject((current) => ({ ...current, stakeholders: current.stakeholders.filter((item) => item.id !== id) })); }

  const statusText: Record<NavarisProject['status'], string> = { draft: 'مسودة / Draft', active: 'نشط / Active', on_hold: 'متوقف مؤقتًا / On hold', completed: 'مكتمل / Completed' };
  const raidText: Record<RaidItem['category'], string> = { risk: 'مخاطر / Risk', assumption: 'افتراض / Assumption', issue: 'مشكلة / Issue', dependency: 'اعتمادية / Dependency' };

  if (!ready) return <main className={styles.page} dir="rtl"><div className={styles.empty}>جارٍ تحميل المشروع… / Loading project…</div></main>;
  if (!project) return <main className={styles.page} dir="rtl"><div className={styles.container}><div className={styles.empty}><strong>المشروع غير موجود على هذا الجهاز / Project not found on this device</strong><Link href="/projects">العودة للمشاريع / Back to projects</Link></div></div></main>;

  return (
    <main className={styles.page} dir="rtl">
      <header className={styles.topbar}><Link className={styles.brand} href="/projects"><span className={styles.logo}>N</span><span>NAVARIS<small>PROJECT DELIVERY</small></span></Link><nav><Link href="/tasks">المهام / Tasks</Link><Link href="/">الموقع / Website</Link></nav></header>
      <section className={styles.container}>
        <Link className={styles.back} href="/projects">← كل المشاريع / All projects</Link>
        <div className={styles.detailHeading}><div><span className={styles.eyebrow}>PROJECT WORKSPACE · DRAFT UNTIL REVIEWED</span><h1>{project.name}</h1><p>{project.client || 'عميل غير محدد / Client not specified'} · {statusText[project.status]}</p></div><label className={styles.statusSelect}>حالة المشروع / Status<select value={project.status} onChange={(e) => updateProject((current) => ({ ...current, status: e.target.value as NavarisProject['status'] }))}><option value="draft">مسودة / Draft</option><option value="active">نشط / Active</option><option value="on_hold">متوقف / On hold</option><option value="completed">مكتمل / Completed</option></select></label></div>
        <div className={styles.privacy}><strong>تخزين محلي / Local storage</strong><span>هذا السجل محفوظ في متصفح هذا الجهاز فقط؛ ليس قاعدة بيانات مشتركة أو آمنة للعميل. لا تدخل معلومات سرية. / Stored in this browser only; not a shared or client-secure database. Do not enter confidential data.</span></div>
        {notice && <p className={styles.error} role="alert">{notice}</p>}
        <nav className={styles.tabs} aria-label="أقسام المشروع / Project sections">{([['overview','نظرة عامة / Overview'],['tasks','المهام WBS / Tasks'],['raid','سجل RAID'],['stakeholders','أصحاب المصلحة / Stakeholders']] as [Tab,string][]).map(([key,label]) => <button key={key} type="button" className={tab === key ? styles.activeTab : ''} onClick={() => setTab(key)}>{label}</button>)}</nav>

        {tab === 'overview' && <section className={styles.panel}>
          <h2>ميثاق المشروع / Project charter</h2>
          <div className={styles.form}>
            <label>اسم العميل / Client<input value={project.client} maxLength={120} onChange={(e) => updateProject((current) => ({ ...current, client: e.target.value }))} /></label>
            <label>مسؤول المشروع / Owner<input value={project.owner} maxLength={100} onChange={(e) => updateProject((current) => ({ ...current, owner: e.target.value }))} /></label>
            <label className={styles.wide}>الهدف / Objective<textarea value={project.objective} maxLength={1000} rows={3} onChange={(e) => updateProject((current) => ({ ...current, objective: e.target.value }))} /></label>
            <label className={styles.wide}>النطاق / Scope<textarea value={project.scope} maxLength={2000} rows={4} placeholder="ما الذي يشمله المشروع؟ وما الذي لا يشمله؟ / What is in scope and out of scope?" onChange={(e) => updateProject((current) => ({ ...current, scope: e.target.value }))} /></label>
            <label>تاريخ البداية / Start date<input type="date" value={project.startDate} onChange={(e) => updateProject((current) => ({ ...current, startDate: e.target.value }))} /></label>
            <label>التاريخ المستهدف / Target date<input type="date" value={project.targetDate} onChange={(e) => updateProject((current) => ({ ...current, targetDate: e.target.value }))} /></label>
          </div>
          <div className={styles.summary}><span>المهام / Tasks <b>{project.tasks.length}</b></span><span>مفتوح RAID / Open RAID <b>{project.raid.filter((item) => item.status !== 'closed').length}</b></span><span>أصحاب المصلحة / Stakeholders <b>{project.stakeholders.length}</b></span></div>
          <p className={styles.helper}>المخرجات مسودات تنظيمية، وليست توصيات معتمدة أو التزامًا تعاقديًا. / Outputs are working drafts, not approved advice or contractual commitments.</p>
        </section>}

        {tab === 'tasks' && <section className={styles.panel}><h2>هيكل تقسيم العمل / Work breakdown structure</h2>
          <form className={styles.inlineForm} onSubmit={addTask}><label>المهمة / Task<input value={taskTitle} onChange={(e) => setTaskTitle(e.target.value)} required maxLength={180} placeholder="اسم المهمة / Task name" /></label><label>المسؤول / Owner<input value={taskOwner} onChange={(e) => setTaskOwner(e.target.value)} maxLength={100} /></label><label>تاريخ الاستحقاق / Due<input type="date" value={taskDate} onChange={(e) => setTaskDate(e.target.value)} /></label><button className={styles.primary}>إضافة / Add</button></form>
          {project.tasks.length === 0 ? <div className={styles.empty}>لا توجد مهام بعد / No tasks yet.</div> : <div className={styles.tableWrap}><table className={styles.table}><thead><tr><th>المهمة / Task</th><th>المسؤول / Owner</th><th>الموعد / Due</th><th>الحالة / Status</th><th>إجراء / Action</th></tr></thead><tbody>{project.tasks.map((task) => <tr key={task.id}><td>{task.title}</td><td>{task.owner || 'غير محدد / Unassigned'}</td><td>{task.dueDate || 'غير محدد / Not set'}</td><td><select value={task.status} onChange={(e) => changeTaskStatus(task.id, e.target.value as ProjectTask['status'])}><option value="not_started">لم تبدأ / Not started</option><option value="in_progress">قيد التنفيذ / In progress</option><option value="done">مكتملة / Done</option></select></td><td><button className={styles.delete} type="button" onClick={() => removeTask(task.id)}>حذف / Delete</button></td></tr>)}</tbody></table></div>}
        </section>}

        {tab === 'raid' && <section className={styles.panel}><h2>سجل المخاطر والافتراضات والمشكلات والاعتماديات / RAID log</h2>
          <form className={styles.inlineForm} onSubmit={addRaid}><label>الفئة / Category<select value={raidCategory} onChange={(e) => setRaidCategory(e.target.value as RaidItem['category'])}><option value="risk">مخاطر / Risk</option><option value="assumption">افتراض / Assumption</option><option value="issue">مشكلة / Issue</option><option value="dependency">اعتمادية / Dependency</option></select></label><label className={styles.wide}>الوصف / Description<input value={raidDescription} onChange={(e) => setRaidDescription(e.target.value)} required maxLength={300} /></label><label>المسؤول / Owner<input value={raidOwner} onChange={(e) => setRaidOwner(e.target.value)} maxLength={100} /></label><label className={styles.wide}>الاستجابة أو الإجراء / Response<input value={raidResponse} onChange={(e) => setRaidResponse(e.target.value)} maxLength={500} /></label><button className={styles.primary}>إضافة إلى السجل / Add to log</button></form>
          {project.raid.length === 0 ? <div className={styles.empty}>لا توجد عناصر RAID بعد / No RAID items yet.</div> : <div className={styles.tableWrap}><table className={styles.table}><thead><tr><th>الفئة / Category</th><th>الوصف / Description</th><th>المسؤول / Owner</th><th>الاستجابة / Response</th><th>الحالة / Status</th><th></th></tr></thead><tbody>{project.raid.map((item) => <tr key={item.id}><td>{raidText[item.category]}</td><td>{item.description}</td><td>{item.owner || 'غير محدد / Unassigned'}</td><td>{item.response || 'غير محدد / Not set'}</td><td><select value={item.status} onChange={(e) => changeRaidStatus(item.id, e.target.value as RaidItem['status'])}><option value="open">مفتوح / Open</option><option value="monitoring">متابعة / Monitoring</option><option value="closed">مغلق / Closed</option></select></td><td><button className={styles.delete} type="button" onClick={() => removeRaid(item.id)}>حذف / Delete</button></td></tr>)}</tbody></table></div>}
        </section>}

        {tab === 'stakeholders' && <section className={styles.panel}><h2>خريطة أصحاب المصلحة / Stakeholder map</h2>
          <form className={styles.inlineForm} onSubmit={addStakeholder}><label>الاسم / Name<input value={stakeholderName} onChange={(e) => setStakeholderName(e.target.value)} required maxLength={120} /></label><label>الدور / Role<input value={stakeholderRole} onChange={(e) => setStakeholderRole(e.target.value)} maxLength={120} placeholder="مثال: راعي المشروع / Sponsor" /></label><button className={styles.primary}>إضافة / Add stakeholder</button></form>
          {project.stakeholders.length === 0 ? <div className={styles.empty}>لا يوجد أصحاب مصلحة مسجلون / No stakeholders recorded.</div> : <div className={styles.tableWrap}><table className={styles.table}><thead><tr><th>الاسم / Name</th><th>الدور / Role</th><th>التأثير / Influence</th><th>الاهتمام / Interest</th><th>نهج التواصل / Engagement approach</th><th></th></tr></thead><tbody>{project.stakeholders.map((person) => <tr key={person.id}><td>{person.name}</td><td>{person.role || 'غير محدد / Not set'}</td><td><select aria-label={`Influence ${person.name}`} value={person.influence} onChange={(e) => updateProject((current) => ({ ...current, stakeholders: current.stakeholders.map((p) => p.id === person.id ? { ...p, influence: Number(e.target.value) } : p) }))}>{[1,2,3,4,5].map((n) => <option key={n} value={n}>{n}</option>)}</select></td><td><select aria-label={`Interest ${person.name}`} value={person.interest} onChange={(e) => updateProject((current) => ({ ...current, stakeholders: current.stakeholders.map((p) => p.id === person.id ? { ...p, interest: Number(e.target.value) } : p) }))}>{[1,2,3,4,5].map((n) => <option key={n} value={n}>{n}</option>)}</select></td><td><input aria-label={`Engagement approach ${person.name}`} value={person.engagement} maxLength={300} placeholder="خطة المشاركة / Engagement plan" onChange={(e) => updateProject((current) => ({ ...current, stakeholders: current.stakeholders.map((p) => p.id === person.id ? { ...p, engagement: e.target.value } : p) }))} /></td><td><button className={styles.delete} type="button" onClick={() => removeStakeholder(person.id)}>حذف / Delete</button></td></tr>)}</tbody></table></div>}
        </section>}
      </section>
    </main>
  );
}
