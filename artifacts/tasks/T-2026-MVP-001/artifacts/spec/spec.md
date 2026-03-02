# Specification: Hello World Endpoint

## Overview
Add a simple HTTP endpoint that returns a JSON greeting.

## Requirements
- Endpoint: GET /hello
- Response: `{ "message": "Hello" }`
- Language: Go

## Acceptance Criteria
1. Endpoint returns 200 OK
2. Response Content-Type: application/json
3. Response body contains "message": "Hello"

## Notes
- This is the E2E vertical slice demo task (T-2026-MVP-001)
- Used to validate the Pipeline mode loop
