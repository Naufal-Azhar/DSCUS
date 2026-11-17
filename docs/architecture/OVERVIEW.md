# Architecture Overview

## System Architecture

DecisionMirror follows a **modular monolith** architecture with clear separation between frontend, backend, and database layers.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  React + TypeScript + TailwindCSS + React Flow              │
│                    (Port 5173)                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────▼──────────────────────────────────────┐
│                       Backend API                            │
│         FastAPI + SQLAlchemy + NetworkX                      │
│                    (Port 8000)                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ Async SQL (asyncpg)
┌──────────────────────▼──────────────────────────────────────┐
│                    PostgreSQL 16                             │
│                    (Port 5432)                               │
└─────────────────────────────────────────────────────────────┘
```

## Core Layers

### 1. Presentation Layer (Frontend)
- **Technology**: React 18 with TypeScript
- **State Management**: TanStack Query (React Query)
- **Styling**: TailwindCSS with custom design system
- **Graph Visualization**: React Flow
- **Form Handling**: React Hook Form + Zod validation
- **Routing**: React Router v6

**Key Pages**:
- Home page with product introduction
- Decision input form (bilingual: EN/ID)
- Decision workspace (graph, scenarios, reports)

### 2. API Layer (Backend)
- **Framework**: FastAPI (async)
- **Validation**: Pydantic v2
- **ORM**: SQLAlchemy 2.x with AsyncIO
- **Graph Engine**: NetworkX for reasoning algorithms
- **Migrations**: Alembic

**API Structure**:
```
/api/v1
├── /decisions          # Decision CRUD
├── /elements           # Graph nodes and edges
├── /scenarios          # Stress test scenarios
├── /counterarguments   # Challenge review
└── /health             # Health checks
```

### 3. Data Layer (Database)
- **Database**: PostgreSQL 16
- **Schema**: Normalized relational model
- **Indexes**: Optimized for common queries
- **Constraints**: Foreign keys, unique constraints, CHECK constraints

**Core Tables**:
- `sessions` - Anonymous session management
- `decisions` - Root decision entities
- `decision_versions` - Immutable snapshots
- `nodes` - Graph nodes (claims, assumptions, etc.)
- `edges` - Graph relationships
- `scenarios` - Stress test scenarios
- `scenario_changes` - Scenario modifications
- `evaluations` - Evaluation results
- `audit_events` - Audit trail

## Design Patterns

### 1. Repository Pattern
Encapsulates data access logic in dedicated repository classes.

### 2. Service Layer Pattern
Business logic separated from API handlers.

### 3. Immutable Snapshots
Decision versions are immutable; edits create new versions.

### 4. Scenario Overlay
Scenarios apply changes as overlays without modifying baseline.

### 5. Deterministic Evaluation
Reasoning engine follows explicit, reproducible rules.

## Data Flow

### Creating a Decision
```
User Input → API Validation → Create Decision Entity → 
Create Version 1 → Return Decision ID
```

### AI Decomposition
```
Decision Context → LLM Adapter → Structured Proposal → 
User Review → Graph Builder → Save to Version
```

### Stress Testing
```
Load Baseline Version → Apply Scenario Changes → 
Evaluate Claims (NetworkX) → Calculate Impact → 
Return Diff Report
```

## Security Architecture

### Session Management
- Anonymous sessions with secure tokens
- HttpOnly, Secure cookies in production
- Session expiry after 24 hours

### Data Isolation
- Strict session-based access control
- Foreign key constraints enforce relationships
- Soft-delete for user-initiated deletion

### API Security
- CORS allowlist
- Rate limiting per endpoint
- CSRF protection
- Input validation with Pydantic

### Privacy
- No decision text in logs
- User-controlled deletion
- No cross-session data sharing

## Deployment Architecture

### Development
```
Docker Compose
├── db (PostgreSQL)
├── api (FastAPI)
└── frontend (Vite dev server)
```

### Production (Recommended)
```
VPS/Cloud Instance
├── Caddy (Reverse Proxy + SSL)
├── Frontend (Static build)
├── API (Gunicorn + Uvicorn)
└── PostgreSQL (Persistent volume)
```

## Scalability Considerations

### Current (MVP)
- Single server deployment
- Estimated capacity: 100-500 concurrent users
- Soft cap: 40 nodes per decision graph

### Future Scaling Options
1. **Horizontal scaling**: Add API replicas behind load balancer
2. **Database optimization**: Read replicas, connection pooling
3. **Caching**: Redis for session data and evaluation results
4. **Queue**: Background jobs for LLM decomposition

## Technology Choices

| Requirement | Technology | Rationale |
|------------|------------|-----------|
| Fast API development | FastAPI | Async support, auto docs, type safety |
| Type safety | TypeScript + Pydantic | Catch errors at compile/validation time |
| Graph processing | NetworkX | Mature library, deterministic algorithms |
| Async DB | asyncpg | High performance async PostgreSQL |
| UI components | shadcn/ui + Tailwind | Customizable, accessible, modern |
| Graph visualization | React Flow | Performant, interactive, customizable |

## Testing Strategy

- **Unit tests**: Core business logic
- **Integration tests**: API endpoints with test database
- **Property tests**: Hypothesis for reasoning engine
- **E2E tests**: Critical user flows (future)

## Monitoring (Production)

- Health check endpoints (/health, /ready, /live)
- Structured logging (JSON format)
- Database query monitoring
- Error tracking (Sentry or similar)
- Performance budgets tracked

## Migration Strategy

Alembic migrations follow this pattern:
1. Schema changes in models
2. Generate migration: `alembic revision --autogenerate`
3. Review and test migration
4. Apply: `alembic upgrade head`
5. Rollback if needed: `alembic downgrade -1`

## Further Reading

- [Database Schema](../decisionmirror_erd.md)
- [API Design](../api/)
- [Security Model](../security/)
- [Testing Strategy](../testing/)
