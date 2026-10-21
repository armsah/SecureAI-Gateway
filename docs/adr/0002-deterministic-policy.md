# ADR-0002: Deterministic Policy Enforcement

- **Status:** Accepted for P0 architecture baseline
- **Date:** 2026-10-21
- **Decision owners:** SecureAI Gateway security architecture team
- **Scope:** Authorization, AI governance, and privileged operations

## 1. Context

SecureAI Gateway integrates AI models into enterprise workflows.

AI model responses are probabilistic and may contain incorrect, manipulated, or unauthorized instructions.

Prompt injection and malicious content can attempt to influence application behavior.

Therefore, AI model output must never be treated as an authorization decision or as sufficient permission to execute privileged operations.

## 2. Decision

SecureAI Gateway will enforce security policies using deterministic application logic.

AI models may generate recommendations, classifications, summaries, and proposed actions.

However, all privileged operations must pass independent policy checks before execution.

## 3. Core Principles

### 3.1 AI Output Is Untrusted

Model-generated content is treated as untrusted input.

It cannot:

- Grant permissions.
- Modify authorization rules.
- Override tenant boundaries.
- Approve privileged actions.
- Disable audit logging.
- Bypass risk classification.
- Change execution allowlists.

### 3.2 Default Deny

Actions are denied unless an explicit policy permits them.

Missing policy data, invalid identity context, or unavailable authorization dependencies must not result in implicit permission.

### 3.3 Separation of Decision and Execution

The platform separates:

1. AI-generated recommendations.
2. Deterministic policy decisions.
3. Human approval decisions.
4. Privileged action execution.

Each stage must have explicit inputs, outputs, and audit evidence.

### 3.4 Least Privilege

Execution identities must receive only the permissions required for authorized operations.

### 3.5 Tenant Isolation

All authorization decisions must include verified tenant context.

A user or workflow must not access another tenant's resources without an explicitly authorized cross-tenant mechanism.

## 4. Policy Inputs

A policy evaluation may consider:

- Authenticated user identity.
- Tenant identifier.
- Assigned roles.
- Requested operation.
- Target resource.
- Resource ownership.
- Data classification.
- Risk classification.
- Approval requirements.
- Current approval status.
- Environment restrictions.
- Request expiration.
- Relevant security configuration.

The policy evaluator must use trusted, validated inputs.

## 5. Policy Outcomes

The policy evaluator must return one of the following decisions:

| Decision        | Meaning                                                    |
| --------------- | ---------------------------------------------------------- |
| Allow           | Operation may proceed subject to execution-time validation |
| Deny            | Operation must not proceed                                 |
| RequireApproval | Human approval is required before execution                |

A decision must include a machine-readable reason code.

## 6. Risk-Based Controls

| Risk level | Expected control                                                          |
| ---------- | ------------------------------------------------------------------------- |
| Low        | Deterministic authorization                                               |
| Medium     | Authorization and additional policy restrictions                          |
| High       | Explicit human approval                                                   |
| Critical   | Deny by default unless a separately approved exceptional procedure exists |

Risk classification must not be determined solely by an AI model.

## 7. Privileged Execution Requirements

Before executing a privileged action, the Action Gateway must:

1. Validate the authenticated execution context.
2. Verify tenant scope.
3. Validate the requested action against an allowlist.
4. Reevaluate deterministic policy.
5. Verify required approvals.
6. Confirm that approvals are valid and unexpired.
7. Validate operation parameters.
8. Enforce idempotency and replay protection.
9. Record the execution decision.
10. Execute only through an authorized infrastructure adapter.

Approvals must be bound to the intended action, resource, tenant, and relevant parameters.

A change to the approved action must invalidate the approval or require reevaluation.

## 8. Separation of Duties

For high-risk operations, the requester must not approve their own request.

Approvers must possess the required permission for the operation and tenant.

Approval decisions must be recorded with:

- Approver identity.
- Tenant identifier.
- Requested action.
- Decision.
- Timestamp.
- Reason.
- Approval expiration.

## 9. Failure Handling

### Policy Service Unavailable

Deny the operation or keep it pending.

### Approval Service Unavailable

Do not execute an operation requiring approval.

### Invalid or Expired Approval

Deny execution.

### Audit Evidence Unavailable

Do not execute privileged operations that require durable audit evidence.

### AI Model Unavailable

Return a controlled error or apply a bounded retry policy.

AI model availability must not determine whether security controls are enforced.

## 10. Audit Requirements

Policy decisions must produce structured evidence containing:

- Correlation identifier.
- Tenant identifier.
- Actor identifier.
- Requested operation.
- Resource identifier.
- Policy version.
- Decision.
- Reason code.
- Timestamp.

Sensitive data must not be unnecessarily copied into audit records.

## 11. Alternatives Considered

### Alternative A: AI-Based Authorization

Rejected because probabilistic model output cannot provide reliable authorization guarantees.

### Alternative B: Prompt-Only Security Controls

Rejected because prompts cannot replace deterministic security enforcement.

### Alternative C: Execute First, Audit Later

Rejected because unauthorized operations could occur before detection.

## 12. Consequences

### Positive

- Predictable authorization behavior.
- Stronger prompt-injection resistance.
- Explicit governance boundaries.
- Auditable security decisions.
- Improved testability.

### Negative

- Additional policy implementation.
- More approval workflow complexity.
- Increased latency for high-risk operations.

## 13. Verification

The implementation must include automated tests proving that:

- Unauthorized actions are denied.
- Missing policies result in denial.
- AI-generated instructions cannot grant permissions.
- Expired approvals are rejected.
- Cross-tenant access is denied.
- High-risk actions require valid approvals.
- Self-approval is prohibited where separation of duties applies.
- Privileged execution is blocked when required audit guarantees are unavailable.

## 14. Related Documents

- [Architecture Overview](../architecture/README.md)
- [ADR-0001: Platform Boundaries](0001-platform-boundaries.md)
- [Risk Policy](../security/risk-policy.md)
- [Authorization Matrix](../security/authorization-matrix.md)
