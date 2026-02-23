# Schema Migration Rules

> Version: 1.0.0  
> Last Updated: 2026-02-23

---

## Schema Versioning

Each schema includes a `$version` field for migration tracking:

```json
{
  "$version": "1.0.0",
  ...
}
```

### Version Format

```
MAJOR.MINOR.PATCH
```

| Component | Change Type |
|-----------|-------------|
| **MAJOR** | Breaking change - requires migration |
| **MINOR** | Backward compatible - can add fields |
| **PATCH** | Documentation/format only - no change needed |

---

## Migration Rules

### Rule 1: Read Version First

Before processing any schema, always check `$version`:

```python
def process_task(data):
    version = data.get("$version", "0.0.0")
    
    if version != CURRENT_VERSION:
        data = migrate_task(data, version)
    
    return validate_task(data)
```

### Rule 2: Major Version Bumps Require Migration Script

When MAJOR version changes:

1. Create migration script: `migrations/v{major}_to_v{new}.py`
2. Test migration on all known previous versions
3. Document breaking changes in CHANGELOG

### Rule 3: Minor Version Additions Are Optional

When MINOR version changes (new optional fields):

- Old data is valid without migration
- New fields have defaults or are optional
- No migration script needed

### Rule 4: Patch Is Transparent

PATCH versions are for documentation only:

- No code changes required
- No migration needed

---

## Migration Examples

### Example: Adding Required Field (Major)

v1.0.0 → v2.0.0 (adding `owner` field)

```python
# migrations/v1_to_v2.py
def migrate_task_v1_to_v2(data):
    if "owner" not in data:
        data["owner"] = "unassigned"  # default
    data["$version"] = "2.0.0"
    return data
```

### Example: Adding Optional Field (Minor)

v1.0.0 → v1.1.0 (adding `tags` field)

```python
# No migration needed - field is optional
def validate_task_v1_1_0(data):
    # tags is optional, no validation required
    return True
```

---

## Current Schemas

| Schema | Version | Status |
|--------|---------|--------|
| task.json | 1.0.0 | ✅ Final |
| state.json | 1.0.0 | ✅ Final |
| envelope.json | 1.0.0 | ✅ Final |
| event.json | 1.0.0 | ✅ Final |

---

## Validation

### CLI Validation

```bash
# Validate a task
ajv validate -s schemas/task.json -d data/task.json

# Validate all schemas
for schema in schemas/*.json; do
    ajv validate -s "$schema" -d "data/$(basename $schema)"
done
```

### Python Validation

```python
from jsonschema import validate, Draft7Validator
import json

def validate_task(data):
    with open('schemas/task.json') as f:
        schema = json.load(f)
    
    validator = Draft7Validator(schema)
    if not validator.is_valid(data):
        raise ValueError(validator.iter_errors(data))
```

---

## Future Schema Changes

When updating schemas:

1. Increment version appropriately
2. Add migration script if MAJOR change
3. Update this document
4. Update CHANGELOG

---

*Last updated: 2026-02-23*
