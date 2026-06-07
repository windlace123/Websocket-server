# WebSocket Position Server

A FastAPI WebSocket server for synchronizing player positions between multiple clients.

The main use case is a C++ client, for example a Boost.Beast WebSocket client, that connects to this server, sends its current coordinates, and receives snapshot packets with the latest positions of other connected players.

## Features

- WebSocket endpoint for real-time clients.
- Stable `player_id` assignment per connection.
- In-memory position cache for fast broadcasting.
- Redis hash storage for the latest known player positions.
- PostgreSQL table for connected player metadata.
- Fixed-rate snapshot broadcasting at 30 ticks per second.
- Docker Compose setup for Redis and PostgreSQL.

## Tech Stack

- **Python 3.12+**
- **FastAPI**
- **Uvicorn**
- **Redis**
- **PostgreSQL**
- **SQLAlchemy**
- **Docker Compose**

## Project Structure

```text
.
├── docker-compose.yml      # Redis and PostgreSQL services
├── requirements.txt        # Python dependencies
├── README.md
└── src
    ├── Main.py             # FastAPI WebSocket endpoint
    ├── conectionManager.py # Connection manager and broadcast loop
    ├── database.py         # PostgreSQL models and sessions
    └── redis.py            # Redis client
```

## Requirements

You need:

- Python 3.12 or newer.
- Docker Desktop on Windows, or Docker Engine + Docker Compose on Linux.
- Git.

Download Python from the official website:

```text
https://www.python.org/downloads/
```

Python virtual environments are created with the built-in `venv` module:

```text
https://docs.python.org/3/library/venv.html
```

## Environment Variables

Create a `.env` file in the project root. The project root is the folder that contains `README.md`, `requirements.txt`, and `docker-compose.yml`.

The final structure should look like this:

```text
.
├── .env
├── docker-compose.yml
├── requirements.txt
├── README.md
└── src
```

Create `.env` on Windows PowerShell:

```powershell
New-Item -Path .env -ItemType File
notepad .env
```

Create `.env` on Linux:

```bash
touch .env
nano .env
```

Put this content into `.env`:

```env
DB_NAME=YOUR_NAME_POSTGRES
DB_PASSWORD=YOUR_PASSWORD_POSTGRES
DB_HOST=127.0.0.1
DB_USER=YOUR_USERNAME_POSTGRES
DB_PORT=5432
```

These values must match the PostgreSQL service configuration in `docker-compose.yml`. If you change the database user, password, database name, host, or port in Docker Compose, update `.env` as well.

## Installation on Windows

Open PowerShell in the project root.

Check Python:

```powershell
python --version
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, run this once for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Check that the required packages were installed:

```powershell
pip list
```

## Installation on Linux

Open a terminal in the project root.

Check Python:

```bash
python3 --version
```

Install `venv` support if your distribution does not include it by default.

Ubuntu/Debian example:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Check that the required packages were installed:

```bash
pip list
```

## Run Redis and PostgreSQL with Docker

Start the infrastructure:

```bash
docker compose up -d
```

The same command works in Windows PowerShell and Linux shell.

Check container status:

```bash
docker compose ps
```

Follow logs:

```bash
docker compose logs -f
```

Stop containers:

```bash
docker compose down
```

Stop containers and remove Redis/PostgreSQL volumes:

```bash
docker compose down -v
```

## Run the Server on Windows

Make sure Docker services are already running, then start FastAPI:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn src.Main:app --reload --host 0.0.0.0 --port 8000
```

## Run the Server on Linux

Make sure Docker services are already running, then start FastAPI:

```bash
source venv/bin/activate
uvicorn src.Main:app --reload --host 0.0.0.0 --port 8000
```

WebSocket endpoint:

```text
ws://127.0.0.1:8000/ws
```

If another machine on the same network needs to connect, use the server machine IP instead of `127.0.0.1`.

Example:

```text
ws://192.168.1.50:8000/ws
```

## WebSocket Protocol

After connection, the server sends a welcome packet with the assigned player id:

```json
{
  "type": "welcome",
  "id": 1
}
```

The client sends its current position:

```json
{
  "type": "pos",
  "x": 10.5,
  "y": 2.0,
  "z": -4.2
}
```

The server also supports the old text format:

```text
x:10.5,y:2.0,z:-4.2
```

The server broadcasts snapshots 30 times per second:

```json
{
  "type": "snapshot",
  "tick": 123,
  "players": [
    {
      "id": 2,
      "x": 5.0,
      "y": 1.0,
      "z": 9.0
    }
  ]
}
```

The player does not receive its own position back. The `players` array contains only other connected clients.

## How It Works

1. A client connects to `/ws`.
2. The server assigns a unique `player_id`.
3. The client sends position updates.
4. The server stores the latest position in memory.
5. The server also writes the latest position to Redis.
6. A background broadcast loop sends snapshot packets to all connected clients.
7. When a client disconnects, its state is removed from memory, Redis, and PostgreSQL.

## Redis State

Latest player positions are stored in a Redis hash:

```text
players:positions
```

Example:

```text
1 -> {"x":10.5,"y":2.0,"z":-4.2}
2 -> {"x":5.0,"y":1.0,"z":9.0}
```

## Useful Commands

Compile-check Python files on Windows:

```powershell
.\venv\Scripts\python.exe -m py_compile src\Main.py src\conectionManager.py src\database.py src\redis.py
```

Compile-check Python files on Linux:

```bash
python -m py_compile src/Main.py src/conectionManager.py src/database.py src/redis.py
```

Restart Docker services:

```bash
docker compose down
docker compose up -d
```
