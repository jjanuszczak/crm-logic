import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from frontmatter_utils import load_frontmatter_file, serialize_frontmatter


def load_intelligence_engine():
    spec = importlib.util.spec_from_file_location(
        "intelligence_engine_test",
        REPO_ROOT / "scripts/intelligence-engine.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class IntelligenceEngineTests(unittest.TestCase):
    def test_unchanged_telemetry_does_not_touch_date_modified(self):
        engine = load_intelligence_engine()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Account.md"
            path.write_text(
                serialize_frontmatter(
                    {
                        "warmth-score": 1,
                        "warmth-status": "cold",
                        "velocity-score": 0,
                        "account-warmth-index": 1,
                        "date-modified": "2026-08-19",
                    }
                )
                + "# Account\n",
                encoding="utf-8",
            )

            changed = engine.update_frontmatter(
                str(path),
                {
                    "warmth-score": 1,
                    "warmth-status": "cold",
                    "velocity-score": 0,
                    "account-warmth-index": 1,
                },
            )

            self.assertFalse(changed)
            self.assertEqual(
                str(load_frontmatter_file(path)[0]["date-modified"]),
                "2026-08-19",
            )

    def test_changed_telemetry_writes_record(self):
        engine = load_intelligence_engine()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Account.md"
            path.write_text(
                serialize_frontmatter({"warmth-score": 1}) + "# Account\n",
                encoding="utf-8",
            )

            changed = engine.update_frontmatter(
                str(path),
                {"warmth-score": 2, "date-modified": "2026-08-20"},
            )

            self.assertTrue(changed)
            self.assertEqual(load_frontmatter_file(path)[0]["warmth-score"], 2)


if __name__ == "__main__":
    unittest.main()
