# SecureAI Gateway — Threat Model

- **Status:** P0 security baseline
- **Date:** 2026-10-21
- **Methodology:** STRIDE
- **Scope:** SecureAI Gateway application, AI integrations, privileged actions, and Azure infrastructure

## 1. Purpose

This threat model identifies security threats affecting SecureAI Gateway and defines the controls required to mitigate them.

The platform must protect enterprise identities, tenant data, AI workflows, privileged operations, and audit evidence.

Security decisions must be enforced by deterministic application controls rather than relying exclusively on AI-generated instructions.

## 2. System Overview

SecureAI Gateway provides governed access to AI capabilities through an ASP.NET Core API.

The planned architecture includes:

- Microsoft Entra ID authentication.
- Tenant-scoped authorization.
- Application-level policy enforcement.
- Azure OpenAI integration.
- Human approval workflows.
- Privileged action execution.
- Azure data services.
- Azure Service Bus messaging.
- Azure Key Vault.
- Azure Monitor and Application Insights.

These components represent the target architecture and may not yet be deployed.

## 3. Protected Assets

| Asset                        | Security requirement                          |
| ---------------------------- | --------------------------------------------- |
| User identities              | Authentication and authorization              |
| Access tokens                | Confidentiality and integrity                 |
| Tenant data                  | Isolation and access control                  |
| AI prompts                   | Data classification and controlled disclosure |
| AI responses                 | Validation and safe handling                  |
| Policy definitions           | Integrity and change control                  |
| Approval records             | Integrity and non-repudiation                 |
| Privileged credentials       | Least privilege and secret protection         |
| Audit records                | Integrity and retention                       |
| Infrastructure configuration | Controlled access and change management       |

## 4. Trust Boundaries

### TB-01: Client to API

External requests enter the platform through authenticated API endpoints.

### TB-02: API to Application

Validated identity and tenant context must be propagated to application services.

### TB-03: Application to AI Provider

Prompts and retrieved context leave the application boundary and are processed by an AI service.

### TB-04: Application to Privileged Action Gateway

AI recommendations and workflow commands must pass deterministic policy enforcement.

### TB-05: Application to Azure Resources

Infrastructure access must use managed identities, least privilege, and controlled networking.

### TB-06: Messaging and Background Processing

Asynchronous messages must preserve tenant context, authorization requirements, and idempotency guarantees.

## 5. STRIDE Threat Analysis

### 5.1 Spoofing

**Threat:** An attacker impersonates a legitimate user, service, or approver.

Potential attack paths:

- Stolen access tokens.
- Forged service identity.
- Incorrect token audience validation.
- Spoofed approval requests.

Required mitigations:

- Microsoft Entra ID authentication.
- Token issuer, audience, lifetime, and signature validation.
- Managed identities for service authentication.
- Approval identity verification.
- Short-lived credentials.
- Least-privilege role assignments.

### 5.2 Tampering

**Threat:** An attacker modifies requests, policies, approval records, or workflow state.

Potential attack paths:

- Manipulated API parameters.
- Unauthorized policy changes.
- Modified approval payloads.
- Message alteration.
- Corrupted audit evidence.

Required mitigations:

- Strict request validation.
- Role-restricted policy administration.
- Approval binding to action parameters.
- Integrity-protected persistence.
- Optimistic concurrency where appropriate.
- Immutable or tamper-evident audit storage where required.

### 5.3 Repudiation

**Threat:** A user or service denies performing an action.

Potential attack paths:

- Missing audit records.
- Shared privileged identities.
- Incomplete approval history.
- Missing correlation identifiers.

Required mitigations:

- Structured audit events.
- Actor and tenant identifiers.
- Correlation IDs.
- Approval decision records.
- Execution timestamps.
- Restricted audit modification permissions.
- Defined audit retention policies.

### 5.4 Information Disclosure

**Threat:** Sensitive information is exposed to unauthorized users, tenants, models, or logs.

Potential attack paths:

- Cross-tenant data retrieval.
- Sensitive prompts sent to unauthorized model endpoints.
- Secrets written to logs.
- Excessive model context.
- Incorrect storage permissions.

Required mitigations:

- Tenant-scoped queries.
- Data classification enforcement.
- Context minimization.
- Secret redaction.
- Managed identities.
- Encryption in transit and at rest.
- Restricted model endpoint access.
- Log data minimization.

### 5.5 Denial of Service

