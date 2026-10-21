"""Offline unit tests for the redacting numeric SNMPwalk analyzer."""
import unittest
from tools.analyze_snmpwalk import BASE, parse_oids, analyze

class SnmpWalkSummaryTest(unittest.TestCase):
    def test_names_and_addresses_are_not_in_output(self):
        lines = [
            ".1.3.6.1.4.1.28553.2.1.11.2.1.2.0.0 = STRING: customer-private-name",
            "iso.3.6.1.4.1.28553.2.1.11.2.1.3.0.0 = INTEGER: 1",
            "iso.3.6.1.4.1.28553.2.1.11.2.1.7.0.0 = Counter64: 500",
            ".1.3.6.1.4.1.28553.1.1.0 = STRING: Serial-and-customer-details",
            "nonsense"
        ]
        result = analyze(parse_oids(lines))
        self.assertEqual(result["tables"]["wireguard_peers"]["discovered_rows"], 1)
        self.assertEqual(result["tables"]["wireguard_peers"]["missing_columns_by_type"]["received"], 1)
        self.assertTrue(result["scalars_present"]["product"])
        self.assertNotIn("customer-private-name", str(result))
        self.assertNotIn("Serial-and-customer-details", str(result))
        self.assertNotIn("0.0", str(result))

    def test_no_walk_entries(self):
        result = analyze(parse_oids(["Malformed", "text"]))
        self.assertEqual(result["parsed_oids"], 0)
        self.assertEqual(result["tables"]["services"]["discovered_rows"], 0)

if __name__ == "__main__":
    unittest.main()
