import { useState, useEffect } from 'react'
import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import AgentBuilderPage from './components/AgentBuilderPage'
import WorkflowBuilderPage from './components/WorkflowBuilderPage'
import HomePage from './components/HomePage'

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('theme')
    return saved === 'dark'
  })
  const location = useLocation()

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light')
    localStorage.setItem('theme', darkMode ? 'dark' : 'light')
  }, [darkMode])

  const closeSidebar = () => setSidebarOpen(false)

  // إغلاق الشريط الجانبي عند تغيير المسار (على الهاتف)
  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `sidebar-link ${isActive ? 'active' : ''}`

  return (
    <div className={`app-layout ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      {/* ترويسة الهاتف */}
      <div className="mobile-header">
        <button
          className="mobile-hamburger"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          {sidebarOpen ? '✕' : '☰'}
        </button>
        <span className="mobile-title">منشئ أكواد MAF</span>
      </div>

      {/* طبقة التعتيم */}
      <div
        className={`sidebar-overlay ${
          sidebarOpen ? 'sidebar-overlay--visible' : ''
        }`}
        onClick={closeSidebar}
      />

      {/* الشريط الجانبي */}
      <nav className={`sidebar ${sidebarOpen ? 'sidebar--open' : ''}`}>
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">⚡</div>

          {!sidebarCollapsed && (
            <div className="sidebar-brand-text">
              <h1>إطار الوكلاء</h1>
              <span className="sidebar-subtitle">منشئ الأكواد</span>
            </div>
          )}
        </div>

        {!sidebarCollapsed && (
          <div className="sidebar-section">التنقل</div>
        )}

        <NavLink
          to="/"
          end
          className={navLinkClass}
          onClick={closeSidebar}
        >
          <span className="sidebar-link-icon">🏠</span>
          {!sidebarCollapsed && 'الرئيسية'}
        </NavLink>

        <NavLink
          to="/agents"
          className={navLinkClass}
          onClick={closeSidebar}
        >
          <span className="sidebar-link-icon">🤖</span>
          {!sidebarCollapsed && 'الوكلاء'}
        </NavLink>

        <NavLink
          to="/workflows"
          className={navLinkClass}
          onClick={closeSidebar}
        >
          <span className="sidebar-link-icon">🔀</span>
          {!sidebarCollapsed && 'سير العمل'}
        </NavLink>

        <div style={{ flex: 1 }} />

        <button
          className="sidebar-theme-btn"
          onClick={() => setDarkMode(prev => !prev)}
          title={
            darkMode
              ? 'التبديل إلى الوضع الفاتح'
              : 'التبديل إلى الوضع الداكن'
          }
        >
          {darkMode ? '☀️' : '🌙'}
          {!sidebarCollapsed &&
            (darkMode ? ' فاتح' : ' داكن')}
        </button>

        <button
          className="sidebar-collapse-btn"
          onClick={() => setSidebarCollapsed(prev => !prev)}
          title={
            sidebarCollapsed
              ? 'فتح الشريط الجانبي'
              : 'إغلاق الشريط الجانبي'
          }
        >
          {sidebarCollapsed ? '»' : '«'}
        </button>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/agents" element={<AgentBuilderPage />} />
          <Route
            path="/workflows"
            element={<WorkflowBuilderPage />}
          />
        </Routes>
      </main>
    </div>
  )
}