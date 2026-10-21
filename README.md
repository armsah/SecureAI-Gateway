# SecureAI Gateway

Enterprise AI governance platform built with .NET and Microsoft Azure.

SecureAI Gateway is designed to provide secure, auditable, and policy-controlled access to AI capabilities.

## Project Objectives

The platform aims to support:

- Enterprise authentication and authorization.
- Tenant isolation.
- Deterministic security policy enforcement.
- Risk-based approval workflows.
- Controlled AI model integration.
- Privileged action governance.
- Auditable workflow execution.
- Security evaluation and operational monitoring.

## Architecture

The target implementation uses Clean Architecture:

- **Domain:** Business entities, invariants, and risk models.
- **Application:** Use cases, orchestration, and service interfaces.
- **Infrastructure:** Azure integrations and persistence adapters.
- **API:** ASP.NET Core endpoints and application composition.

Planned integrations include Microsoft Entra ID, Azure OpenAI, Azure Service Bus, Azure Key Vault, and Azure Monitor.

See the [Architecture Overview](docs/architecture/README.md).

## Project Documentation

### Requirements

- [Problem Statement](docs/problem-statement.md)
- [Data Classification](docs/data-classification.md)
- [Non-Functional Requirements](docs/non-functional-requirements.md)

### Architecture

- [Architecture Overview](docs/architecture/README.md)
- [Sequence Diagrams](docs/architecture/sequence.md)
- [ADR-0001: Platform Boundaries](docs/adr/0001-platform-boundaries.md)
- [ADR-0002: Deterministic Policy Enforcement](docs/adr/0002-deterministic-policy.md)

### Security

- [Threat Model](docs/security/threat-model.md)
- [Risk Policy](docs/security/risk-policy.md)
- [Authorization Matrix](docs/security/authorization-matrix.md)

### Evaluation

- [Evaluation Specification](docs/evaluation/specification.md)

## Implementation Roadmap

| Phase   | Focus                                                          | Status    |
| ------- | -------------------------------------------------------------- | --------- |
| P0      | Architecture, security, and evaluation foundation              | Completed |
| P1      | ASP.NET Core application foundation                            | Planned   |
| P2      | Azure infrastructure with Terraform                            | Planned   |
| P3      | Microsoft Entra ID authentication                              | Planned   |
| P4–P8   | Data processing, AI integrations, and model evaluation         | Planned   |
| P9–P13  | Workflow orchestration, approvals, messaging, and verification | Planned   |
| P14–P15 | Offline evaluation and adversarial security testing            | Planned   |
| P16–P19 | Observability, cost controls, networking, and reliability      | Planned   |

## P0 Deliverables

Phase P0 establishes the project's architecture, security, and evaluation baseline.

Completed deliverables include:

- Problem statement and project scope.
- Enterprise data classification requirements.
- Non-functional requirements.
- C4 architecture documentation.
- Request and approval sequence diagrams.
- Architecture Decision Records (ADRs).
- STRIDE threat model.
- Risk and autonomy policy.
- Role-based authorization matrix.
- Evaluation specification and release gates.
- Automated documentation validation script.

These deliverables define the intended system behavior. They do not represent a deployed or production-certified implementation.

## P0 Validation

### Requirements

- Python 3.10 or later.
- Git.
- A local clone of the repository.

### Run Validation

From the repository root:

```powershell
python scripts/validate_p0.py
```

The validator checks:

- Required documentation files exist.
- Required files are not empty.
- Local Markdown links point to existing files.
- The threat model includes all six STRIDE categories.
- Architecture documentation identifies the Domain, Application, Infrastructure, and API layers.

### Expected Output

```text
============================================================
SecureAI Gateway — P0 Validation
============================================================

VALIDATION PASSED

Validated 12 required files.
Markdown links: PASS
Security documentation: PASS
Architecture documentation: PASS

P0 documentation integrity verified.
```

A successful validation confirms basic documentation integrity. It does not establish production security readiness.

## P1 — ASP.NET Core Application Foundation

The next implementation phase will establish the .NET solution and Clean Architecture project structure.

### Planned Components

```text
src/
├── SecureAI.Gateway.Domain/
├── SecureAI.Gateway.Application/
├── SecureAI.Gateway.Infrastructure/
└── SecureAI.Gateway.Api/

tests/
├── SecureAI.Gateway.Domain.Tests/
├── SecureAI.Gateway.Application.Tests/
└── SecureAI.Gateway.Api.Tests/
```

### P1 Acceptance Criteria

P1 will be considered complete when:

1. The .NET solution is created.
2. All four application projects are configured.
3. Project dependencies follow the approved architecture.
4. The ASP.NET Core API starts successfully.
5. A basic health endpoint is available.
6. Unit and integration test projects are configured.
7. The solution builds successfully.
8. Automated tests pass.
9. P1 changes are committed and pushed to GitHub.

## Security Principles

SecureAI Gateway follows these foundational security principles:

- **Zero implicit trust:** Every protected operation requires authorization.
- **Default deny:** Missing permissions or unavailable security controls must not result in access.
- **Least privilege:** Users and services receive only the permissions necessary for their responsibilities.
- **Tenant isolation:** Data and operations are restricted to authorized tenant boundaries.
- **Deterministic policy enforcement:** AI model output cannot grant permissions or override security policies.
- **Human oversight:** High-risk operations require explicit approval.
- **Auditability:** Security-sensitive decisions and privileged actions require appropriate audit evidence.
- **Fail-closed execution:** Privileged operations must not bypass required controls during failures.

For additional details, see the [Security Documentation](docs/security/threat-model.md).

## Development Status

**Current phase:** P1 — ASP.NET Core Application Foundation (next planned phase).

**Completed:** P0 — Architecture, security, and evaluation foundation.

The repository currently contains the P0 documentation baseline and its validation script.

Application source code, Azure infrastructure, authentication integrations, automated security controls, and deployment pipelines will be introduced incrementally in subsequent phases.

## License

See [LICENSE](LICENSE).
