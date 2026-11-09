export type ProjectTask = {
  id: string;
  title: string;
  owner: string;
  dueDate: string;
  status: 'not_started' | 'in_progress' | 'done';
};

export type RaidItem = {
  id: string;
  category: 'risk' | 'assumption' | 'issue' | 'dependency';
  description: string;
  owner: string;
  response: string;
  status: 'open' | 'monitoring' | 'closed';
};

export type Stakeholder = {
  id: string;
  name: string;
  role: string;
  influence: number;
  interest: number;
  engagement: string;
};

export type NavarisProject = {
  id: string;
  name: string;
  client: string;
  objective: string;
  scope: string;
  owner: string;
  startDate: string;
  targetDate: string;
  status: 'draft' | 'active' | 'on_hold' | 'completed';
  createdAt: string;
  updatedAt: string;
  tasks: ProjectTask[];
  raid: RaidItem[];
  stakeholders: Stakeholder[];
};

const STORAGE_KEY = 'navaris-projects-v1';

function isProject(value: unknown): value is NavarisProject {
  if (!value || typeof value !== 'object') return false;
  const project = value as Partial<NavarisProject>;
  return typeof project.id === 'string'
    && typeof project.name === 'string'
    && typeof project.client === 'string'
    && typeof project.objective === 'string'
    && typeof project.scope === 'string'
    && typeof project.owner === 'string'
    && typeof project.createdAt === 'string'
    && typeof project.updatedAt === 'string'
    && Array.isArray(project.tasks)
    && Array.isArray(project.raid)
    && Array.isArray(project.stakeholders);
}

export function loadProjects(): NavarisProject[] {
  try {
    const parsed: unknown = JSON.parse(window.localStorage.getItem(STORAGE_KEY) ?? '[]');
    return Array.isArray(parsed) ? parsed.filter(isProject) : [];
  } catch {
    return [];
  }
}

export function saveProjects(projects: NavarisProject[]): boolean {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(projects));
    return true;
  } catch {
    return false;
  }
}

export function newRecordId(): string {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export function createProject(input: Pick<NavarisProject, 'name' | 'client' | 'objective' | 'owner'>): NavarisProject {
  const now = new Date().toISOString();
  return {
    id: newRecordId(),
    ...input,
    scope: '',
    startDate: '',
    targetDate: '',
    status: 'draft',
    createdAt: now,
    updatedAt: now,
    tasks: [],
    raid: [],
    stakeholders: [],
  };
}
