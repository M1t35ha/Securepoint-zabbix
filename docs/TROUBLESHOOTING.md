# Troubleshooting and lessons learned

The earlier experimental v2/v3 builds generated over 400 Items on one installation. This was caused by over-broad HOST-RESOURCES-MIB discovery and unsupported per-row columns. The maintained template removes those discoveries.

| Error | What it means | Response |
| --- | --- | --- |
| `No Such Instance currently exists at this OID` | SNMP agent does not expose requested instance | Check that the scalar ends with `.0`; for tables, verify actual discovery indices and whether the specific column is implemented |
| `Cannot evaluate function: not enough data` | Calculated/dependent Item has no valid source data yet | Fix the master Item first; do not add more dependent Items |
| `division by zero` | Denominator is zero (for example absent swap) | No SWAP percentage in maintained template; use expressions that verify denominator or avoid division |
| Import: unexpected `tags` under `discovery_rules` | Field is not allowed at that nesting point | Put tags on Items/prototypes rather than LLD rule |
| Missing generic network metrics | Built-in generic SNMP template not installed/linked | Import official `Network Generic Device by SNMP` and ensure inheritance |
| Correct number, confusing state | Missing manufacturer value mapping | Map only enums defined by the actual MIB; do not invent states |
| Many Items unsupported after import | Template incorrectly assumes all MIB tables exist on your model | Disable unsupported optional rules, capture sanitized OID inventory, change template in PR |

## Debugging discipline

1. Classify the failed Item as **scalar**, **table**, or **calculated/dependent**.
2. Inspect OID and type in [OID reference](OID_REFERENCE.md).
3. Check real SNMP response directly from the Zabbix server using a restricted account (do not paste authentication secrets into issues).
4. Make one change per test branch. Run `python tools/validate_template.py templates/securepoint-utm-mib-v4.yaml` and retest on the test host.
5. Only after stable collection add rates, graph units and trigger thresholds.
6. Do not re-enable broad `hrStorage`/`hrDevice` rules without a narrow, documented and device-tested filter.

## Compatibility reports

Create an issue containing version, list of keys, and sanitized errors from the checklist in [TESTING.md](TESTING.md). Do not post IP addresses, tunnel names or credentials.

## Host update: graph `Securepoint: CPU core {#SNMPINDEX} - utilisation` already exists

A v2/v3 graph prototype had the same name as the optional v5 per-core CPU graph, but its Items have different keys. Zabbix refuses the host update even if the new CPU discovery is disabled. **Do not unlink-and-clear or erase historical data solely to resolve this.** The v5 graph prototype was renamed to `Securepoint UTM v5: CPU core {#SNMPINDEX} usage`. Re-import the corrected template with *Update existing* enabled and *Delete missing* disabled; then retry host linkage. Other conflicts, if any, must be diagnosed by their exact Zabbix error.
