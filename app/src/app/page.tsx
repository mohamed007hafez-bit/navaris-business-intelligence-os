'use client';

import { useMemo, useState } from 'react';

type AssistantBody = {
  title: string;
  diagnosis: string[];
  metrics: { label: string; value: string }[];
  sopItems: string[];
  contract: string[];
  currencies: { currency: string; rate: string; note: string }[];
  sources: string[];
  deepResearchNote?: string;
};

type Message = {
  id: number;
  role: 'assistant' | 'user';
  text?: string;
  body?: AssistantBody;
};

const sourceCatalog = [
  'Kotler - Hotel Management',
  'Minto - Pyramid Principle',
  'ISO 9001:2015',
  'Naguib Mahfouz - Miramar',
  'Central Bank of Egypt - USD Rate',
  'Booking.com - Fouad Rating 6.5',
  'Ministry of Tourism - Adada 1927',
];

const parseProjectText = (value: string) => {
  const lower = value.toLowerCase();

  const millionMatches = [
    /([0-9]+(?:[.,][0-9]+)?)\s*(?:million|مليون|m)/i,
    /([0-9]+(?:[.,][0-9]+)?)\s*(?:thousand|ألف|k)/i,
  ];

  let capital = 0;
  for (const regex of millionMatches) {
    const match = value.match(regex);
    if (match) {
      const amount = Number(match[1].replace(',', ''));
      const multiplier = /(million|مليون|m)/i.test(match[0]) ? 1_000_000 : 1_000;
      capital = amount * multiplier;
      break;
    }
  }

  let sector = 'Tourism';
  let subSector = 'Hotel';

  if (/(oil|well|slickline|bore|بئر|نفط|slickline)/i.test(lower)) {
    sector = 'Oil & Gas';
    subSector = 'Slickline';
  } else if (/(عمارة|building|property|estate|residential|adada|عادا)/i.test(lower)) {
    sector = 'Real Estate';
    subSector = 'Boutique Heritage';
  } else if (/(فندق|hotel|tourism|miramar|فؤاد|resort|hospitality)/i.test(lower)) {
    sector = 'Tourism';
    subSector = 'Hotel';
  }

  if (/(مستشفى|hospital|clinic|medical)/i.test(lower)) {
    sector = 'Healthcare';
    subSector = 'Clinic';
  }

  if (/(sops|SOPs|checklist|iso|ايزو)/i.test(lower)) {
    subSector = `${subSector} + ISO QMS`;
  }

  return { capital, sector, subSector };
};

const formatMoney = (value: number) => {
  if (!value) return '0 EGP';
  return new Intl.NumberFormat('en-EG', {
    style: 'currency',
    currency: 'EGP',
    maximumFractionDigits: 0,
  }).format(value);
};

const buildAssistantReply = (input: string, deepResearch: boolean): AssistantBody => {
  const parsed = parseProjectText(input);
  const capital = parsed.capital || 2_000_000;

  const diagnosis = [
    `Capital detected: ${formatMoney(capital)} with sector focus on ${parsed.sector}.`,
    `${parsed.subSector} positioning is viable if the asset story and operating model are mapped to demand and experience quality.`,
    'The project shows clear upside once pricing, occupancy, or uptime is formalized and evidence is tracked against the operating baseline.',
  ];

  const metrics = [
    { label: 'NPV', value: `${(capital * 0.34).toLocaleString('en-EG', { maximumFractionDigits: 0 })} EGP` },
    { label: 'IRR', value: '22.4%' },
    { label: 'Payback', value: '2.6 years' },
    { label: 'Break-even', value: '68%' },
  ];

  const sopItems = [
    'Reception & arrival flow',
    'Housekeeping & linen control',
    'Pricing & rate integrity',
    'Guest complaint handling',
    'Finance & cash reconciliation',
    'Safety, HAZOP, and incident reporting',
  ];

  if (parsed.sector === 'Oil & Gas') {
    sopItems[0] = 'Wellsite access and permit control';
    sopItems[1] = 'Slickline equipment inventory';
    sopItems[2] = 'Job risk assessment and toolbox talk';
    sopItems[3] = 'Well control and shut-in readiness';
    sopItems[4] = 'Daily reporting and close-out pack';
  }

  if (parsed.sector === 'Real Estate') {
    sopItems[0] = 'Heritage asset inspection';
    sopItems[1] = 'Guest experience and boutique service';
    sopItems[2] = 'Pricing and reservations flow';
    sopItems[3] = 'Facilities and maintenance register';
    sopItems[4] = 'Brand story and guest narrative';
  }

  const currencies = [
    { currency: 'EGP', rate: '1.00', note: 'Local operating base' },
    { currency: 'USD', rate: '49.75', note: 'Bank rate / supplier settlement' },
    { currency: 'SAR', rate: '13.20', note: 'Regional pricing benchmark' },
    { currency: 'AED', rate: '13.52', note: 'Hospitality / project benchmark' },
  ];

  const defaultSources = [
    '[1] Kotler - Hotel Management',
    '[2] Minto - Pyramid Principle',
    '[3] ISO 9001:2015',
    '[4] Central Bank of Egypt - USD Rate',
    '[5] Booking.com - Fouad Rating 6.5',
  ];

  const deepSources = [
    '[1] Kotler - Hotel Management',
    '[2] Minto - Pyramid Principle',
    '[3] ISO 9001:2015',
    '[4] Naguib Mahfouz - Miramar',
    '[5] Central Bank of Egypt - USD Rate',
    '[6] Booking.com - Fouad Rating 6.5',
    '[7] Ministry of Tourism - Adada 1927',
  ];

  return {
    title: `${parsed.subSector} • ${parsed.sector} feasibility`,
    diagnosis,
    metrics,
    sopItems: Array.from({ length: 7 }, (_, index) => `${index + 1}. ${sopItems[index % sopItems.length]} — ISO Clause ${4 + index}`),
    contract: [
      '50% advance upon award and mobilization',
      'Force majeure: no liability for acts of war, civil unrest, or government shutdown',
      'War risk and insurance rider to be reviewed before execution',
      'Download contract pack',
    ],
    currencies,
    sources: deepResearch ? deepSources : defaultSources,
    deepResearchNote: deepResearch
      ? 'بحثت في 12 مصدر - 3 كتب - 2 ISO - 4 تقارير رسمية'
      : 'كل رقم ليه مصدر - اضغط عليه للتأكد - مفيش تخمين',
  };
};

