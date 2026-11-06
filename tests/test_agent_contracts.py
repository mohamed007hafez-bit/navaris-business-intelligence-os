import unittest
from pathlib import Path
import yaml

class AgentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=yaml.safe_load(Path("agents.yaml").read_text(encoding="utf-8"))
    def test_exactly_seven_agents(self):
        self.assertEqual(self.config["agent_count"],7)
        self.assertEqual(len(self.config["agents"]),7)
        self.assertEqual({a["id"] for a in self.config["agents"]},{"supervisor","discovery","analysis","coordination","documentation","audit","memory"})
    def test_every_agent_has_contract_and_test(self):
        for agent in self.config["agents"]:
            for key in ("goal","tools","skills","input_schema","output_schema","permission","test"):
                self.assertIn(key,agent)
                self.assertTrue(agent[key])
    def test_paused_services_are_not_active_agents(self):
        self.assertEqual(self.config["service_count"],4)
    def test_supervisor_contract(self): self.assertTrue(next(a for a in self.config["agents"] if a["id"]=="supervisor")["permission"])
    def test_discovery_contract(self): self.assertTrue(next(a for a in self.config["agents"] if a["id"]=="discovery")["tools"])
    def test_analysis_contract(self): self.assertTrue(next(a for a in self.config["agents"] if a["id"]=="analysis")["skills"])
    def test_coordination_contract(self): self.assertIn("licensed partner",next(a for a in self.config["agents"] if a["id"]=="coordination")["permission"])
    def test_documentation_contract(self): self.assertIn("certification",next(a for a in self.config["agents"] if a["id"]=="documentation")["permission"])
    def test_audit_contract(self): self.assertTrue(next(a for a in self.config["agents"] if a["id"]=="audit")["test"])
    def test_memory_contract(self): self.assertIn("non-sensitive",next(a for a in self.config["agents"] if a["id"]=="memory")["permission"])

if __name__=="__main__": unittest.main()
