import unittest
from navaris_core_engine import (DEFAULT_INTERMEDIARY_COMMISSION_RATE, AUTONOMOUS_AGENTS,
    VERTICALS, cash_collected, commission_spread, financial_snapshot,
    operating_expense_ratio, operating_margin)

class TestNAVARISCoreEngine(unittest.TestCase):
    def test_oer_formula(self):
        self.assertAlmostEqual(operating_expense_ratio(25, 100), 25.0)
    def test_operating_margin_allows_loss(self):
        self.assertAlmostEqual(operating_margin(-5, 100), -5.0)
    def test_nonpositive_revenue_is_not_calculable(self):
        self.assertIsNone(operating_expense_ratio(10, 0))
        self.assertIsNone(operating_margin(10, -1))
    def test_commission_default_is_fifteen_percent(self):
        self.assertEqual(DEFAULT_INTERMEDIARY_COMMISSION_RATE, 0.15)
        self.assertAlmostEqual(commission_spread(1000), 150.0)
    def test_invalid_commission_rate_rejected(self):
        with self.assertRaises(ValueError):
            commission_spread(100, 1.2)
    def test_cash_defaults_to_zero_without_receipt(self):
        self.assertEqual(cash_collected(None), 0.0)
        self.assertEqual(cash_collected({"amount": 1000, "evidence_type": "INVOICE"}), 0.0)
    def test_cash_requires_verified_reconciled_bank_receipt(self):
        record = {"amount":"125.50","currency":"EGP","bank_transaction_reference":"TX-1",
          "received_date":"2026-10-29","evidence_reference":"redacted://receipt/hash",
          "verified_by":"finance-reviewer","verified_at":"2026-10-29T09:00:00Z",
          "reconciliation_reference":"REC-1","evidence_type":"BANK_RECEIPT",
          "verification_status":"VERIFIED_BY_FINANCE","reconciliation_status":"RECONCILED"}
        self.assertEqual(cash_collected(record), 125.5)
        record["reconciliation_status"] = "PENDING"
        self.assertEqual(cash_collected(record), 0.0)
    def test_registry_has_nine_verticals_and_five_coordinators(self):
        self.assertEqual(len(VERTICALS), 9)
        self.assertEqual(len(AUTONOMOUS_AGENTS), 5)
    def test_snapshot_defaults_cash_to_zero(self):
        result = financial_snapshot(opex=20, ebit=10, net_revenue=100)
        self.assertEqual(result["cash_collected"], 0.0)
        self.assertEqual(result["operating_expense_ratio_percent"], 20.0)
        self.assertEqual(result["operating_margin_percent"], 10.0)

if __name__ == "__main__":
    unittest.main()
