export type Metric = {
  label: string
  value: string
  accent: string
}

export type Player = {
  name: string
  role: string
  server: string
  ping: string
  activity: string
}

export const metrics: Metric[] = [
  {
    label: 'Redis',
    value: '98.7%',
    accent: 'violet',
  },
  {
    label: 'Postgres',
    value: '124 ms',
    accent: 'magenta',
  },
  {
    label: 'Server Uptime',
    value: '0h 0m 0s',
    accent: 'blue',
  },
  {
    label: 'Players',
    value: '1,284',
    accent: 'green',
  },
  {
    label: 'Load',
    value: '2.61',
    accent: 'amber',
  },
]

export const players: Player[] = [
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