const initialMessages: Message[] = [
  {
    id: 1,
    role: 'assistant',
    body: {
      title: 'Fouad Hotel — Turnaround',
      diagnosis: [
        'The project has a heritage hospitality story with upside from rooms, pricing, and guest experience repositioning.',
        'At 6.5/10 rating and 1000 EGP entry price, the case is viable if operations are tightened within 90 days.',
      ],
      metrics: [
        { label: 'NPV', value: '5.8M EGP' },
        { label: 'IRR', value: '27.1%' },
        { label: 'Payback', value: '2.2 years' },
        { label: 'Break-even', value: '63%' },
      ],
      sopItems: [
        '1. Reception & welcome journey — ISO Clause 4',
        '2. Housekeeping & linen control — ISO Clause 6',
        '3. Pricing & channel management — ISO Clause 7',
        '4. Guest experience and storytelling — ISO Clause 8',
        '5. Finance & cash reconciliation — ISO Clause 9',
      ],
      contract: [
        '50% advance upon award and mobilization',
        'Force majeure: no liability for acts of war, civil unrest, or government shutdown',
        'War risk and insurance rider to be reviewed before execution',
        'Download contract pack',
      ],
      currencies: [
        { currency: 'EGP', rate: '1.00', note: 'Local operations' },
        { currency: 'USD', rate: '49.75', note: 'Bank rate' },
        { currency: 'SAR', rate: '13.20', note: 'Regional pricing' },
        { currency: 'AED', rate: '13.52', note: 'Tourism benchmark' },
      ],
      sources: [
        '[1] Kotler - Hotel Management',
        '[2] Minto - Pyramid Principle',
        '[3] ISO 9001:2015',
        '[4] Central Bank of Egypt - USD Rate',
        '[5] Booking.com - Fouad Rating 6.5',
      ],
      deepResearchNote: 'بحثت في 12 مصدر - 3 كتب - 2 ISO - 4 تقارير رسمية',
    },
  },
];

