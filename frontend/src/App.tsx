import './App.css'
import { metrics, players } from './dashboardData'
import cLogo from './assets/c-logo.png'
import cppLogo from './assets/cpp-logo.png'

function App() {
  return (
    <main className="dashboard-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <section className="hero hero-wide">
        <img className="hero-art hero-art-left" src={cLogo} alt="" aria-hidden="true" />
        <div className="hero-title-wrap">
          <h1>
            <span>Admin</span>
          </h1>
        </div>
        <img className="hero-art hero-art-right" src={cppLogo} alt="" aria-hidden="true" />
      </section>

      <section className="metrics-grid" aria-label="Key metrics">
        {metrics.map((metric) => (
          <article className={`metric-card accent-${metric.accent}`} key={metric.label}>
            <div className="metric-label">{metric.label}</div>
            <div className="metric-value">{metric.value}</div>
          </article>
        ))}
      </section>

      <section className="content-grid">
        <article className="panel panel-wide players-panel">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Players</p>
              <h2>Active sessions</h2>
            </div>
            <div className="panel-badge">1,284 online</div>
          </div>

          <div className="players-list">
            {players.map((player) => (
              <div className="player-row" key={player.name}>
                <div className="player-row-left">
                  <span className="avatar">{player.name.slice(0, 1)}</span>
                  <div>
                    <strong>{player.name}</strong>
                    <span>{player.role}</span>
                  </div>
                </div>

                <div className="player-row-meta">
                  <span>{player.server}</span>
                  <strong>{player.ping}</strong>
                </div>

                <p className="player-activity">{player.activity}</p>
              </div>
            ))}
          </div>
        </article>
      </section>
    </main>
  )
}

export default App
