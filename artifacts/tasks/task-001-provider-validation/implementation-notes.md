# task-001-provider-validation — implementation notes

## What was added
- CLI validator: `validators/provider_config_validator.py`
- Tests: `dev-workspace/provider_validation/tests/test_provider_config_validator.py`

## Usage
```bash
python3 validators/provider_config_validator.py
# default path: config/providers.yaml

python3 validators/provider_config_validator.py /path/to/providers.yaml
```

## Validation rules
Each provider must contain non-empty string values for:
- `name`
- `model`
- `api_base`
- `api_key_env`

Accepted top-level YAML shapes:
1. list of providers
2. object with `providers: [...]`

## Exit codes
- `0`: config valid
- non-zero: invalid config, missing file, malformed YAML, or wrong schema

## Error output format
Errors include provider index and name where possible, e.g.:
- `provider[0] openai: missing required field 'api_key_env'`
- `provider[1] azure: invalid field 'api_base' (must be non-empty string)`
