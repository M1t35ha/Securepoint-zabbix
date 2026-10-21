# Contributing to Securepoint UTM → Zabbix

Current active artifact: [Standalone v5.6 template](templates/securepoint-utm-standalone-v5.6.yaml), release candidate `v1.0.0-rc.1`.

1. Review the [RC1 acceptance status](docs/RELEASE_CANDIDATE_1.md) and [roadmap](docs/ROADMAP.md) before proposing work.
2. Open an Issue describing **one** reproducible problem: firmware/build (no serial number), Item key/OID, expected vs actual type/value, sanitized error and relevant feature settings.
3. Use a topic branch and small PR. Preserve UUIDs and existing keys for fixes to already-imported Items. Add new UUIDv4 identifiers for new objects.
4. Run:
   ```bash
   python -m pip install -r requirements-dev.txt
   python tools/validate_template.py templates/securepoint-utm-standalone-v5.6.yaml
   python -m unittest discover -s tests -v
   ```
5. Test changes with Zabbix 8.0 against a disposable host or approved lab; record what was **defined by MIB**, **imported**, **returned actual SNMP values**, or **behavior-tested**.
6. Update the [test checklist](docs/TESTING.md), [roadmap](docs/ROADMAP.md), and [changelog](CHANGELOG.md) for feature changes. Documentation-only changes need no new YAML revision.
7. Open a PR into the active release line. Do not silently modify a tested installer without a new test cycle; use RC2 for unverified behavioral changes.

Do not commit proprietary MIB files, authentication material, private network information, client IP addresses, peer identifiers or raw packet/SNMP captures. Monitoring must stay read-only.

The repository currently has no declared permissive/open-source license; ask the owner before copying code in or out.
