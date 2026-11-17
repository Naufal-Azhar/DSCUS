# Next Steps - DecisionMirror Development

This guide helps you continue development from where the foundation phase left off.

---

## 🎯 Current State

**Foundation Phase Complete ✅**
- Full-stack structure ready
- Database models implemented
- Basic API endpoints working
- Frontend skeleton in place
- Docker environment configured

**Next Phase: Reasoning Engine (Nov 17-21)**

---

## 🚀 Getting Started

### 1. Verify Setup

```bash
# Ensure Docker Desktop is running

# Start services
docker-compose up -d

# Check health
curl http://localhost:8000/health

# Access frontend
# Open browser: http://localhost:5173
```

### 2. Verify Database

```bash
# Generate initial migration
docker-compose exec api alembic revision --autogenerate -m "Initial schema"

# Apply migration
docker-compose exec api alembic upgrade head

# Verify tables
docker-compose exec db psql -U decisionmirror -d decisionmirror -c "\dt"
```

You should see 8 tables: sessions, decisions, decision_versions, nodes, edges, scenarios, scenario_changes, evaluations, audit_events

---

## 📋 Development Roadmap

### Phase 1: Reasoning Engine Core (Priority 1)

#### 1.1 Graph Validator (`backend/app/services/graph_validator.py`)

Create service to validate graph structure:

```python
# Implement:
- validate_node_type(node_type: str) -> bool
- validate_edge_type(edge: Edge, source: Node, target: Node) -> bool
- detect_cycles(graph: nx.DiGraph, edge_type: str) -> bool
- validate_graph_structure(version_id: UUID) -> ValidationResult
```

**Tests**: `tests/services/test_graph_validator.py`

#### 1.2 Claim Evaluator (`backend/app/services/claim_evaluator.py`)

Implement reasoning rules R1-R7:

```python
# Implement:
- evaluate_claim_status(node: Node, graph: nx.DiGraph) -> ClaimStatus
- apply_assumption_rules(node: Node, dependencies: List[Node]) -> ClaimStatus
- apply_support_rules(node: Node, evidence: List[Node]) -> ClaimStatus
- apply_precedence_rules(statuses: List[ClaimStatus]) -> ClaimStatus
```

**Status Precedence**: UNSUPPORTED > CHALLENGED > CONDITIONAL > SUPPORTED

**Tests**: `tests/services/test_claim_evaluator.py` (T01-T12 from spec)

#### 1.3 Argumentation Engine (`backend/app/services/argumentation_engine.py`)

Implement grounded labelling:

```python
# Implement:
- build_attack_graph(counterarguments: List[Node]) -> nx.DiGraph
- compute_grounded_labelling(attack_graph: nx.DiGraph) -> Dict[UUID, Label]
- apply_challenges(labelling: Dict, claims: List[Node]) -> None
```

**Labels**: IN, OUT, UNDECIDED

**Tests**: `tests/services/test_argumentation_engine.py`

#### 1.4 Scenario Evaluator (`backend/app/services/scenario_evaluator.py`)

Implement stress testing:

```python
# Implement:
- load_baseline_version(version_id: UUID) -> GraphState
- apply_scenario_changes(baseline: GraphState, changes: List[ScenarioChange]) -> GraphState
- identify_affected_nodes(changes: List[ScenarioChange], graph: nx.DiGraph) -> Set[UUID]
- evaluate_scenario(scenario_id: UUID) -> EvaluationResult
- compute_impact_diff(baseline: GraphState, scenario: GraphState) -> ImpactReport
```

**Tests**: `tests/services/test_scenario_evaluator.py` (S01-S10 from spec)

---

### Phase 2: API Endpoints (Priority 2)

Implement remaining endpoints in `backend/app/api/v1/`:

#### 2.1 Decomposition (`decomposition.py`)

```python
POST /decisions/{id}/decompose
- Call LLM adapter for decomposition
- Validate proposed structure
- Return structured proposal
- User reviews before committing
```

#### 2.2 Graph Editing (`elements.py`)

