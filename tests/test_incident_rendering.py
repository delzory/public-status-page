"""Exercise the pinned theme with incidents without changing real incident history."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class IncidentRenderingTests(unittest.TestCase):
    def test_severity_precedence_and_resolved_incidents(self):
        config = yaml.safe_load((ROOT / "config.yml").read_text())
        first, second = [s["name"] for s in config["params"]["systems"][:2]]
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            shutil.copytree(ROOT / "content", temp / "content")
            # Isolate the scenario from future real incidents.
            shutil.rmtree(temp / "content/issues")
            (temp / "content/issues").mkdir()
            scenarios = [("down", first, False), ("notice", first, False), ("down", second, True)]
            for index, (severity, service, resolved) in enumerate(scenarios):
                fields = dict(title=f"CI fixture {index}", section="issue", date="2026-01-01T12:00:00Z",
                              severity=severity, affected=[service], resolved=resolved)
                if resolved:
                    fields["resolvedWhen"] = "2026-01-01T13:00:00Z"
                (temp / f"content/issues/ci-{index}.md").write_text(
                    "---\n" + yaml.safe_dump(fields) + "---\nTemporary CI incident.\n")
            subprocess.run([str(ROOT / ".tools/hugo"), "--environment", "production",
                            "--contentDir", str(temp / "content"), "--destination", str(temp / "public")],
                           cwd=ROOT, check=True, capture_output=True, text=True)
            home = json.loads((temp / "public/index.json").read_text())
            statuses = {s["name"]: s["status"] for s in home["systems"]}
            self.assertEqual(home["summaryStatus"], "down")
            self.assertEqual(statuses[first], "down")
            self.assertEqual(statuses[second], "ok")


if __name__ == "__main__":
    unittest.main()
