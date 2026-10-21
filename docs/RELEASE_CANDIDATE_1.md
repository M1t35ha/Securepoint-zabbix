# Securepoint UTM → Zabbix — Release Candidate 1

**Release ID:** `v1.0.0-rc.1`  
**Baseline:** `Securepoint UTM Standalone v5.6 by SNMP`  
**Status:** test candidate — **NOT** production-certified

## Installation artifact

- [Standalone v5.6 Zabbix YAML](../templates/securepoint-utm-standalone-v5.6.yaml)
- [Migration and rollback](V5_6_STANDALONE.md)
- [Test checklist](TESTING.md)
- [OID / manufacturer SNMP reference](OID_REFERENCE.md)
- [Russian setup notes](README_RU.md)

The RC branch was created from the previously CI-checked `feature/utm-v5-unified` tip. This is a **snapshot of existing work**, not a claim that untested modules are operational. It does not depend on the generic `Network Generic Device by SNMP` template and includes four own Host Dashboard pages: Overview, Network, Interfaces, VPN & Security.

## Observed in a real Zabbix 8.0 instance (October 21, 2026)

- [x] Standalone template imported and linked to the `Firewall` host with no inherited network template shown.
- [x] SNMPv3 host interface is configured.
- [x] Six network interfaces discovered (LAN/VLAN, tunnel and WireGuard).
- [x] Interface operating/admin status maps populate as **Up / Enabled**.
- [x] Interface link speed values populate (1 Gbps for LAN-like interfaces, 0 reported for virtual VPN).
- [x] Host Dashboard `Interfaces` shows the new consolidated tables.

## Second live acceptance observation — 2026-10-21

Additional user-provided Zabbix Dashboard and Problems screenshots **confirm** these test-device behaviors. Values are snapshots and must not be confused with long-term baselines:

- [x] **RX/TX rates populate** after multiple samples across detected interfaces. Example observed: LAN1 received around 3.15 Mbps; another LAN transmit rate around 3.14 Mbps. Both nonzero rates and zero idle links are visible.
- [x] **Interface throughput graph prototype** displays real RX/TX bit-rate history.
- [x] **IF-MIB input/output errors and discards per second** populate. Error readings shown as 0 events/s; inbound discards on two LAN-like interfaces about 1 event/s, and a small nonzero outgoing discard rate on one WireGuard interface.
- [x] **Errors/discards graph prototype** draws actual historical series (including a nonzero discard line).
- [x] **Standard CPU/RAM and TCP/UDP metrics** produce values in the Overview and Network dashboards.
- [x] **Manufacturer firmware SNMP fields respond:** installed `14.1.6`, manufacturer-reported new `14.1.9.5`.
- [x] **License SNMP fields respond:** remaining days `90`, license type `Software v11`.
- [x] **Firmware mismatch trigger is active:** Zabbix Problems shows `UTM: firmware update reported by manufacturer`. This validates the trigger for *different current/new version strings*, not semantic version ordering or notification delivery to email.
- [x] **WireGuard peer-state Item reports a mapped value:** Disconnected (0) for an observed peer. **No connection/handshake recovery has been verified**.
- [x] The four-page standalone dashboard renders: Overview, Network, Interfaces, VPN & Security.

### Remaining test gates before v1.0.0 Stable

- [ ] **WireGuard peer up/down transition**, last handshake and RX/TX counters: compare with UTM UI during a known active session (not merely wg interface Up).
- [ ] **IPsec state / OpenVPN client count / antivirus / service LLD**: compare with GUI when features are configured; empty IPsec table is not an integration failure by itself. The screenshot's WireGuard Disconnected and OpenVPN zero clients might be normal.
- [ ] **Firmware update trigger recovery:** check it clears when manufacturer-reported available version matches installed version, without changing a production firewall just for testing.
- [ ] **License thresholds:** test 30-day WARNING, 7-day HIGH, handling of exactly zero days, recovery and notification routing in an isolated Zabbix test environment. Current license 90 days does *not* exercise those thresholds.
- [ ] **No-SNMP-data (15m)** and opt-in physical interface-down trigger: validate conditions and recoveries without taking down the production firewall.
- [ ] **Severity / notification delivery:** confirm Actions, Media types and recipients are configured, if external notifications are wanted. A visible Problem is not proof of a delivered notification.
- [ ] **Sustained discarded packets** (approximately 1 per second observed on two LAN interfaces): establish a baseline and check for drops/congestion or SNMP counter semantics if persistent. Do not call it a hardware fault from one screenshot.
- [ ] **Longer polling stability and load**: verify no significant unsupported items, unexpected LLD proliferation or undue SNMP load after a day.

**Release status:** strong evidence for standalone SNMP system, IF-MIB monitoring and manufacturer firmware/license collection on this device; not yet evidence that every vendor feature or alarm is production-ready. No private hostname, management IP or identity is recorded.

## Project / branch policy

- `main`: conservative baseline and project overview; do not mistake it for RC1.
- `release/1.0.0-rc.1`: frozen integration test baseline; bugfixes for RC1 are made here deliberately.
- `feature/utm-v5-unified`: previous integrated development history retained for reference.
- Only merge RC1 into `main` and create a stable tag **after** acceptance checks. If changes are needed, increment to `rc.2` or track verified fixes explicitly.

Do not publish proprietary Securepoint MIB files, real SNMPv3 credentials, private interface addresses or customer-specific logs.

## Zabbix cleanup

Once `Securepoint UTM Standalone v5.6 by SNMP` is the host's only linked template and its desired data is collecting, **unused old Securepoint templates** can be deleted under **Data collection → Templates**. Check their linked hosts before deletion. Do not globally delete `Network Generic Device by SNMP` if other hosts use it; it may remain installed yet detached from this Firewall.

Avoid using `Delete missing` during routine YAML imports. Existing host history was already intentionally cleared during the switch to standalone; do not assume reimporting an old template restores that history.

**Validation scope:** GitHub Actions checks YAML schema shape/UUIDs/internal references and local SNMPwalk helper tests. It does **not** perform a live Zabbix import or prove every SNMP OID exists on a target device.
