# Design: Hello World Endpoint

## Architecture
- Simple HTTP handler in Go
- Standard library net/http

## Implementation Details
- File: main.go
- Handler function: `helloHandler(w http.ResponseWriter, r *http.Request)`

## Error States
- Unsupported method returns default handler behavior (future hardening can enforce 405).
- JSON encoding failure should be treated as internal server error in future revisions.

## Testing Strategy
- Unit test for helloHandler using net/http/httptest

## Test Considerations
- Validate status code, content type, and body payload.

## File Structure
```
main.go       - HTTP server and handler
main_test.go  - Unit tests
```
