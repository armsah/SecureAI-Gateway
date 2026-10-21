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

| Phase   | Focus                                                          | Status      |
| ------- | -------------------------------------------------------------- | ----------- |
| P0      | Architecture, security, and evaluation foundation              | In progress |
| P1      | ASP.NET Core application foundation                            | Planned     |
| P2      | Azure infrastructure with Terraform                            | Planned     |
| P3      | Microsoft Entra ID authentication                              | Planned     |
| P4–P8   | Data processing, AI integrations, and model evaluation         | Planned     |
| P9–P13  | Workflow orchestration, approvals, messaging, and verification | Planned     |
| P14–P15 | Offline evaluation and adversarial security testing            | Planned     |
| P16–P19 | Observability, cost controls, networking, and reliability      | Planned     |

## P0 Validation

### Requirements

Python 3.10 or later.

### Run Validation

From the repository root:

```powershell
python scripts/validate_p0.py
```

The validator checks:

- Required documentation files.
- Nonempty files.
- Local Markdown links.
- STRIDE threat categories.
- Architecture layer terminology.

A successful validation confirms basic documentation integrity. It does not establish production security readiness.

## Development Status

The project is currently establishing its architecture and governance baseline.

Application source code, Azure infrastructure, automated security controls, and deployment pipelines will be introduced in subsequent phases.

## License

See [LICENSE](LICENSE).
