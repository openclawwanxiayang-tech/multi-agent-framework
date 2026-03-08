# Acceptance: Hello World Endpoint

## Pass Criteria
1. `GET /hello` responds with HTTP 200.
2. `Content-Type` is `application/json`.
3. Body includes `{"message":"Hello"}`.

## Fail Criteria
- Any non-200 status.
- Missing/incorrect `Content-Type`.
- Missing `message` field.

## Evidence
- Unit test: `artifacts/impl/main_test.go`
- Runtime contract: `artifacts/impl/main.go`
