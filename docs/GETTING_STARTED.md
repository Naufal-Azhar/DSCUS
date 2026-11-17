# Getting Started with DecisionMirror

This guide will help you get DecisionMirror up and running on your local machine.

## Prerequisites

Before you begin, ensure you have:

- **Docker Desktop** installed and running
- **Docker Compose** (usually included with Docker Desktop)
- **Git** for version control
- (Optional) **Node.js 20+** for local frontend development
- (Optional) **Python 3.12+** for local backend development

### Installing Docker

- **Windows/Mac**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Follow [official Docker installation guide](https://docs.docker.com/engine/install/)

## Quick Start (Docker)

The fastest way to get started is using Docker Compose:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd KIROWEEEN
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (optional for local development)
```

### 3. Start Services

#### On Windows (PowerShell)
```powershell
.\scripts\setup.ps1
```

#### On Linux/Mac
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Or manually:
```bash
docker-compose up -d
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Stop Services

```bash
docker-compose down
```

## Local Development Setup

For active development, you may want to run services locally outside Docker.

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Edit DATABASE_URL to point to localhost
export DATABASE_URL="postgresql://decisionmirror:devpassword@localhost:5432/decisionmirror"

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at http://localhost:5173 with hot-reload enabled.

### Database Only (Docker)

If running backend/frontend locally, you can run just PostgreSQL in Docker:

```bash
docker-compose up -d db
```

## Verification

### Check Service Health

```bash
# API health check
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "decisionmirror-api",
#   "version": "0.1.0",
#   "database": "connected"
# }
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f db
```

## Common Issues

### Port Already in Use

If ports 5173, 8000, or 5432 are already in use:

1. Stop conflicting services
2. Or modify ports in `docker-compose.yml`

### Docker Not Running

Ensure Docker Desktop is started before running docker-compose commands.

### Database Connection Error

If backend can't connect to database:
1. Check PostgreSQL is running: `docker-compose ps`
2. Verify DATABASE_URL in `.env`
3. Wait a few seconds for PostgreSQL to initialize

### Frontend Can't Connect to API

1. Check API is running: `curl http://localhost:8000/health`
2. Verify CORS settings in backend `.env`
3. Check browser console for CORS errors

## Next Steps

- Read [Architecture Overview](architecture/OVERVIEW.md)
- Review [API Documentation](http://localhost:8000/docs)
- Explore [Database Schema](../decisionmirror_erd.md)
- Check [Contributing Guidelines](../CONTRIBUTING.md)

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Run tests locally
4. Submit a pull request

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

### Code Quality

```bash
# Backend linting
cd backend
ruff check .
ruff format .

# Backend type checking
mypy app

# Frontend linting
cd frontend
npm run lint
```

## Troubleshooting

### Reset Everything

If something goes wrong, you can reset:

```bash
# Stop and remove all containers
docker-compose down -v

# Remove volumes (WARNING: deletes all data)
docker volume prune

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

### Access Database Directly

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U decisionmirror -d decisionmirror

# Common commands:
# \dt          - List tables
# \d sessions  - Describe sessions table
# \q           - Quit
```

## Need Help?

- Open an issue on GitHub
- Check existing documentation in `docs/`
- Review error logs with `docker-compose logs`

---

Happy decision-making! 🧠