```python
POST /decisions/{id}/elements
- Add node or edge
- Validate types and relationships
- Create new version if needed
- Trigger evaluation

PATCH /decisions/{id}/elements/{element_id}
- Update node content
- Validate changes
- Create new version
- Trigger evaluation

DELETE /decisions/{id}/elements/{element_id}
- Soft-delete node/edge
- Create new version
- Recalculate affected claims
```

#### 2.3 Scenarios (`scenarios.py`)

```python
POST /decisions/{id}/stress-test
- Create scenario from baseline
- Apply changes
- Evaluate impact
- Return diff report

GET /decisions/{id}/scenarios
- List all scenarios
- Include stale status

GET /decisions/{id}/scenarios/{scenario_id}
- Get scenario details
- Include evaluation results
```

#### 2.4 Analysis (`analysis.py`)

```python
POST /decisions/{id}/analyze
- Generate counterarguments
- Use Advocate/Skeptic/Neutral perspectives
- Return proposals for user review

PATCH /decisions/{id}/counterarguments/{cid}
- Accept or dismiss counterargument
- Update review_state
- Trigger argumentation evaluation
```

#### 2.5 Report (`report.py`)

```python
GET /decisions/{id}/report
- Generate decision report
- Include supporting evidence
- List counterarguments
- Show assumption states
- Evidence gaps
- Scenario comparisons
- Export as Markdown
```

---

### Phase 3: LLM Integration (Priority 3)

#### 3.1 LLM Adapter (`backend/app/services/llm/adapter.py`)

```python
class LLMAdapter:
    def decompose_decision(self, context: str) -> DecompositionProposal
    def generate_counterarguments(self, claims: List[Node]) -> List[Counterargument]
    def explain_status_change(self, change: StatusChange) -> str
```

#### 3.2 Provider Implementations

- `backend/app/services/llm/openai_provider.py` - OpenAI integration
- `backend/app/services/llm/fixture_provider.py` - Fixture mode (no API)

#### 3.3 Prompts

Create prompt templates in `backend/app/services/llm/prompts/`:
- `decomposition.txt` - Decision decomposition
- `advocate.txt` - Advocate perspective
- `skeptic.txt` - Skeptic perspective
- `neutral.txt` - Neutral perspective

---

### Phase 4: Frontend Components (Priority 4)

#### 4.1 Graph Visualization (`frontend/src/components/ReasoningGraph.tsx`)

Use React Flow:
```tsx
- Display nodes with type-specific styling
- Show edges with relationship labels
- Highlight affected nodes in scenarios
- Support zoom, pan, selection
- Show status colors (supported/conditional/challenged/unsupported)
```

#### 4.2 Node Editor (`frontend/src/components/NodeEditor.tsx`)

```tsx
- Edit node content
- Change assumption state
- Review counterarguments
- Add/remove evidence
```

#### 4.3 Scenario Lab (`frontend/src/components/ScenarioLab.tsx`)

```tsx
- Create new scenario
- Toggle assumption states
- View impact diff
- Show affected claims
- Highlight propagation paths
```

#### 4.4 Counterargument Review (`frontend/src/components/CounterargumentReview.tsx`)

```tsx
- Display proposed counterarguments
- Accept/Dismiss buttons
- Show grounded label
- Explain impact on claims
```

#### 4.5 Decision Report (`frontend/src/components/DecisionReport.tsx`)

```tsx
- Render structured report
- Export to Markdown
- Show evidence gaps
- List assumptions
- Scenario comparison table
```

---

## 🧪 Testing Strategy

### Unit Tests
```bash
cd backend
pytest tests/services/test_claim_evaluator.py -v
```

Test cases from spec:
- T01-T12: Claim evaluation rules
- S01-S10: Scenario evaluation
- SEC01-SEC15: Security and prompt injection

### Integration Tests
```bash
pytest tests/integration/test_api.py -v
```

### Property-Based Tests
```bash
pytest tests/property/test_reasoning_invariants.py -v
```

Use Hypothesis to test:
- Graph properties always hold
- Status precedence is never violated
- Baseline immutability

---

## 📚 Resources

### Documentation References
- [Implementation Blueprint](decisionmirror_implementation_blueprint.md) - Full spec
- [ERD](decisionmirror_erd.md) - Database design
- [Project Spec](decisionmirror_project_spec.json) - Machine-readable spec

### Code Examples

