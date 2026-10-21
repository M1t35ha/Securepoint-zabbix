# Roadmap

## Unified v5 candidate (2026-10-21)

- [x] Research community IPsec/WireGuard implementations and Zabbix SNMP template practices.
- [x] Combine manufacturer-MIB v4 with selected operational standard counters from v3.
- [x] Restore network diagnostics and graphs without hrStorage/hrDevice discovery.
- [x] Optional CPU discovery; per-service and per-tunnel alerts opt-in.
- [x] Document included/excluded capabilities, provenance, privacy and a test plan.
- [ ] Pass offline CI for v5 **and** v4.
- [ ] Confirm import in Zabbix 8.0 test host.
- [ ] Verify every vendor OID and optional table on firmware 14.x via sanitized snmpwalk.
- [ ] Compare semantics and graphs against firewall GUI.
- [ ] Only then mark release `v5.0.0` and consider production migration.


This is a prioritized engineering plan, **not** a claim of current support.

- [x] Establish public repository, template location and documentation.
- [x] Add MIB-derived status maps and conservative six active / two optional discoveries.
- [x] Guard against repeating broad hrStorage/hrDevice discovery and zero-denominator swap formulas.
- [ ] Confirm successful import on Zabbix 8.0 RC/build.
- [ ] Record a sanitized, device-verified capability matrix for UTM 14.x.
- [ ] Verify WireGuard last-handshake time representation; add last-handshake age only after verification.
- [ ] Verify peer traffic counters and reset behavior; improve per-peer graphs.
- [ ] Add per-VPN/service dashboard with operational status, uptime and current sessions.
- [ ] Validate HA, IPsec subnet and backup optional data on appropriate devices.
- [ ] Add cautious, context-macro controlled alerts for required IPsec and WireGuard peers.
- [ ] Evaluate non-SNMP data via supported API/syslog sources, with read-only scope and privacy review.
- [ ] Add a genuine Zabbix 8.0 import smoke test to CI using an isolated container; offline YAML validation alone is not sufficient.

## Engineering rules

Every new OID must have a documented type, an explicitly stated source (MIB/standard MIB/live observation), evidence of support on tested firmware, stable discovery indexing and a safe failure mode. Every new alert must explain whether the device might be intentionally offline.
