# Roadmap — Securepoint Zabbix

**Current baseline:** `v1.0.0-rc.1` → `templates/securepoint-utm-standalone-v5.6.yaml`. Updated **2026-10-21** from observed live Zabbix screens and CI results.

This tracks **current decisions**, not every historic iteration. See [CHANGELOG](../CHANGELOG.md) for the project history and [RC1 report](RELEASE_CANDIDATE_1.md) for evidence.

## Complete / demonstrated on the initial test device

- [x] Independent Securepoint SNMP template: no linked generic template; imported and linked on Zabbix 8.0 RC.
- [x] Four-page standalone Host Dashboard.
- [x] Targeted IF-MIB LLD: six discovered interfaces, operating/admin status and link speeds.
- [x] 64-bit receive/transmit counter rates and graph history; error and discard counter rates and graphs.
- [x] CPU, RAM, uptime, processes and standard TCP/UDP/IP counters.
- [x] Manufacturer firmware current/available version Items; firmware mismatch Problem appears.
- [x] Manufacturer license type and remaining-day Items respond (90 days during test).
- [x] WireGuard peer `Disconnected (0)` mapped correctly as an SNMP value (not yet verified against a live connection transition).
- [x] No broad `hrStorage` or `hrDevice` discovery; offline YAML/UUID/reference CI checks and sanitized SNMPwalk helper.
- [x] Standalone migration documentation and reproducible RC1 branch/PR.

## P0 — blocking stable v1.0.0

- [ ] Audit *Not supported* Items and LLD stability after at least 24 hours; record sanitized keys and the target firmware/build.
- [ ] Test **active WireGuard peer**: connect/disconnect, last handshake units, sent/received counter directions and accurate state transitions.
- [ ] Validate IPsec/OpenVPN/services/antivirus against the UTM GUI where features are enabled. Inactive features should not generate false failures.
- [ ] Exercise firmware trigger **recovery** safely after a legitimate update; string inequality is not semantic version comparison.
- [ ] Test license thresholds at 30, 7 and 0 days in an isolated Zabbix test environment; verify special/unlimited license semantics.
- [ ] Test SNMP no-data and opt-in critical-interface link-down alarm/recovery without disrupting a production firewall.
- [ ] Confirm Zabbix Actions + Media deliver notifications to intended recipients, not merely create Problems.
- [ ] Review persistent nonzero LAN packet discards and polling cost before alert thresholds.

## P1 — hardening and multi-device compatibility

- [ ] Test on additional Securepoint firmware builds, hardware and virtual UTM, and differing VPN/license configurations.
- [ ] Record capability matrix: numeric OID, data type, firmware availability, observed values, test status.
- [ ] Add isolated **real Zabbix importer smoke test** to CI; YAML validation alone is insufficient.
- [ ] Introduce selective triggers for always-on VPN/services only after the state semantics are verified.
- [ ] Improve version comparison if manufacturer reports update/channel information sufficient to prove ordering.
- [ ] Decide and document public project license with repository owner approval.

## P2 — optional expansion

- [ ] Validate HA, IPsec subnet and backup inventory on a device exposing those features.
- [ ] Consider authenticated read-only API or syslog integration as a separate, privacy-reviewed module.
- [ ] Evaluate aggregate traffic dashboard and better interface grouping once LLD support is proven across devices.

## Rules

Every new item needs evidence of its SNMP OID/type and index, every alert a conservative failure mode, and every feature report a distinction between **defined in MIB**, **Zabbix imported**, **observed data**, and **behavior tested**. Keep the vendor MIB binaries, credentials, raw SNMP walks, license identifiers and customer details out of Git.