**NetworkX Graph Operations**:
```python
import networkx as nx

# Build graph
G = nx.DiGraph()
G.add_node(node_id, **node_data)
G.add_edge(source_id, target_id, edge_type="DEPENDS_ON")

# Detect cycles
try:
    cycles = list(nx.simple_cycles(G))
except nx.NetworkXNoCycle:
    pass

# Topological sort
sorted_nodes = list(nx.topological_sort(G))

# Reverse dependencies
reverse_graph = G.reverse()
dependents = list(reverse_graph.successors(node_id))
```

**React Flow Graph**:
```tsx
import ReactFlow, { Node, Edge } from 'reactflow'

const nodes: Node[] = [
  { id: '1', type: 'claim', data: { label: 'Claim' }, position: { x: 0, y: 0 } }
]

const edges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', label: 'SUPPORTS' }
]

<ReactFlow nodes={nodes} edges={edges} />
```

---

## 🎯 Milestones

| Week | Focus | Deliverables |
|------|-------|-------------|
| Nov 17-21 | Reasoning Engine | Graph validator, evaluators, tests |
| Nov 22-25 | AI Integration | LLM adapter, prompts, fixture mode |
| Nov 26-29 | Frontend | Graph UI, scenarios, reports |
| Nov 30-Dec 2 | Hardening | Tests, deployment, pilot |
| Dec 3-4 | Submission | Demo video, docs, deploy |

---

## 🐛 Known Issues to Address

1. **Import fixes needed**:
   - Some models have circular import issues
   - May need to adjust import order or use TYPE_CHECKING

2. **Migration generation**:
   - First migration needs to be generated
   - Test up/down migrations

3. **Session management**:
   - Currently using temp UUID for session_id
   - Need to implement proper session middleware

4. **CORS in production**:
   - Update CORS origins for production URL

---

## 💡 Development Tips

### Hot Reload
Both frontend and backend support hot reload:
- Frontend: Vite watches files automatically
- Backend: Uvicorn `--reload` flag enabled

### Database Changes
```bash
# After modifying models:
docker-compose exec api alembic revision --autogenerate -m "description"
docker-compose exec api alembic upgrade head
```

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f frontend
```

### Running Tests
```bash
# Backend
docker-compose exec api pytest

# With coverage
docker-compose exec api pytest --cov=app

# Frontend (after npm install in container)
docker-compose exec frontend npm run test
```

### API Documentation
FastAPI auto-generates docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🎓 Learning Resources

### FastAPI
- [Official Docs](https://fastapi.tiangolo.com/)
- [Async SQL](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

### React Flow
- [Official Docs](https://reactflow.dev/)
- [Examples](https://reactflow.dev/examples)

### NetworkX
- [Official Docs](https://networkx.org/documentation/stable/)
- [Algorithms](https://networkx.org/documentation/stable/reference/algorithms/)

### Grounded Semantics
- [Argumentation Theory](https://en.wikipedia.org/wiki/Argumentation_framework)
- [Grounded Labelling](https://www.sciencedirect.com/topics/computer-science/grounded-semantics)

---

## 🤝 Need Help?

1. Check `docs/` for detailed documentation
2. Review `IMPLEMENTATION_SUMMARY.md` for what's built
3. Read `docs/PROJECT_STATUS.md` for current progress
4. Open an issue if stuck
5. Refer to original specs in root directory

---

## ✨ Success Criteria

MVP is complete when:
- [x] Foundation structure ✅
- [ ] User can input a decision
- [ ] AI decomposes decision into graph
- [ ] User can edit graph elements
- [ ] System evaluates claims deterministically
- [ ] User can create stress-test scenarios
- [ ] Changes propagate through graph
- [ ] Impact report shows affected elements
- [ ] Report can be exported as Markdown
- [ ] Tests pass with >80% coverage
- [ ] Application runs in Docker
- [ ] Documentation is complete

---

**Let's build the reasoning engine! 🚀**

For questions or clarifications, see:
- `decisionmirror_implementation_blueprint.md` - Full implementation guide
- `docs/architecture/OVERVIEW.md` - Architecture details
- `docs/GETTING_STARTED.md` - Setup instructions

**Built with Kiro for Kiroween 2026** 🎃