**Threat:** An attacker or malfunctioning workflow exhausts platform resources.

Potential attack paths:

- Excessive API requests.
- Large prompts.
- Unbounded retries.
- Queue flooding.
- Expensive model requests.

Required mitigations:

- Rate limiting.
- Request size limits.
- Token and cost budgets.
- Bounded retries.
- Circuit breakers.
- Queue backpressure.
- Resource quotas.
- Monitoring and alerting.

### 5.6 Elevation of Privilege

**Threat:** A user, service, or AI workflow gains permissions beyond its authorization.

Potential attack paths:

- Missing authorization checks.
- Overprivileged managed identities.
- AI-generated tool commands.
- Approval bypass.
- Cross-tenant authorization errors.

Required mitigations:

- Default-deny authorization.
- Explicit permission checks.
- Action allowlists.
- Risk-based approval requirements.
- Separation of duties.
- Execution-time policy revalidation.
- Least-privilege infrastructure identities.

## 6. AI-Specific Threats

### 6.1 Prompt Injection

An attacker embeds instructions in user input, retrieved documents, tool responses, or external content to influence AI behavior.

Controls:

- Treat retrieved content as untrusted.
- Separate system instructions from external content.
- Restrict model-accessible tools.
- Validate proposed actions independently.
- Apply deterministic policy checks.
- Require approval for high-risk operations.

### 6.2 Indirect Prompt Injection

Malicious instructions may be embedded in documents, web pages, search results, or external service responses.

Controls:

- Maintain source provenance.
- Restrict retrieval scope.
- Prevent retrieved text from becoming authorization policy.
- Validate all tool requests.
- Evaluate adversarial examples.

### 6.3 Sensitive Data Leakage

AI prompts or outputs may disclose confidential information.

Controls:

- Apply data classification rules.
- Minimize prompt context.
- Enforce tenant isolation.
- Restrict logging of prompts and responses.
- Validate output handling requirements.

### 6.4 Unsafe Tool Execution

A model may propose an unauthorized or harmful action.

Controls:

- Use an independent Action Gateway.
- Enforce explicit action allowlists.
- Validate action parameters.
- Require human approval where necessary.
- Revalidate authorization before execution.

### 6.5 Model Output Manipulation

A model may produce fabricated evidence, incorrect classifications, or misleading recommendations.

Controls:

- Treat outputs as untrusted.
- Require independent verification for consequential actions.
- Track model and prompt versions.
- Maintain evaluation datasets.
- Apply release gates.

## 7. Threat Register

| ID    | Threat                              | Severity | Primary control                                  |
| ----- | ----------------------------------- | -------- | ------------------------------------------------ |
| T-001 | Stolen access token                 | High     | Token validation and identity controls           |
| T-002 | Cross-tenant data access            | Critical | Tenant-scoped authorization                      |
| T-003 | Prompt injection                    | High     | Deterministic policy enforcement                 |
| T-004 | Approval bypass                     | Critical | Execution-time approval validation               |
| T-005 | Unauthorized tool execution         | Critical | Action allowlists and least privilege            |
| T-006 | Sensitive prompt leakage            | High     | Data classification and minimization             |
| T-007 | Audit tampering                     | High     | Restricted and integrity-protected audit storage |
| T-008 | Resource exhaustion                 | Medium   | Rate limits and quotas                           |
| T-009 | Replay of privileged command        | High     | Idempotency and replay protection                |
| T-010 | Compromised infrastructure identity | Critical | Managed identity and least privilege             |

Severity values are initial design assessments and must be reviewed against the deployed environment.

## 8. Security Testing Requirements

The implementation must include tests for:

- Invalid authentication tokens.
- Missing permissions.
- Cross-tenant access attempts.
- Prompt injection.
- Approval bypass.
- Expired approvals.
- Replay attacks.
- Unauthorized tool requests.
- Sensitive data leakage.
- Policy evaluation failures.

## 9. Residual Risk

Residual risks must be documented with:

- Threat identifier.
- Affected component.
- Existing controls.
- Remaining exposure.
- Risk owner.
- Treatment decision.
- Review date.

Critical residual risks must not be silently accepted.

## 10. Related Documents

- [Architecture Overview](../architecture/README.md)
- [Risk Policy](risk-policy.md)
- [Authorization Matrix](authorization-matrix.md)
- [ADR-0002: Deterministic Policy Enforcement](../adr/0002-deterministic-policy.md)
