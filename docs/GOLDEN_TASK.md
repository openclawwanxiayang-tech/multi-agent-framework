# Golden Task: Hello World Endpoint

> Task ID: T-2026-MVP-001  
> Purpose: E2E vertical slice demo for Pipeline mode  
> Last Updated: 2026-02-23

---

## Overview

This is the first "golden task" used to validate the end-to-end Pipeline loop. It should pass all validators and produce complete artifacts.

---

## Input

### User Request

```
Add a simple /hello endpoint that returns { "message": "Hello" }
```

### Task Configuration

```json
{
  "$version": "1.0.0",
  "task_id": "T-2026-MVP-001",
  "title": "Add Hello World Endpoint",
  "created_at": "2026-02-23T10:00:00Z",
  "mode": "pipeline",
  "risk_tier": "low",
  "definition_of_done": [
    "Spec approved",
    "Design approved",
    "Implementation merged",
    "Tests passing"
  ],
  "budgets": {
    "max_tool_calls": 50,
    "max_total_tokens": 100000
  }
}
```

---

## Expected Artifacts

| Stage | Artifact | Path | Validator |
|-------|----------|------|-----------|
| SPEC | spec.md | `artifacts/tasks/T-2026-MVP-001/artifacts/spec/spec.md` | spec_validator.py |
| DESIGN | design.md | `artifacts/tasks/T-2026-MVP-001/artifacts/design/design.md` | design_validator.py |
| IMPLEMENT | main.go | `artifacts/tasks/T-2026-MVP-001/artifacts/impl/main.go` | code_linter.py |
| IMPLEMENT | main_test.go | `artifacts/tasks/T-2026-MVP-001/artifacts/impl/main_test.go` | code_linter.py |
| QA | results.md | `artifacts/tasks/T-2026-MVP-001/artifacts/qa/results.md` | qa_checker.py |

---

## Expected Content

### SPEC.md

```markdown
# Specification: Hello World Endpoint

## Overview
Add a simple HTTP endpoint that returns a JSON greeting.

## Requirements
- Endpoint: GET /hello
- Response: { "message": "Hello" }
- Language: Go

## Acceptance Criteria
1. Endpoint returns 200 OK
2. Response Content-Type: application/json
3. Response body contains "message": "Hello"
```

### DESIGN.md

```markdown
# Design: Hello World Endpoint

## Architecture
- Simple HTTP handler in Go
- Standard library net/http

## Implementation
- File: main.go
- Handler function: helloHandler(w http.ResponseWriter, r *http.Request)

## Testing
- Unit test for helloHandler
```

### main.go

```go
package main

import (
    "encoding/json"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(Response{Message: "Hello"})
}

func main() {
    http.HandleFunc("/hello", helloHandler)
    http.ListenAndServe(":8080", nil)
}
```

### main_test.go

```go
package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHelloHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/hello", nil)
    w := httptest.NewRecorder()
    
    helloHandler(w, req)
    
    if w.Code != http.StatusOK {
        t.Errorf("Expected status 200, got %d", w.Code)
    }
    
    if w.Header().Get("Content-Type") != "application/json" {
        t.Errorf("Expected Content-Type: application/json")
    }
}
```

---

## Validation Checklist

- [ ] spec_validator.py passes
- [ ] design_validator.py passes
- [ ] Code compiles: `go build ./...`
- [ ] Tests pass: `go test ./...`
- [ ] events.ndjson contains all events
- [ ] state.json shows full lifecycle: SPEC → DESIGN → IMPLEMENT → REVIEW → QA → DONE

---

## State Progression

### After SPEC

```json
{
  "$version": "1.0.0",
  "task_id": "T-2026-MVP-001",
  "stage": "SPEC",
  "status": "COMPLETED",
  "assigned": [{"role": "pm", "agent_id": "agent-pm-1"}],
  "checkpoints": [{"stage": "SPEC", "artifact": "artifacts/spec/spec.md", "hash": "sha256:..."}]
}
```

### After DESIGN

```json
{
  "$version": "1.0.0",
  "task_id": "T-2026-MVP-001",
  "stage": "DESIGN",
  "status": "COMPLETED",
  "assigned": [{"role": "designer", "agent_id": "agent-designer-1"}],
  "checkpoints": [
    {"stage": "SPEC", "artifact": "artifacts/spec/spec.md", "hash": "sha256:..."},
    {"stage": "DESIGN", "artifact": "artifacts/design/design.md", "hash": "sha256:..."}
  ]
}
```

### After IMPLEMENT

```json
{
  "$version": "1.0.0",
  "task_id": "T-2026-MVP-001",
  "stage": "IMPLEMENT",
  "status": "COMPLETED",
  "assigned": [{"role": "dev", "agent_id": "agent-dev-1"}],
  "checkpoints": [
    {"stage": "SPEC", "artifact": "artifacts/spec/spec.md", "hash": "sha256:..."},
    {"stage": "DESIGN", "artifact": "artifacts/design/design.md", "hash": "sha256:..."},
    {"stage": "IMPLEMENT", "artifact": "artifacts/impl/main.go", "hash": "sha256:..."}
  ]
}
```

### After DONE

```json
{
  "$version": "1.0.0",
  "task_id": "T-2026-MVP-001",
  "stage": "DONE",
  "status": "COMPLETED",
  "assigned": [],
  "checkpoints": [
    {"stage": "SPEC", "artifact": "artifacts/spec/spec.md", "hash": "sha256:..."},
    {"stage": "DESIGN", "artifact": "artifacts/design/design.md", "hash": "sha256:..."},
    {"stage": "IMPLEMENT", "artifact": "artifacts/impl/main.go", "hash": "sha256:..."},
    {"stage": "QA", "artifact": "artifacts/qa/results.md", "hash": "sha256:..."}
  ]
}
```

---

## Related

- See also: `docs/tasks.md` Milestone 2.13
- Related issue: #6

---

*Last updated: 2026-02-23*
