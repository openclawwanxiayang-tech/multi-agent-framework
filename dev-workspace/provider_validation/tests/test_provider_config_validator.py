import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "validators" / "provider_config_validator.py"


def run_validator(config_path: Path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(config_path)],
        capture_output=True,
        text=True,
    )


class ProviderConfigValidatorTests(unittest.TestCase):
    def test_valid_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "providers.yaml"
            cfg.write_text(
                """
providers:
  - name: openai
    model: gpt-5
    api_base: https://api.example.com
    api_key_env: OPENAI_API_KEY
""".strip(),
                encoding="utf-8",
            )
            result = run_validator(cfg)
            self.assertEqual(result.returncode, 0)
            self.assertIn("is valid", result.stdout)

    def test_missing_required_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "providers.yaml"
            cfg.write_text(
                """
providers:
  - name: openai
    model: gpt-5
    api_base: https://api.example.com
""".strip(),
                encoding="utf-8",
            )
            result = run_validator(cfg)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("provider[0] openai: missing required field 'api_key_env'", result.stderr)

    def test_malformed_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "providers.yaml"
            cfg.write_text("providers: [name: openai", encoding="utf-8")
            result = run_validator(cfg)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("yaml error", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
