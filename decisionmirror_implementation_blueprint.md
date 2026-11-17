# DecisionMirror — Implementation Blueprint

> Version: 1.0.0  
> Status: Implementation baseline  
> Based on: Reviews 1–10  
> Updated: 2026-11-14  
>
> This is a planning baseline, not proof of implementation. Recheck live Kiroween rules before submission.

## 1. Product definition

**DecisionMirror** is a **Decision Stress Testing Platform** for students and university students.

**Tagline:** Think Before You Commit.

**Core promise:** Turn a personal decision into an editable reasoning model, challenge its assumptions, and see how changes affect the reasoning behind it.

The product helps users think better; it does not decide for them.

### Primary demo scenario

A student receives an internship offer in another city. They are uncertain about accommodation costs, transportation, academic responsibilities, and whether the experience will improve career prospects.

The key demo moment is changing one assumption and showing which claims and consequences are affected, with an explanation of why.

## 2. Goals and non-goals

### Goals
1. Decompose natural-language decisions into editable reasoning elements.
2. Expose claims, assumptions, evidence, unknowns, counterarguments, alternatives, and consequences.
3. Let users correct AI-proposed content.
4. Evaluate claims through deterministic rules.
5. Stress-test assumptions against an immutable baseline.
6. Trace changes through dependencies and affected consequences.
7. Preserve provenance and explain status changes.

### Non-goals
- Choosing the best decision or predicting future outcomes.
- Treating internal statuses as objective truth.
- Replacing professional medical, legal, or financial advice.
- Medical diagnosis/treatment, legal strategy, investment/trading, emergencies, or direct physical-safety decisions.
- Bayesian probability estimates, unrestricted evidence retrieval, collaboration, or multi-criteria weighting in MVP.

## 3. Target users and use cases

**Primary:** students and university students.  
**Secondary:** freelancers, early-career professionals, small founders, independent professionals.

Initial use cases:
1. Accept an internship in another city.
2. Change university major.
3. Buy an expensive laptop for study or freelance work.

## 4. Product workflow

1. **Decision Input** — title, context, optional alternatives.
2. **Decomposition Review** — LLM proposes typed elements; user can accept, edit, reject, add, or delete.
3. **Challenge Center** — LLM proposes counterarguments; user reviews each one.
4. **Scenario Lab** — user changes assumptions to `HOLDS` or `FAILS`.
5. **Reasoning Map** — displays nodes, relationships, statuses, provenance, and paths.
6. **Decision Report** — traceable summary, support, counterarguments, assumptions, evidence gaps, scenario comparison, unresolved questions, and next actions.

Users must be able to complete the core workflow without opening the full graph. The graph is an exploration tool, not the landing screen.

## 5. MVP scope

### P0
- Decision input and validation.
- AI decomposition and user correction.
- Advocate, Skeptic, and Neutral analysis (lenses are not independent evidence).
- Counterargument review.
- Assumption stress testing.
- Typed decision graph.
- Evidence provenance.
- Traceable report with Markdown export.
- English and Indonesian UI/input.
- Safety, privacy, and data deletion.
- Fixture demo mode.

### Deferred
PDF export, collaborative review, Bayesian updating, multi-criteria weighting, arbitrary probability scores, advanced graph animation, reasoning history, and external evidence retrieval.

**Scope rule:** after kickoff, add no feature unless it fixes a P0 defect or a submission requirement.

## 6. Domain model

### Node types
`DECISION`, `ALTERNATIVE`, `CLAIM`, `ASSUMPTION`, `EVIDENCE`, `UNKNOWN`, `COUNTERARGUMENT`, `CONSEQUENCE`.

### Edge types
| Edge | Direction | Meaning |
|---|---|---|
| `SUPPORTS` | evidence/argument → claim | Source supports target claim |
| `ATTACKS` | counterargument → counterargument | Attack relation used by argumentation engine |
| `CHALLENGES` | counterargument → claim | Effective counterargument challenges claim |
| `DEPENDS_ON` | claim → prerequisite | Claim depends on assumption or another claim |
| `ADDRESSES` | unknown → claim/decision | Information gap; no status propagation in MVP |
| `LEADS_TO` | claim/alternative → consequence | Consequence tracing, not direct claim-status assignment |

### Provenance
`USER_PROVIDED`, `EXTERNAL_SOURCE`, `SYSTEM_INFERENCE`, `UNVERIFIED_ASSUMPTION`, `UNKNOWN_INFORMATION`.

Keep `origin`, `created_by`, and `updated_by` separate.

### State fields
- ASSUMPTION: `UNVERIFIED | HOLDS | FAILS`.
- COUNTERARGUMENT: `review_state = PROPOSED | USER_ACCEPTED | DISMISSED`; separate `grounded_label = IN | OUT | UNDECIDED`.
- CLAIM: `SUPPORTED | CONDITIONAL | CHALLENGED | UNSUPPORTED`.
- CONSEQUENCE: `NO_DETECTED_CHANGE | CONDITIONALLY_AT_RISK | CHALLENGED | AT_RISK`.

User acceptance makes a counterargument eligible for evaluation; it does not prove it true.

