import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_status import load_yaml, validate_config, validate_incident


class ValidationTests(unittest.TestCase):
    def incident(self, **overrides):
        return dict(title="Service unavailable", section="issue", date="2026-01-01T12:00:00Z",
                    severity="down", affected=["Portal"], resolved=False, **overrides)

    def test_duplicate_yaml_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate YAML key"):
            load_yaml("resolved: false\nresolved: true")

    def test_unknown_category_is_rejected(self):
        config = dict(baseURL="https://status.example.com", params=dict(
            categories=[dict(name="Account")], systems=[dict(name="Portal", category="Acccount")]))
        with self.assertRaisesRegex(ValueError, "Unknown category"):
            validate_config(config)

    def test_unknown_affected_service_is_rejected(self):
        value = self.incident()
        value["affected"] = ["Poratl"]
        with self.assertRaisesRegex(ValueError, "Unknown affected"):
            validate_incident(value, {"Portal"})

    def test_invalid_resolution_order_is_rejected(self):
        value = self.incident()
        value.update(resolved=True, resolvedWhen="2026-01-01T11:00:00Z")
        with self.assertRaisesRegex(ValueError, "cannot precede"):
            validate_incident(value, {"Portal"})

    def test_valid_incident_and_empty_informational_post(self):
        validate_incident(self.incident(), {"Portal"})
        value = self.incident()
        value.update(informational=True, affected=[])
        validate_incident(value, {"Portal"})


if __name__ == "__main__":
    unittest.main()
