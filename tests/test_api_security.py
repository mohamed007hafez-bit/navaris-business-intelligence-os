import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ApiSecurityRegressionTests(unittest.TestCase):
    def test_master_key_is_environment_configured_not_hardcoded(self):
        source = (ROOT / "core" / "master.py").read_text(encoding="utf-8")
        self.assertIn('os.environ.get("NAVARIS_MASTER_KEY"', source)
        self.assertNotIn('MASTER_KEY = "NAVARIS-MASTER-2026"', source)

    def test_task_and_report_routes_require_authorization(self):
        source = (ROOT / "mcp-server" / "server.py").read_text(encoding="utf-8")
        self.assertIn("def create_task(", source)
        self.assertIn("authorize(x_navaris_master_key)", source)
        report = source.split('@app.post("/reports")', 1)[1]
        self.assertIn("x_navaris_master_key: str | None = Header(default=None)", report)
        self.assertIn("authorize(x_navaris_master_key)", report)

    def test_api_fails_closed_when_secret_is_missing(self):
        source = (ROOT / "mcp-server" / "server.py").read_text(encoding="utf-8")
        self.assertIn("if not MASTER_KEY:", source)
        self.assertIn("status_code=503", source)

if __name__ == "__main__":
    unittest.main()