## 7. Deterministic reasoning rules

Status precedence:

`UNSUPPORTED > CHALLENGED > CONDITIONAL > SUPPORTED`

| Rule | Semantics |
|---|---|
| R1 | A claim depending on an assumption in `FAILS` becomes `UNSUPPORTED`. |
| R2 | A claim depending on an `UNSUPPORTED` claim becomes `UNSUPPORTED`; depending on `CHALLENGED` or `CONDITIONAL` makes it at most `CONDITIONAL`. |
| R3 | Grounded labelling applies to the accepted counterargument graph. An `IN` counterargument connected through `CHALLENGES` challenges its claim. |
| R4 | A claim depending on an `UNVERIFIED` assumption, or lacking at least one supporting evidence item from `USER_PROVIDED` or `EXTERNAL_SOURCE`, is at most `CONDITIONAL`. |
| R5 | Otherwise a claim may be `SUPPORTED`, subject to higher-priority rules. |
| R6 | `SYSTEM_INFERENCE` evidence must never independently upgrade a claim to `SUPPORTED`. |
| R7 | A claim attacked by a `PROPOSED` counterargument gets `challenged_by_unverified_counterargument`; proposal does not change claim status. |

### Argumentation
Grounded labelling applies to the counterargument attack graph, not all nodes:
- `IN`: all attackers are `OUT`, or no attackers exist.
- `OUT`: at least one attacker is `IN`.
- `UNDECIDED`: neither condition holds.

Only `USER_ACCEPTED` counterarguments are eligible. Implement a well-defined grounded labelling algorithm and test cycles.

### Propagation
- `SUPPORTS`: changes to supporting evidence/arguments trigger target claim reevaluation.
- `DEPENDS_ON`: store dependent claim → prerequisite; use reverse dependencies.
- `ATTACKS`: triggers argumentation reevaluation, not ordinary dependency propagation.
- `CHALLENGES`: review/label changes trigger target claim reevaluation.
- `LEADS_TO`: trace consequences; do not directly set claim status.
- `ADDRESSES`: no claim-status propagation semantics in MVP.

### Stress-test pipeline
1. Load immutable baseline version.
2. Apply all scenario changes together.
3. Recompute argumentation labels when needed.
4. Identify affected claims.
5. Evaluate affected claims in deterministic topological order with stable ID tie-break.
6. Trace affected consequences.
7. Produce status/impact diff and causal paths.

Reject `DEPENDS_ON` cycles at write time. Reject `LEADS_TO` cycles in MVP unless explicit semantics are designed. `ATTACKS` cycles are allowed.

Every scenario references one baseline version. Editing baseline creates a new version and marks scenarios based on the old version stale.

### Consequence impact
- Unchanged source claim → `NO_DETECTED_CHANGE`.
- Conditional source claim → `CONDITIONALLY_AT_RISK`.
- Challenged source claim → `CHALLENGED`.
- Unsupported source claim → `AT_RISK`.

For multiple upstream claims, derive impact from all relevant sources. Never label a consequence `SAFE` or imply certainty.

## 8. LLM boundary and reliability

The LLM is a stateless proposal and language-analysis service.

It may propose decomposition, counterarguments, and concise explanations. It must not write directly to the database, set final statuses, modify baseline, delete data, execute arbitrary tools, invent provenance, or return a best-decision verdict.

Controls:
- Structured output and Pydantic validation.
- Validate IDs, node/edge types, and endpoints.
- Bounded retries and timeouts.
- Token/cost limits and endpoint rate limits.
- Fixture mode.
- Separate untrusted user text from system instructions.
- Do not log decision text or prompts.

URL existence, source trustworthiness, and support for a claim are separate properties. MVP has no unrestricted LLM web search.

## 9. Technical architecture

**Style:** modular monolith.

Frontend: React, TypeScript strict, Vite, Tailwind, shadcn/ui, React Flow, TanStack Query, React Hook Form, Zod, lightweight i18n.

Backend: Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, Pytest, Hypothesis, NetworkX.

Data/infrastructure: PostgreSQL, Docker, Docker Compose, Caddy, GitHub Actions, external LLM provider adapter.

Do not introduce Kubernetes, microservices, Redis cluster, Kafka, Neo4j, pgvector, or local LLM inference in MVP without demonstrated need.

## 10. Repository structure

This is an engineering recommendation, not a folder layout mandated by the organizer:

```text
decisionmirror/
├── .kiro/
│   ├── specs/
│   ├── steering/
│   ├── hooks/
│   └── agents/
├── frontend/
├── backend/
├── infra/
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── security/
│   ├── testing/
│   └── kiro-usage/
├── scripts/
├── .github/
│   └── workflows/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── CONTRIBUTING.md
```

**Organizer compliance:** public GitHub repository, open-source license, and `.kiro/` at repository root. Do not ignore `.kiro/` or its subfolders. Recheck current rules. Folder names beyond explicit requirements are recommendations.

