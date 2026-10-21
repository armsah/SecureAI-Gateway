# SecureAI Gateway — Risk and Autonomy Policy

- **Status:** P0 security baseline
- **Date:** 2026-10-21
- **Scope:** AI requests, workflow decisions, and privileged operations

## 1. Purpose

This policy defines how SecureAI Gateway classifies operational risk and determines the level of automation permitted for an action.

AI-generated recommendations must not independently authorize privileged execution.

## 2. Risk Classification

SecureAI Gateway uses four risk levels.

| Risk level | Description                               | Example                                        |
| ---------- | ----------------------------------------- | ---------------------------------------------- |
| Low        | Read-only or low-impact operation         | Retrieve permitted non-sensitive metadata      |
| Medium     | Limited operational impact                | Update a non-production workflow configuration |
| High       | Significant business or security impact   | Modify production configuration                |
| Critical   | Potentially severe or irreversible impact | Delete critical production data                |

Risk classification must consider:

- Operation type.
- Resource sensitivity.
- Data classification.
- Production impact.
- Reversibility.
- Financial impact.
- Tenant scope.
- Privilege requirements.
- Potential blast radius.

## 3. Autonomy Levels

| Level | Name                   | Permitted behavior                                |
| ----- | ---------------------- | ------------------------------------------------- |
| A0    | Observe                | Read and summarize authorized information         |
| A1    | Recommend              | Generate recommendations without execution        |
| A2    | Controlled Execute     | Execute explicitly authorized low-risk operations |
| A3    | Approval-Gated Execute | Execute only after valid human approval           |

Autonomy level does not replace authorization.

Every operation must pass deterministic policy evaluation.

## 4. Risk-to-Autonomy Mapping

| Risk level | Maximum default autonomy | Approval requirement           |
| ---------- | ------------------------ | ------------------------------ |
| Low        | A2                       | Not normally required          |
| Medium     | A2                       | Required when policy specifies |
| High       | A3                       | Mandatory                      |
| Critical   | A1                       | Execution denied by default    |

Critical operations require a separately governed exceptional process before execution can be considered.

## 5. Default-Deny Policy

The platform must deny an action when:

- The actor is unauthenticated.
- Required permissions are missing.
- Tenant context is invalid.
- The action is not allowlisted.
- Required policy information is unavailable.
- Required approval is missing or expired.
- Action parameters differ from the approved request.
- Required audit guarantees are unavailable.

## 6. Human Approval Requirements

High-risk actions require explicit human approval.

An approval must include:

- Request identifier.
- Requester identity.
- Approver identity.
- Tenant identifier.
- Operation name.
- Target resource.
- Approved parameters or parameter digest.
- Decision.
- Reason.
- Timestamp.
- Expiration time.

Approvals must be validated again immediately before execution.

## 7. Separation of Duties

For high-risk operations:

- The requester must not approve their own request.
- The approver must have the required permission.
- The approval must apply to the same tenant.
- Approval must not be transferable to another action.
- Expired approvals must be rejected.

## 8. Execution Controls

The Privileged Action Gateway must enforce:

1. Verified actor identity.
2. Valid tenant context.
3. Action allowlist membership.
4. Deterministic policy approval.
5. Valid human approval where required.
6. Parameter validation.
7. Idempotency and replay protection.
8. Required audit evidence.
9. Least-privilege execution identity.

## 9. Failure Handling

| Failure                                   | Required behavior                                |
| ----------------------------------------- | ------------------------------------------------ |
| Policy evaluation unavailable             | Deny                                             |
| Approval service unavailable              | Do not execute                                   |
| Invalid approval                          | Deny                                             |
| Expired approval                          | Deny                                             |
| Audit evidence unavailable                | Block privileged execution                       |
| AI provider unavailable                   | Controlled error or bounded retry                |
| External execution dependency unavailable | Safe failure and bounded retry where appropriate |

## 10. Policy Change Management

Changes to risk classifications, autonomy limits, or approval requirements must be:

- Version-controlled.
- Reviewed by authorized owners.
- Tested before deployment.
- Auditable.
- Reversible where feasible.

## 11. Verification Requirements

Automated tests must verify:

- Default-deny behavior.
- Risk-to-autonomy restrictions.
- Mandatory approval for high-risk actions.
- Critical action denial.
- Approval expiration.
- Separation of duties.
- Tenant isolation.
- Replay protection.
- Execution-time policy revalidation.

## 12. Related Documents

- [Threat Model](threat-model.md)
- [Authorization Matrix](authorization-matrix.md)
- [ADR-0002: Deterministic Policy Enforcement](../adr/0002-deterministic-policy.md)
