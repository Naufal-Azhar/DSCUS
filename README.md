# DecisionMirror

**Think Before You Commit.**

DecisionMirror is a Decision Stress Testing Platform that helps students and university students make better decisions by turning personal choices into editable reasoning models.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Built for Kiroween 2026](https://img.shields.io/badge/Built%20for-Kiroween%202026-purple)](https://kiro.dev)

## 🎯 What is DecisionMirror?

DecisionMirror helps you:
- **Decompose** your decision into claims, assumptions, evidence, and alternatives
- **Challenge** your reasoning with AI-generated counterarguments
- **Stress-test** assumptions against an immutable baseline
- **Visualize** how changes propagate through your reasoning graph
- **Generate** traceable decision reports

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.12+ (for local development)

### Run with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd KIROWEEEN

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec api alembic upgrade head
```

The application will be available at:
- Frontend: http://localhost:5173
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
.
├── .kiro/                      # Kiro configuration (DO NOT IGNORE)
│   ├── specs/                  # Project specifications
│   ├── steering/               # Kiro steering prompts
│   ├── hooks/                  # Kiro hooks
│   └── agents/                 # Kiro agents
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Core configuration
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic
│   ├── alembic/               # Database migrations
│   └── tests/                 # Backend tests
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── lib/               # Utilities
│   │   └── types/             # TypeScript types
│   └── public/                # Static assets
├── infra/                      # Infrastructure config
├── docs/                       # Documentation
└── docker-compose.yml         # Service orchestration
```

## 🛠️ Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 18 with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- TanStack Query for data fetching
- React Flow for graph visualization
- React Hook Form + Zod for validation

**Backend:**
- FastAPI (Python 3.12+)
- SQLAlchemy 2.x with AsyncIO
- PostgreSQL 16
- Alembic for migrations
- NetworkX for graph algorithms
- Pydantic v2 for validation

**Infrastructure:**
- Docker & Docker Compose
- PostgreSQL
- Caddy (reverse proxy)

### Design Principles

1. **Immutable Baselines** - Decision versions are immutable snapshots
2. **Scenario Isolation** - Each stress test is isolated from the baseline
3. **Deterministic Evaluation** - Reasoning rules are transparent and reproducible
4. **Provenance Tracking** - Every element tracks its origin and authorship
5. **Privacy First** - Anonymous sessions, no tracking, user-controlled deletion

## 📚 Documentation

See the `docs/` directory for detailed documentation:
- [Architecture](docs/architecture/) - System design and technical decisions
- [API](docs/api/) - API endpoints and schemas
- [Security](docs/security/) - Security model and privacy
- [Testing](docs/testing/) - Test strategy and cases
- [Kiro Usage](docs/kiro-usage/) - How Kiro was used in development

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# Frontend tests
cd frontend
npm run test
```

## 🔐 Security & Privacy

- **Anonymous Sessions** - No user accounts required
- **Session Isolation** - Decisions are strictly isolated by session
- **Data Deletion** - Users can delete their decisions at any time
- **No Tracking** - Decision content is never logged
- **Secure by Default** - HTTPS in production, secure cookies, CSRF protection

## 📋 Roadmap

### MVP (Current)
- ✅ Decision input and storage
- ✅ Database schema and migrations
- ✅ Basic API endpoints
- ✅ Frontend structure
- 🚧 AI decomposition (LLM integration)
- 🚧 Graph visualization
- 🚧 Reasoning engine
- 🚧 Scenario testing
- 🚧 Decision report

### Post-MVP
- PDF export
- Collaborative review
- Advanced graph analytics
- Mobile app

## 🤝 Contributing

This project is being developed for Kiroween 2026. Contributions are welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Built for Kiroween 2026

This project was developed using [Kiro](https://kiro.dev), an AI-powered development environment.

See [docs/kiro-usage/](docs/kiro-usage/) for details on how Kiro was used throughout development.

## 📖 Project Specifications

Original planning documents:
- [`decisionmirror_project_spec.json`](decisionmirror_project_spec.json) - Machine-readable specification
- [`decisionmirror_implementation_blueprint.md`](decisionmirror_implementation_blueprint.md) - Implementation guide
- [`decisionmirror_erd.md`](decisionmirror_erd.md) - Database design

---

**Think Before You Commit.** 🧠
