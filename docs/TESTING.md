# RC1 test checklist — Securepoint UTM Standalone v5.6

This checklist distinguishes **observed values** from **tested behavior**. Latest test evidence: [RC1 report](RELEASE_CANDIDATE_1.md).

## Current test status (2026-10-21)

| Area | Result |
| --- | --- |
| Import + host link in Zabbix 8.0 RC, standalone/no generic parent | **PASS** (user screenshots) |
| Four Host Dashboard tabs | **PASS** |
| Six IF-MIB interfaces, admin/oper status, speed | **PASS** |
| Per-interface RX/TX bit rates and graph prototypes | **PASS** |
| Errors/discards rates and graphs | **PASS** (some LAN inbound discards nonzero) |
| CPU, RAM, uptime, TCP/UDP | **PASS** |
| Manufacturer current/available firmware fields | **PASS** (14.1.6 / 14.1.9.5 at test) |
| License type/remaining days | **PASS** (Software v11 / 90 days at test) |
| Firmware mismatch Problem | **PASS: trigger fired**; delivery/recovery not yet checked |
| WireGuard peer raw/mapped state | **Partial:** Disconnected (0) observed |
| Active peer handshake / IPsec / OpenVPN / AV / services | **Not fully tested** |
| License 30/7/0 triggers, notification delivery, outage recovery | **Not tested** |
| Full 24h unsupported-item/load audit | **Not yet recorded** |

## P0: what to check next

- [ ] **24-hour health:** `Data collection → Hosts → [Firewall] → Items`. Count unsupported Items and inspect sanitized key + Info errors; check LLD count stability and monitoring load.
- [ ] **WireGuard live handshake:** connect a known peer, then compare `Disconnected → Connected`, last-handshake units, and direction/rates of RX/TX against the Securepoint UI. Test disconnect as well.
- [ ] **Services, AV, IPsec and OpenVPN:** compare states with GUI. Record `N/A` if the feature is not configured; don't treat empty tables as errors.
- [ ] **License 30/7/0 days:** test thresholds, recovery and zero-day semantics in an isolated Zabbix test host/lab—not by editing real license or production firewall.
- [ ] **Firmware trigger recovery:** observe after a legitimate future update; do not update solely for a test. Compare firmware channel/build.
- [ ] **SNMP unavailable + critical interface down:** safely test alarm and recovery outside production.
- [ ] **Notification delivery:** confirm Zabbix Action/Media sends to an intended test recipient (a Problem alone is not delivery).
- [ ] **Traffic drops:** establish a baseline for nonzero LAN inbound discards (~1 event/s at one observation); investigate only if persistent/significant.

## Test record template

| Field | Value |
| --- | --- |
| Zabbix version/build | |
| Firewall model (no serial) / UTM firmware | |
| SNMPv3 security level (`authNoPriv` / `authPriv`) | |
| Linked Zabbix templates | |
| Interfaces found; unsupported Items count | |
| Firmware/license OIDs and values (redacted where sensitive) | |
| VPN states compared with UTM GUI | |
| Alert condition, result, recovery and notification delivery | |
| Polling load and LLD stability | |
| Test date / anonymized observations | |

Do not post raw SNMP dumps, real IP addresses, hostnames, peer keys, usernames, customer license identifiers or passwords.

## Offline checks

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_template.py templates/securepoint-utm-standalone-v5.6.yaml
python -m unittest discover -s tests -v
```

Run `python tools/analyze_snmpwalk.py /path/to/private_numeric_walk.txt --json` locally to summarize missing vendor SNMP columns without publishing values. The source walk file may contain private data; keep it out of Git. Offline checks **cannot** confirm Zabbix importer success, actual vendor OID support or alert delivery.
