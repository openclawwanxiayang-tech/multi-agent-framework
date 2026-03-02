# Design: Hello World Endpoint

## Architecture
- Simple HTTP handler in Go
- Standard library net/http

## Implementation Details
- File: main.go
- Handler function: `helloHandler(w http.ResponseWriter, r *http.Request)`

## Testing Strategy
- Unit test for helloHandler using net/http/httptest

## File Structure
```
main.go       - HTTP server and handler
main_test.go  - Unit tests
```
