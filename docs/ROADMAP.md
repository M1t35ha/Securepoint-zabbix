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

## v5.5 interface support (2026-10-21)

- [x] Add status, link speed, errors and discards to bounded IF-MIB discovery.
- [x] Dedicated **Interfaces** page listing all discovered devices at once; traffic and error graph prototypes remain selectable.
- [x] Preserve vendor VPN/firmware/license features and official generic SNMP parent.
- [x] Document the inherited **Network interfaces** dashboard limitation and safe removal options.
- [ ] Confirm all interface statuses and rates on actual Securepoint 14.x firmware.
- [ ] If only Firewall should hide the parent dashboard, trial a detached/clone approach on a separate host; do not remove generic monitoring without checking macros and history.

## v5.6 Standalone (2026-10-21)

- [x] Build separate standalone YAML with NO generic SNMP template inheritance.
- [x] Preserve own IF-MIB discovery, all four dashboard pages, and Securepoint VPN/license/firmware Items.
- [x] Add self-monitoring of missing SNMP data and opt-in critical interface link-down alerts.
- [x] Write migration/rollback guide, including two-step Unlink and clear and history-loss warning.
- [ ] Complete live import and Zabbix 8.0 host acceptance.
- [ ] Confirm interface discovery, status, link speed and missing SNMP OIDs against Securepoint GUI.
- [ ] Verify firmware/license vendor fields and alert routing to email/Teams before rolling out.
