'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import styles from './tasks.module.css';

type Task = {
  id: string;
  title: string;
  dueDate: string;
  completed: boolean;
  createdAt: string;
};

type Filter = 'all' | 'open' | 'completed';
const STORAGE_KEY = 'navaris-tasks-v1';

function readTasks(): Task[] {
  try {
    const stored: unknown = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]');
    if (!Array.isArray(stored)) return [];
    return stored.filter((task): task is Task =>
      task && typeof task.id === 'string' && typeof task.title === 'string'
      && typeof task.completed === 'boolean' && typeof task.createdAt === 'string'
      && typeof task.dueDate === 'string',
    );
  } catch {
    return [];
  }
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [filter, setFilter] = useState<Filter>('all');
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setTasks(readTasks());
    setReady(true);
  }, []);

  useEffect(() => {
    if (!ready) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
    } catch {
      // Keep the current session usable if browser storage is unavailable or full.
    }
  }, [tasks, ready]);

  const remaining = tasks.filter((task) => !task.completed).length;
  const completed = tasks.length - remaining;
  const visibleTasks = useMemo(() => tasks.filter((task) => {
    if (filter === 'open') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  }), [filter, tasks]);

  function addTask(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const cleanTitle = title.trim();
    if (!cleanTitle) return;
    const task: Task = {
      id: globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`,
      title: cleanTitle,
      dueDate,
      completed: false,
      createdAt: new Date().toISOString(),
    };
    setTasks((current) => [task, ...current]);
    setTitle('');
    setDueDate('');
  }

  function toggleTask(id: string) {
    setTasks((current) => current.map((task) => task.id === id ? { ...task, completed: !task.completed } : task));
  }

  function deleteTask(id: string) {
    setTasks((current) => current.filter((task) => task.id !== id));
  }

  function clearCompleted() {
    setTasks((current) => current.filter((task) => !task.completed));
  }

  return (
    <main className={styles.page} dir="rtl">
      <header className={styles.topbar}>
        <a className={styles.brand} href="/" aria-label="NAVARIS الرئيسية">
          <span className={styles.logo}>N</span>
          <span>NAVARIS<small>BUSINESS OPERATIONS</small></span>
        </a>
        <a className={styles.backLink} href="/">العودة للموقع / Back to site</a>
      </header>

      <section className={styles.workspace}>
        <div className={styles.heading}>
          <span className={styles.eyebrow}>PERSONAL WORKSPACE · LOCAL ONLY</span>
          <h1>قائمة مهامي <span>/ My tasks</span></h1>
          <p>نظّم خطواتك اليومية. تحفظ المهام في هذا المتصفح على هذا الجهاز فقط.</p>
          <p className={styles.english} dir="ltr">Organize your next steps. Tasks are stored in this browser on this device only.</p>
        </div>

        <div className={styles.stats} aria-label="Task summary">
          <div><span>المهام المفتوحة / Open</span><strong>{ready ? remaining : '—'}</strong></div>
          <div><span>مكتملة / Completed</span><strong>{ready ? completed : '—'}</strong></div>
          <div><span>الإجمالي / Total</span><strong>{ready ? tasks.length : '—'}</strong></div>
        </div>

        <form className={styles.addForm} onSubmit={addTask}>
          <label className={styles.titleField}>
            <span>مهمة جديدة / New task</span>
            <input value={title} onChange={(event) => setTitle(event.target.value)} maxLength={180} required placeholder="ما الخطوة التالية؟ / What is the next step?" />
          </label>
          <label className={styles.dateField}>
            <span>موعد (اختياري) / Due date (optional)</span>
            <input type="date" value={dueDate} onChange={(event) => setDueDate(event.target.value)} />
          </label>
          <button className={styles.addButton} type="submit">إضافة مهمة / Add task <span aria-hidden="true">＋</span></button>
        </form>

        <div className={styles.listHeader}>
          <h2>قائمة العمل / To-do list</h2>
          <div className={styles.controls}>
            <label className={styles.filterLabel}>
              <span className={styles.visuallyHidden}>تصفية المهام / Filter tasks</span>
              <select value={filter} onChange={(event) => setFilter(event.target.value as Filter)}>
                <option value="all">كل المهام / All</option>
                <option value="open">المفتوحة / Open</option>
                <option value="completed">المكتملة / Completed</option>
              </select>
            </label>
            <button type="button" className={styles.clearButton} onClick={clearCompleted} disabled={completed === 0}>حذف المكتمل / Clear completed</button>
          </div>
        </div>

        {!ready ? <div className={styles.emptyState}>جارٍ تحميل المهام… / Loading tasks…</div> : visibleTasks.length === 0 ? (
          <div className={styles.emptyState}>
            <span className={styles.emptyIcon}>✓</span>
            <strong>{filter === 'completed' ? 'لا توجد مهام مكتملة بعد' : filter === 'open' ? 'أحسنت! لا توجد مهام مفتوحة' : 'قائمتك فارغة'}</strong>
            <span>{filter === 'all' ? 'أضف أول خطوة لتبدأ. / Add your first task to get started.' : 'جرّب تغيير التصفية. / Try changing the filter.'}</span>
          </div>
        ) : (
          <ul className={styles.taskList}>
            {visibleTasks.map((task) => (
              <li className={`${styles.task} ${task.completed ? styles.isCompleted : ''}`} key={task.id}>
                <label className={styles.taskLabel}>
                  <input type="checkbox" checked={task.completed} onChange={() => toggleTask(task.id)} aria-label={`${task.completed ? 'إعادة فتح' : 'إكمال'}: ${task.title}`} />
                  <span className={styles.checkmark} aria-hidden="true">✓</span>
                  <span className={styles.taskCopy}>
                    <strong>{task.title}</strong>
                    {task.dueDate && <small>الموعد / Due: <time dateTime={task.dueDate}>{task.dueDate}</time></small>}
                  </span>
                </label>
                <button type="button" className={styles.deleteButton} onClick={() => deleteTask(task.id)} aria-label={`حذف المهمة / Delete task: ${task.title}`}>حذف / Delete</button>
              </li>
            ))}
          </ul>
        )}

        <aside className={styles.notice}>
          <span aria-hidden="true">ⓘ</span>
          <p><strong>تنبيه الخصوصية / Privacy note:</strong> هذه قائمة شخصية تجريبية تحفظ محليًا، وليست قاعدة بيانات مشتركة أو سجلًا آمنًا للعملاء. لا تحفظ فيها معلومات سرية.</p>
        </aside>
      </section>
      <footer className={styles.footer}>NAVARIS · قائمة مهام محلية / Local task list</footer>
    </main>
  );
}
