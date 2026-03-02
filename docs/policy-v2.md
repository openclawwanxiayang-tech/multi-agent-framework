# Policy Engine v2

> Expanded policy constraints beyond MVP.

## New Capabilities

### File/Path Restrictions

```json
{
  "policy": {
    "path_restrictions": {
      "allowed": ["artifacts/**", "docs/**", "config/**"],
      "denied": ["**/secrets/**", "**/.env", "**/credentials/**"]
    }
  }
}
```

### Branch Rules

```json
{
  "policy": {
    "branch_rules": {
      "require_pr": true,
      "allowed_direct_push": ["main"],
      "require_reviews": ["master", "main"]
    }
  }
}
```

### Rate Limits

```json
{
  "policy": {
    "rate_limits": {
      "tool_calls_per_minute": 60,
      "api_requests_per_hour": 1000
    }
  }
}
```

## Approval Workflow

### Request Approval

```json
{
  "$version": "1.0.0",
  "type": "APPROVAL_REQUEST",
  "task_id": "T-2026-MVP-001",
  "risk_tier": "high",
  "requester": "agent-dev-1",
  "action": "deploy to production",
  "expires_at": "2026-03-02T18:00:00Z"
}
```

### Approval Response

```json
{
  "$version": "1.0.0",
  "type": "APPROVAL_RESPONSE",
  "request_id": "req-001",
  "decision": "approved|denied",
  "approver": "human-admin",
  "reason": "looks good",
  "responded_at": "2026-03-02T12:15:00Z"
}
```
