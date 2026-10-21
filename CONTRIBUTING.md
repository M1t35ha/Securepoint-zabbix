# Contributing

We welcome useful, reproducible improvements to Securepoint UTM monitoring.

1. Open an issue with a **sanitized** description of the device version, failing Item key/OID, or feature gap.
2. Create a branch with a small, reviewable change.
3. Keep existing template UUIDs and Item keys stable when updating an existing Item. Never change a key just to reword its label.
4. Run `python -m pip install -r requirements-dev.txt` and `python tools/validate_template.py templates/securepoint-utm-mib-v4.yaml`.
5. Test on a separate Zabbix host. Provide results from `docs/TESTING.md` (import result, Supported/Unsupported, LLD counts).
6. Send a Pull Request. Explicitly list what was **MIB-mapped**, what was **live-tested** and what remains **assumed/unconfirmed**.

Do not commit proprietary manufacturer MIB files, client network identifiers, authentication credentials, SNMP dumps, or captured session data. Proposed monitoring checks should be read-only.
