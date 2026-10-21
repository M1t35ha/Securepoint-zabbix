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

## Must still be verified before v1.0.0 stable

- [ ] After at least two polls, RX/TX bit-rate, errors/s and discards/s values populate and match device/network expectations.
- [ ] Interface throughput and errors/discards graph prototypes show realistic history.
- [ ] WireGuard peer state and handshake reflect real connectivity (interface Up is not peer Up).
- [ ] Vendor MIB firmware (installed/available), license days and license type actually return values. Earlier dashboards displayed **No data** for some of these fields.
- [ ] Firmware mismatch and 30/7-day license alerts correctly evaluate real values; clarify zero-day semantics.
- [ ] SNMP no-data alert, opt-in link-down alarms, and service state mappings are tested without false positives.
- [ ] Confirm performance / SNMP polling load with configured interface count.

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
