#!/usr/bin/env python3
"""Validate provider entries in config/providers.yaml."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REQUIRED_FIELDS = ("name", "model", "api_base", "api_key_env")


def _load_providers(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("providers"), list):
        return data["providers"]
    raise ValueError("Expected a list of providers or a top-level 'providers' list")


def _validate_provider(provider, idx: int):
    if not isinstance(provider, dict):
        return [f"provider[{idx}] <unknown>: provider entry must be a mapping/object"]

    name = str(provider.get("name") or f"provider[{idx}]")
    errors = []
    for field in REQUIRED_FIELDS:
        value = provider.get(field)
        if value is None:
            errors.append(f"provider[{idx}] {name}: missing required field '{field}'")
        elif not isinstance(value, str) or not value.strip():
            errors.append(f"provider[{idx}] {name}: invalid field '{field}' (must be non-empty string)")
    return errors


def validate_file(path: Path):
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"file error: '{path}' does not exist"]

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return [f"yaml error in '{path}': {exc}"]

    try:
        providers = _load_providers(data)
    except ValueError as exc:
        return [f"schema error in '{path}': {exc}"]

    errors = []
    for idx, provider in enumerate(providers):
        errors.extend(_validate_provider(provider, idx))
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate provider config YAML")
    parser.add_argument(
        "config_path",
        nargs="?",
        default="config/providers.yaml",
        help="Path to providers YAML (default: config/providers.yaml)",
    )
    args = parser.parse_args(argv)

    path = Path(args.config_path)
    errors = validate_file(path)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1

    print(f"OK: {path} is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
