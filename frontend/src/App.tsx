import './App.css'

type ServiceStatus = 'healthy' | 'warning'

type Metric = {
  label: string
  value: string
  hint: string
  trend: string
  accent: string
}

type ServiceCard = {
  name: string
  status: ServiceStatus
  details: string
  latency: string
  fill: number
}

type Player = {
  name: string
  role: string
  server: string
  ping: string
  activity: string
}

const metrics: Metric[] = [
  {
    label: 'Redis',
    value: '98.7%',
    hint: 'cache hit rate',
    trend: '+4.1% today',
    accent: 'violet',
  },
  {
    label: 'Postgres',
    value: '124 ms',
    hint: 'avg query time',
    trend: '-18 ms vs. yesterday',
    accent: 'magenta',
  },
  {
    label: 'Server Uptime',
    value: '99.98%',
    hint: 'last 30 days',
    trend: '42 days 18h active',
    accent: 'blue',
  },
  {
    label: 'Players',
    value: '1,284',
    hint: 'online right now',
    trend: '+96 in the last hour',
    accent: 'green',
  },
  {
    label: 'Load',
    value: '2.61',
    hint: '1 / 5 / 15 min avg',
    trend: 'stable after peak',
    accent: 'amber',
  },
]

const services: ServiceCard[] = [
  {
    name: 'Redis cluster',
    status: 'healthy',
    details: 'Replica sync active, eviction policy stable',
    latency: '8 ms',
    fill: 86,
  },
  {
    name: 'Postgres primary',
    status: 'warning',
    details: 'Connection pool at 73%, vacuum scheduled',
    latency: '124 ms',
    fill: 73,
  },
  {
    name: 'Game session API',
    status: 'healthy',
    details: 'Requests flowing cleanly through the edge',
    latency: '31 ms',
    fill: 91,
  },
]

const players: Player[] = [
  {
    name: 'Nova',
    role: 'Admin',
    server: 'EU-West 3',
    ping: '18 ms',
    activity: 'Managing server settings',
  },
  {
    name: 'Echo',
    role: 'Moderator',
    server: 'EU-Central 1',
    ping: '24 ms',
    activity: 'Reviewing chat reports',
  },
  {
    name: 'Mira',
    role: 'Builder',
    server: 'US-East 2',
    ping: '41 ms',
    activity: 'Testing world changes',
  },
  {
    name: 'Rook',
    role: 'Player',
    server: 'EU-West 3',
    ping: '32 ms',
    activity: 'In lobby',
  },
]

const loadBars = [54, 68, 72, 59, 86, 77, 63, 81, 74, 69, 91, 88]

function App() {
  return (
    <main className="dashboard-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <section className="hero">
        <div>
          <p className="eyebrow">Infrastructure overview</p>
          <h1>Admin dashboard</h1>
          <p className="hero-text">
            Live health signals for cache, database, player activity and server
            load in one clean panel.
          </p>
        </div>

        <div className="status-pill">
          <span className="status-dot" />
          Live monitoring
        </div>
      </section>

      <section className="metrics-grid" aria-label="Key metrics">
        {metrics.map((metric) => (
          <article className={`metric-card accent-${metric.accent}`} key={metric.label}>
            <div className="metric-label-row">
              <span className="metric-label">{metric.label}</span>
              <span className="metric-trend">{metric.trend}</span>
            </div>
            <div className="metric-value">{metric.value}</div>
            <div className="metric-hint">{metric.hint}</div>
          </article>
        ))}
      </section>

      <section className="content-grid">
        <article className="panel panel-wide">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Server load</p>
              <h2>Traffic distribution</h2>
            </div>
            <div className="panel-badge">Current: 2.61</div>
          </div>

          <div className="load-card">
            <div className="load-legend">
              <span>1m</span>
              <span>5m</span>
              <span>15m</span>
            </div>
            <div className="load-bars" aria-hidden="true">
              {loadBars.map((value, index) => (
                <span
                  className="load-bar"
                  key={`${value}-${index}`}
                  style={{ height: `${value}%` }}
                />
              ))}
            </div>
            <div className="load-footer">
              <span>CPU threads balanced</span>
              <span>Queue depth: 12</span>
            </div>
          </div>
        </article>

        <article className="panel">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Database</p>
              <h2>Service health</h2>
            </div>
          </div>

          <div className="service-list">
            {services.map((service) => (
              <div className="service-card" key={service.name}>
                <div className="service-topline">
                  <div>
                    <div className="service-name">{service.name}</div>
                    <div className="service-details">{service.details}</div>
                  </div>
                  <span className={`service-status ${service.status}`}>
                    {service.status}
                  </span>
                </div>

                <div className="service-meter" aria-hidden="true">
                  <span style={{ width: `${service.fill}%` }} />
                </div>

                <div className="service-bottomline">
                  <span>Latency</span>
                  <strong>{service.latency}</strong>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="content-grid bottom-grid">
        <article className="panel panel-wide">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Players</p>
              <h2>Active sessions</h2>
            </div>
            <div className="panel-badge">1,284 online</div>
          </div>

          <div className="table-shell">
            <div className="table-head">
              <span>Player</span>
              <span>Server</span>
              <span>Ping</span>
              <span>Activity</span>
            </div>

            {players.map((player) => (
              <div className="table-row" key={player.name}>
                <div className="player-cell">
                  <span className="avatar">{player.name.slice(0, 1)}</span>
                  <div>
                    <strong>{player.name}</strong>
                    <span>{player.role}</span>
                  </div>
                </div>
                <span>{player.server}</span>
                <span>{player.ping}</span>
                <span>{player.activity}</span>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <div className="panel-header">
            <div>
              <p className="panel-kicker">Uptime</p>
              <h2>Reliability snapshot</h2>
            </div>
          </div>

          <div className="uptime-card">
            <div className="uptime-value">42d 18h 14m</div>
            <p className="uptime-text">
              No critical incidents in the last 30 days. Scheduled maintenance
              window on Friday at 02:00.
            </p>

            <div className="uptime-grid">
              <div>
                <span>Redis</span>
                <strong>99.99%</strong>
              </div>
              <div>
                <span>Postgres</span>
                <strong>99.94%</strong>
              </div>
              <div>
                <span>API</span>
                <strong>99.98%</strong>
              </div>
              <div>
                <span>Players</span>
                <strong>99.91%</strong>
              </div>
            </div>
          </div>
        </article>
      </section>
    </main>
  )
}

export default App