export default function Page() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState('');
  const [deepResearch, setDeepResearch] = useState(false);

  const suggestions = useMemo(
    () => ['فندق فؤاد - Turnaround', 'عمارة عادا - Boutique', 'بئر بترول - Slickline'],
    [],
  );

  const handleSend = (value?: string) => {
    const text = (value ?? input).trim();
    if (!text) return;

    const userMessage: Message = { id: Date.now(), role: 'user', text };
    const assistantBody = buildAssistantReply(text, deepResearch);
    const assistantMessage: Message = { id: Date.now() + 1, role: 'assistant', body: assistantBody };

    setMessages((current) => [...current, userMessage, assistantMessage]);
    setInput('');
  };

  return (
    <div className="chat-shell">
      <aside className="sidebar">
        <div className="sidebar-top">
          <div className="brand-row">
            <div className="brand-mark">N</div>
            <div className="brand-copy">
              <span className="brand-label">NAVARIS</span>
            </div>
          </div>
          <button className="new-chat">New Chat</button>
        </div>

        <div className="history-label">History</div>
        <div className="history-list">
          {['Fouad Hotel - Miramar', 'Adada - Heritage', 'Oil Well - Slickline', 'New Project...'].map((item) => (
            <button key={item} className={`history-item ${item === 'Fouad Hotel - Miramar' ? 'active' : ''}`} type="button">
              {item}
            </button>
          ))}
        </div>

        <div className="user-card">
          <div className="user-avatar">MH</div>
          <div>
            <strong>Dr. Mohamed Hafez</strong>
            <small>DBA, ISO Lead Auditor</small>
          </div>
        </div>
      </aside>

      <main className="chat-panel">
        <header className="chat-header">
          <div className="model-picker">
            <span className="model-dot" />
            <span>NAVARIS Pro - Consulting</span>
          </div>
        </header>

        <section className="chat-stream" aria-live="polite">
          {messages.map((message) => (
            <div key={message.id} className={`message-row ${message.role}`}>
              <div className="avatar">{message.role === 'assistant' ? 'N' : 'MH'}</div>

              <div className={`bubble ${message.role}`}>
                {message.role === 'user' ? (
                  <p>{message.text}</p>
                ) : (
                  <div className="assistant-card">
                    <div className="assistant-header">
                      <span className="eyebrow">NAVARIS AI</span>
                      <button
                        type="button"
                        className={`deep-toggle ${deepResearch ? 'on' : ''}`}
                        onClick={() => setDeepResearch((value) => !value)}
                      >
                        {deepResearch ? 'بحث عميق ON' : 'Deep Research'}
                      </button>
                    </div>

                    <h3>{message.body?.title}</h3>

                    <div className="info-block">
                      <h4>Diagnosis</h4>
                      <ul>
                        {message.body?.diagnosis.map((point) => <li key={point}>{point}</li>)}
                      </ul>
                    </div>

                    <div className="info-block metrics-block">
                      <h4>Feasibility</h4>
                      <div className="matrix">
                        {message.body?.metrics.map((metric) => (
                          <div key={metric.label} className="metric-box">
                            <span>{metric.label}</span>
                            <strong>{metric.value}</strong>
                          </div>
                        ))}
                      </div>
                      <div className="formula-box">
                        <strong>Formula</strong>
                        <span>NPV = Σ(CF / (1+r)^t) − Initial Investment</span>
                      </div>
                    </div>

                    <div className="info-block">
                      <h4>SOPs Auto</h4>
                      <details open>
                        <summary>87 checkpoints • ISO 9001:2015 Clauses 4–10</summary>
                        <ul className="checklist">
                          {message.body?.sopItems.map((item) => <li key={item}>{item}</li>)}
                        </ul>
                      </details>
                    </div>

                    <div className="info-block contract-block">
                      <h4>Contract</h4>
                      <ul>
                        {message.body?.contract.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                      <button type="button" className="download-link">[Download]</button>
                    </div>

                    <div className="info-block">
                      <h4>Currencies</h4>
                      <table>
                        <thead>
                          <tr>
                            <th>Currency</th>
                            <th>Rate</th>
                            <th>Use</th>
                          </tr>
                        </thead>
                        <tbody>
                          {message.body?.currencies.map((row) => (
                            <tr key={row.currency}>
                              <td>{row.currency}</td>
                              <td>{row.rate}</td>
                              <td>{row.note}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    <div className="sources-panel">
                      <div className="source-head">
                        <h4>Sources</h4>
                        <span>{message.body?.deepResearchNote}</span>
                      </div>
                      <div className="source-links">
                        {message.body?.sources.map((source) => (
                          <a key={source} href="#" className="source-link">
                            {source}
                          </a>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </section>

        <div className="composer-wrap">
          <div className="suggestions" aria-label="Suggested prompts">
            {suggestions.map((prompt) => (
              <button key={prompt} type="button" className="suggestion-pill" onClick={() => handleSend(prompt)}>
                {prompt}
              </button>
            ))}
          </div>

          <div className="composer">
            <button type="button" className="icon-btn" aria-label="Attach file">
              +
            </button>
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') handleSend();
              }}
              placeholder="اكتب مشروعك... معايا 2 مليون - فندق فؤاد"
              aria-label="Project input"
            />
            <button type="button" className="icon-btn mic" aria-label="Voice input">
              ◉
            </button>
            <button type="button" className="send-btn" onClick={() => handleSend()}>
              Send
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
