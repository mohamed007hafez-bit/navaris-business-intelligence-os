"""Regression tests for the safe, deterministic local workflow agents."""
import unittest

from backend.workflow import AGENT_SEQUENCE, run_workflow


class LocalWorkflowTests(unittest.TestCase):
    def test_runs_all_named_agents_as_draft(self):
        result = run_workflow({"sector": "Operations", "problem": "Reduce late handoffs"})
        self.assertEqual([step["agent"] for step in result["agents"]], list(AGENT_SEQUENCE))
        self.assertEqual(result["status"], "DRAFT_REVIEW_REQUIRED")
        self.assertTrue(result["human_approval_required"])
        self.assertEqual(result["external_actions"], "DISABLED")

    def test_missing_source_is_reported_not_invented(self):
        result = run_workflow({
            "sector": "Operations",
            "problem": "Review cost",
            "facts": [{"label": "Revenue", "value": 100}],
        })
        self.assertIn("Revenue: source reference is missing", result["evidence_gaps"])
        self.assertIsNone(result["case"]["facts"][0]["source_ref"])
        self.assertEqual(result["case"]["facts"][0]["status"], "EVIDENCE_REQUIRED")

    def test_valid_risk_score_is_calculated_from_input(self):
        result = run_workflow({
            "sector": "Operations",
            "problem": "Review delivery risk",
            "risks": [{"id": "R-1", "description": "Delay", "likelihood": 3, "impact": 4}],
        })
        self.assertEqual(result["risk_register"][0]["score"], 12)
        self.assertEqual(result["risk_register"][0]["status"], "CALCULATED_FROM_INPUT")

    def test_out_of_range_risk_is_not_calculated(self):
        result = run_workflow({
            "sector": "Operations",
            "problem": "Review delivery risk",
            "risks": [{"likelihood": 6, "impact": 2}],
        })
        self.assertIsNone(result["risk_register"][0]["score"])
        self.assertEqual(result["risk_register"][0]["status"], "INPUT_REQUIRED")

    def test_required_case_fields_are_explicit(self):
        result = run_workflow({})
        self.assertIn("Case field required: sector", result["evidence_gaps"])
        self.assertIn("Case field required: problem", result["evidence_gaps"])
        self.assertTrue(any("no valuation" in item for item in result["limitations"]))


if __name__ == "__main__":
    unittest.main()
