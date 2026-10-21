# SecureAI Gateway — Sequence Diagrams

## 1. Standard AI Request Lifecycle

```mermaid
sequenceDiagram
    autonumber

    actor User
    participant API
    participant Auth as Authorization Service
    participant Policy as Policy Evaluator
    participant Model as Azure OpenAI
    participant Audit as Audit Service

    User->>API: Submit AI request
    API->>Auth: Validate identity and permissions
    Auth-->>API: Authorization decision

    alt Unauthorized
        API-->>User: 403 Forbidden
    else Authorized
        API->>Policy: Evaluate request policy
        Policy-->>API: Allow / Deny

        alt Policy denied
            API->>Audit: Record denial
            API-->>User: Request denied
        else Policy allowed
            API->>Model: Submit governed prompt
            Model-->>API: AI response
            API->>Audit: Record request outcome
            API-->>User: Return response
        end
    end
```

## 2. Privileged Action Approval Workflow

```mermaid
sequenceDiagram
    autonumber

    actor User
    actor Approver
    participant API
    participant Risk as Risk Evaluator
    participant Policy as Policy Evaluator
    participant Approval as Approval Service
    participant Action as Action Gateway
    participant Audit

    User->>API: Request privileged action
    API->>Risk: Classify risk
    Risk-->>API: Risk level

    API->>Policy: Evaluate action policy
    Policy-->>API: Policy decision

    alt Denied
        API->>Audit: Record denial
        API-->>User: Action denied
    else Approval required
        API->>Approval: Create approval request
        Approval-->>Approver: Request review
        Approver->>Approval: Approve or reject

        alt Rejected
            Approval->>Audit: Record rejection
            API-->>User: Action rejected
        else Approved
            Approval->>Action: Submit authorized action
            Action->>Policy: Revalidate policy and approval
            Policy-->>Action: Execution decision

            alt Revalidation denied
                Action->>Audit: Record execution denial
                API-->>User: Action denied
            else Revalidation allowed
                Action->>Action: Execute allowlisted operation
                Action->>Audit: Record execution evidence
                API-->>User: Action result
            end
        end
    else Allowed without approval
        API->>Action: Submit authorized action
        Action->>Policy: Revalidate policy
        Policy-->>Action: Execution decision

        alt Revalidation denied
            Action->>Audit: Record execution denial
            API-->>User: Action denied
        else Revalidation allowed
            Action->>Action: Execute allowlisted operation
            Action->>Audit: Record execution evidence
            API-->>User: Action result
        end
    end
```

## 3. Failure and Retry Handling

```mermaid
sequenceDiagram
    autonumber

    participant Worker
    participant Queue as Azure Service Bus
    participant Service as Application Service
    participant Dependency as External Dependency
    participant Audit

    Worker->>Queue: Receive message
    Queue-->>Worker: Deliver message

    Worker->>Service: Process command
    Service->>Dependency: Execute operation

    alt Successful
        Dependency-->>Service: Success
        Service->>Audit: Record completion
        Worker->>Queue: Complete message
    else Transient failure
        Dependency-->>Service: Retryable error
        Service->>Audit: Record attempt
        Worker->>Queue: Abandon or schedule retry
    else Permanent failure
        Dependency-->>Service: Non-retryable error
        Service->>Audit: Record failure
        Worker->>Queue: Dead-letter message
    end
```

## 4. Security Requirements

The implementation must enforce:

- Authentication before protected API access.
- Tenant-scoped authorization.
- Deterministic policy checks.
- Explicit approval for actions requiring human review.
- Policy revalidation immediately before privileged execution.
- Auditable approval and execution decisions.
- Idempotent message handling.
- Bounded retries and dead-letter processing.
- Fail-closed behavior for security-critical dependencies.

## 5. Implementation Notes

These diagrams describe intended application behavior.

The implementation will be introduced incrementally in later phases, with automated tests verifying the security-critical paths.
