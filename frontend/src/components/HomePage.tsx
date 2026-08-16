import { useEffect, useState } from 'react'
import { listAgents, listWorkflows } from '../api/client'

export default function HomePage() {
  const [agentCount, setAgentCount] = useState(0)
  const [workflowCount, setWorkflowCount] = useState(0)

  useEffect(() => {
    listAgents().then(d => setAgentCount(d.agents.length)).catch(() => {})
    listWorkflows().then(d => setWorkflowCount(d.workflows.length)).catch(() => {})
  }, [])

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Microsoft Agent Framework Code Builder</h1>
      </div>

      <p style={{ color: 'var(--text-secondary)', marginBottom: 32, maxWidth: 680, lineHeight: 1.7, fontSize: 14 }}>
        إنشاء كود وكلاء الذكاء الاصطناعي وسير العمل تلقائيًا باستخدام اللغة الطبيعية.
        باستخدام مهارات Microsoft Agent Framework، يمكنك إنشاء الكود وتحريره واختباره بشكل تفاعلي.
      </p>

      <div className="grid-home">
        <div className="card">
          <div className="card-title">🤖 الوكلاء</div>
          <p className="stat-value">{agentCount}</p>
          <p className="stat-label">الوكلاء المُنشأون</p>
        </div>

        <div className="card">
          <div className="card-title">🔀 سير العمل</div>
          <p className="stat-value">{workflowCount}</p>
          <p className="stat-label">مسارات العمل المُنشأة</p>
        </div>
      </div>

      <div className="card" style={{ marginTop: 24, maxWidth: 680 }}>
        <div className="card-title" style={{ marginBottom: 12 }}>البنية المعمارية</div>

        <pre className="code-block">{`
┌─────────────────────────────────────────┐
│       الواجهة الأمامية (React + TS)     │
│  ┌────────────┐  ┌───────────────────┐  │
│  │ إنشاء وكيل │  │ إنشاء سير العمل   │  │
│  │ (طبيعي/يدوي)│ │ (طبيعي/يدوي/تحرير)│ │
│  └─────┬──────┘  └────────┬──────────┘  │
└────────┼──────────────────┼─────────────┘
         │     REST API     │
┌────────┼──────────────────┼─────────────┐
│        ▼                  ▼             │
│  ┌────────────────────────────────┐     │
│  │          وكيل التنسيق           │     │
│  │       (Azure OpenAI GPT-4o)    │     │
│  └──────┬──────────────┬─────────┘     │
│         │              │               │
│  ┌──────▼─────┐ ┌──────▼──────────┐   │
│  │ مهارة      │ │ مهارة            │   │
│  │ إنشاء      │ │ إنشاء            │   │
│  │ الوكلاء    │ │ سير العمل       │   │
│  │ ┌────────┐ │ │ ┌────────────┐  │   │
│  │ │SKILL.md│ │ │ │SKILL.md    │  │   │
│  │ │scripts/│ │ │ │scripts/    │  │   │
│  │ │refs/   │ │ │ │refs/       │  │   │
│  │ └────────┘ │ │ └────────────┘  │   │
│  └────────────┘ └─────────────────┘   │
│        الواجهة الخلفية (FastAPI)       │
└────────────────────────────────────────┘
        `.trim()}</pre>
      </div>
    </div>
  )
}