# Governance & Policy Enforcement

> Version: 1.0.0  
> Last Updated: 2026-02-23

---

## Overview

This document defines where and how policy is enforced in the v2.2 MVP.

---

## Enforcement Points

### Primary: Orchestrator Wrapper

All tool calls go through the orchestrator which enforces policy **before** execution.

```python
class PolicyEnforcer:
    def __init__(self, policy_config):
        self.policy = policy_config
    
    def check(self, agent, tool, args, task):
        # 1. Check role permissions
        if not self.can_use(agent.role, tool):
            return PolicyResult.denied(f"Role {agent.role} cannot use {tool}")
        
        # 2. Check risk tier
        if task.risk_tier == "critical" and tool in CRITICAL_TOOLS:
            return PolicyResult.require_approval(agent, tool)
        
        # 3. Check budgets
        if agent.budget_used >= agent.budget_max:
            return PolicyResult.denied("Budget exceeded")
        
        # 4. Log attempt
        self.log(agent, tool, args)
        
        return PolicyResult.allowed()
    
    def can_use(self, role, tool):
        permissions = self.policy.get(role, {})
        
        if tool in permissions.get('denied', []):
            return False
        
        if tool in permissions.get('require_approval', []):
            # Not denied, but needs approval
            return True
        
        return tool in permissions.get('allowed', [])
```

### Secondary: CI/PR Checks

Validators run as GitHub Actions on PR:

```yaml
# .github/workflows/validators.yml
name: Validators
on: [pull_request]

jobs:
  spec-validator:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python validators/spec_validator.py
      
  design-validator:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python validators/design_validator.py
      
  code-linter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python validators/code_linter.py
      
  qa-checker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python validators/qa_checker.py
```

---

## Risk-Tier → Permission Matrix

### v1 (MVP)

| Tier | Git Write | Run Tests | Web Search | Deploy | Secrets |
|------|-----------|-----------|------------|--------|---------|
| **Low** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Medium** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **High** | ✅ | ✅ | ✅ | ✅ (approval) | ❌ |
| **Critical** | ✅ | ✅ | ✅ | ✅ (multi-approval) | ✅ (approval) |

### Tool Categories

```yaml
TOOL_CATEGORIES:
  git_write:
    - git push
    - git commit
    - git branch create
  
  run_tests:
    - pytest
    - npm test
    - go test
  
  web_search:
    - web_search
    - web_fetch
  
  deploy:
    - npm publish
    - docker push
    - kubectl apply
  
  secrets:
    - env write (API keys)
    - secret create
```

---

## config/policy.yaml

```yaml
# config/policy.yaml
version: "1.0.0"

# Role permissions
roles:
  pm:
    allowed:
      - read_files
      - write_files
      - web_search
      - github_issues
    denied:
      - git_push
      - git_branch_create
      - deploy
      - secrets
    require_approval: []

  designer:
    allowed:
      - read_files
      - write_files
      - web_search
    denied:
      - git_push
      - git_branch_create
      - deploy
      - secrets
      - run_tests
    require_approval: []

  dev:
    allowed:
      - read_files
      - write_files
      - git_push
      - git_branch_create
      - run_tests
      - web_search
    denied:
      - deploy
      - secrets
    require_approval:
      - external_api_calls

  qa:
    allowed:
      - read_files
      - write_files
      - run_tests
      - web_search
    denied:
      - git_push
      - git_branch_create
      - deploy
      - secrets
    require_approval: []

  release:
    allowed:
      - read_files
      - write_files
      - git_push
      - run_tests
      - deploy
    denied:
      - secrets
    require_approval:
      - deploy

# Risk tier thresholds
risk_tiers:
  low:
    max_tool_calls: 50
    max_tokens: 100000
  
  medium:
    max_tool_calls: 100
    max_tokens: 300000
  
  high:
    max_tool_calls: 200
    max_tokens: 500000
    require_approval: true
  
  critical:
    max_tool_calls: 300
    max_tokens: 1000000
    require_multi_approval: true
```

---

## Approval Workflow

### Single Approval (High Risk)

```python
def request_approval(tool, task, agent):
    approval_request = {
        "task_id": task.id,
        "agent": agent.id,
        "tool": tool,
        "risk_tier": task.risk_tier,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Create approval issue
    issue = github.create_issue(
        title=f"Approval needed: {agent} wants to use {tool}",
        body=format_approval_request(approval_request)
    )
    
    return approval_request
```

### Multi-Approval (Critical Risk)

Requires 2 approvals:
1. Technical lead
2. Security lead (for secrets)

---

## Related

- See also: `docs/architecture-v2.md`
- Related issue: #5

---

*Last updated: 2026-02-23*
