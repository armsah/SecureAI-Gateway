# SecureAI Gateway — Authorization Matrix

- **Status:** P0 security baseline
- **Date:** 2026-10-21
- **Scope:** Application roles and protected operations

## 1. Purpose

This document defines role-based permissions for SecureAI Gateway.

Authorization must be enforced by application services using verified identity and tenant context.

Role assignments alone do not override tenant boundaries, risk policies, or approval requirements.

## 2. Application Roles

| Role          | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| Viewer        | Read authorized information and view permitted outcomes      |
| Operator      | Submit AI requests and execute permitted low-risk operations |
| Approver      | Review and decide approval requests within assigned scope    |
| SecurityAdmin | Manage security policy and review security evidence          |
| PlatformAdmin | Manage platform configuration and operational settings       |
| Auditor       | Review authorized audit evidence without modifying it        |

Roles must be assigned through an approved identity-management process.

## 3. Permission Matrix

Legend:

- **Y:** Permitted, subject to policy and tenant scope.
- **N:** Not permitted.
- **A:** Permitted only with additional approval or governance controls.

| Operation                     | Viewer | Operator | Approver | SecurityAdmin | PlatformAdmin | Auditor |
| ----------------------------- | ------ | -------- | -------- | ------------- | ------------- | ------- |
| Read permitted data           | Y      | Y        | Y        | Y             | Y             | Y       |
| Submit AI request             | N      | Y        | N        | N             | N             | N       |
| View own AI request           | Y      | Y        | Y        | Y             | Y             | Y       |
| Execute low-risk action       | N      | Y        | N        | N             | N             | N       |
| Request high-risk action      | N      | Y        | N        | N             | N             | N       |
| Approve high-risk action      | N      | N        | Y        | N             | N             | N       |
| View approval history         | N      | Y        | Y        | Y             | Y             | Y       |
| Manage security policy        | N      | N        | N        | A             | N             | N       |
| Manage platform configuration | N      | N        | N        | N             | A             | N       |
| View security audit records   | N      | N        | N        | Y             | N             | Y       |
| Modify audit records          | N      | N        | N        | N             | N             | N       |

This matrix is the default baseline. Production permissions must be narrowed further using resource-level and tenant-level policies.

## 4. Authorization Rules

### Rule AUTH-001: Authentication Required

Protected operations require an authenticated principal.

### Rule AUTH-002: Tenant Isolation

Access is restricted to resources belonging to the verified tenant context.

### Rule AUTH-003: Default Deny

An operation without an explicit permission grant must be denied.

### Rule AUTH-004: Least Privilege

Users and services receive only the permissions required for their responsibilities.

### Rule AUTH-005: Risk Policy Enforcement

Role permission does not bypass risk classification or approval requirements.

### Rule AUTH-006: Separation of Duties

A requester must not approve their own high-risk operation.

### Rule AUTH-007: Execution-Time Revalidation

Privileged actions require policy and approval revalidation immediately before execution.

### Rule AUTH-008: Audit Integrity

No application role may directly modify or delete finalized audit records.

## 5. Authorization Context

Each protected request must include trusted values for:

- Actor identifier.
- Tenant identifier.
- Assigned roles.
- Requested operation.
- Target resource.
- Relevant resource attributes.
- Correlation identifier.

Client-supplied tenant identifiers must not be trusted without validation against authenticated identity and authorization context.

## 6. Approval Authorization

Approval decisions require:

- The Approver role.
- Permission for the target tenant.
- Permission for the operation category.
- A valid pending approval request.
- Separation of duties.
- An unexpired approval window.

Approval decisions must be recorded for audit purposes.

## 7. Service-to-Service Authorization

Service identities must:

- Use managed identities where supported.
- Have explicit resource permissions.
- Avoid shared administrative credentials.
- Use least-privilege access.
- Be monitored for unauthorized operations.

## 8. Testing Requirements

Automated authorization tests must cover:

- Missing authentication.
- Missing role.
- Incorrect tenant.
- Unauthorized resource.
- Approval bypass.
- Self-approval.
- Expired approval.
- Unauthorized policy modification.
- Audit record modification attempts.

## 9. Related Documents

- [Threat Model](threat-model.md)
- [Risk Policy](risk-policy.md)
- [Architecture Overview](../architecture/README.md)
- [ADR-0002: Deterministic Policy Enforcement](../adr/0002-deterministic-policy.md)