## 11. Initial API surface

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/decisions` | Create decision |
| GET | `/decisions/{id}` | Get workspace |
| POST | `/decisions/{id}/decompose` | Generate decomposition |
| PATCH | `/decisions/{id}/elements/{element_id}` | Edit element |
| POST | `/decisions/{id}/elements` | Add element |
| DELETE | `/decisions/{id}/elements/{element_id}` | Delete element |
| POST | `/decisions/{id}/analyze` | Generate adversarial analysis |
| PATCH | `/decisions/{id}/counterarguments/{cid}` | Accept/dismiss counterargument |
| POST | `/decisions/{id}/stress-test` | Create/evaluate scenario |
| GET | `/decisions/{id}/scenarios` | List scenarios |
| GET | `/decisions/{id}/graph` | Get graph |
| GET | `/decisions/{id}/report` | Get report |
| POST | `/decisions/{id}/feedback` | Submit feedback |
| DELETE | `/decisions/{id}` | Delete decision data |
| GET | `/health` | Liveness check |

Use anonymous session isolation, foreign keys, transactions, and optimistic concurrency (version or ETag). Finalize API contracts and error schemas before implementation.

## 12. Data model

Proposed tables:
`sessions`, `decisions`, `decision_versions`, `nodes`, `edges`, `scenarios`, `scenario_changes`, `evaluations`, `audit_events`.

See [`decisionmirror_erd.md`](decisionmirror_erd.md) for the conceptual ERD.

Unresolved:
1. Copy nodes/edges per version or immutable snapshots with version membership?
2. Persist immutable evaluation runs or recompute on read?
3. Exact deletion and backup-retention policy?
4. Anonymous session expiry duration?

## 13. Security and privacy

- Anonymous/private sessions with strict resource isolation.
- Session cookie `HttpOnly`, `Secure` in production, appropriate `SameSite`.
- CSRF protection for cookie-authenticated state-changing endpoints.
- Restrictive CORS allowlist.
- Rate-limit LLM endpoints and enforce input size limits.
- Never log decision text, prompts, or sensitive report content.
- Keep API keys server-side; do not expose PostgreSQL publicly.
- Support and test data deletion.
- Review provider retention/training policies before sending user content.
- Pseudonymization is not anonymization.

## 14. Deployment and operations

Recommended MVP: one VPS using Docker Compose with frontend static build, FastAPI, PostgreSQL, and Caddy.

Initial VPS test profile: 2 vCPU, 4 GB RAM, 40–60 GB SSD. This is a starting point for measurement, not a capacity guarantee.

Reliability:
- Persistent PostgreSQL volume and private network.
- Health/readiness checks and restart policies.
- Automated backup and tested restore.
- Fixture fallback if LLM provider is unavailable.
- No false success response if a database write fails.

Proposed performance budgets (must be measured):
- Workspace load: P95 < 2 s.
- Graph evaluation: P95 < 500 ms.
- Stress-test calculation: P95 < 500 ms.
- Health check: P95 < 200 ms.
- LLM request timeout: 30–45 s.

## 15. Testing strategy

P0:
- Claim status precedence.
- Dependency propagation.
- Baseline immutability.
- Scenario isolation.
- Graph validation.
- LLM output validation.
- Provenance preservation.
- Session isolation.
- Data deletion.

Test groups:
- Claim precedence T01–T12.
- Stress scenarios S01–S10.
- Graph integrity and provenance.
- LLM reliability and prompt injection SEC01–SEC15.
- API isolation and rate limiting.
- Hypothesis property-based invariants.

Quality gates: Ruff, mypy or Pyright, Pytest, Hypothesis, FastAPI TestClient, Alembic migration checks, TypeScript strict, frontend lint/build, Docker integration tests.

## 16. Implementation milestones

| Period | Milestone | Deliverables |
|---|---|---|
| Nov 14–16, 2026 | Foundation | Specs/steering, monorepo, Compose, PostgreSQL/migrations, basic CI |
| Nov 17–21 | Reasoning Engine | Graph validator, claim evaluator, argumentation, propagation, baseline/scenario isolation, core tests |
| Nov 22–25 | AI Integration | LLM adapter, decomposition, adversarial lenses, counterargument review, validation, fixture mode |
| Nov 26–29 | Product Experience | Workflow UI, graph, Scenario Lab, report, bilingual interface |
| Nov 30–Dec 2 | Hardening | Integration/security tests, deployment, 5–10 student pilot, UX fixes |
| Dec 3–4 | Submission Freeze | Demo video, README/Kiro write-up, repository audit, Devpost submission |

This schedule is aggressive for one developer. If the reasoning engine is not stable by Nov 21, do not add AI features; reduce visual polish or report complexity first.

## 17. Submission readiness

Verify the live organizer rules for public GitHub repo, open-source license, root `.kiro/` not ignored, functional app URL, public YouTube demo under three minutes, Kiro usage write-up, project originality/prior-work disclosure, app availability during judging, deadline/timezone, judging period, and eligibility.

Do not claim Kiro features that were not actually used. Keep evidence in `docs/kiro-usage/`.

## 18. Open decisions

- Select LLM provider based on current pricing, latency, structured output, and retention terms.
- Finalize SQL versioning strategy.
- Define session expiry and backup retention.
- Recheck live Kiroween rules.
- Confirm installed Kiro version's exact spec, steering, hook, and agent formats.
