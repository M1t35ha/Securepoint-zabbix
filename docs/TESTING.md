# Acceptance test checklist

## Additional v5 acceptance gates

- [ ] Run CI on **both v4 and v5** templates; confirm all graph references/UUIDs are unique.
- [ ] Import candidate into isolated test host, not existing production monitored host.
- [ ] Compare v3's previously functional HR/TCP/IP counters with new v5 `sp.std.*` and `sp.hr.*`.
- [ ] Inspect all 9 discovery rules; optional per-CPU, HA, subnet and backup collection must remain opt-in.
- [ ] Confirm no SNMP OIDs are queried from `hrStorageTable`/`hrDeviceTable`.
- [ ] Observe 30–60 minutes of polling and record unsupported-items count and exact error category.
- [ ] Confirm `sp.mib.wg.peer.bps.*` graph uses counter **change per second**, not raw byte total; handshake remains raw until verified.
- [ ] Confirm no user sessions, VPN endpoint addresses, secrets or personally identifiable log data are retained.
- [ ] Confirm Zabbix graphical status mappings: services, IPsec, OpenVPN, AV and WireGuard.
- [ ] Record sanitized firmware revision, test date, number of detected interfaces/peers, and `Not supported` keys in an issue.


Offline GitHub Actions checks are **not** a real import or live-device test.

## Per test build

- Zabbix version/build: ____
- Securepoint UTM firmware/build: ____
- Hardware or VM (avoid serial numbers): ____
- SNMPv3 mode: ____
- Test host created separately: yes/no
- Template import: PASS/FAIL + first error text
- LLD rules: active / unsupported / discovered counts
- Unsupported Items: list **item key and sanitized SNMP error** only
- Product/firmware scalars: verified / unavailable
- License and conntrack scalars: verified / unavailable
- Service states: maps verified / not verified
- IPsec state: maps verified / not applicable
- OpenVPN profile/client count: verified / not applicable
- WireGuard interface/peer status: verified / not applicable
- WireGuard transfer counters: monotonically increasing / other
- WireGuard last-handshake unit: **unknown until measured**
- Graphs: correct units and plausible change rates / needs work
- Trigger tests: only opt-in, deliberately controlled conditions
- Total generated Items and Not supported count: ____ / ____

## Safe feedback

Report only `snmp_oid`, Item key, expected/actual numeric types and error text (without client identifiers). Replace peer names, IP addresses, usernames, public keys, DNS names and serial numbers with placeholders. Never attach unsanitized SNMP walks, PCAPs or screenshots with real client information.

## What CI does not establish

CI does not speak to Securepoint devices, does not test Zabbix's importer, and does not prove stable discovery indexing or trigger behavior. The acceptance checklist above must be completed before a release is called production-ready.

## Local diagnostic helper (privacy preserving)

From an authorized SNMPv3 monitoring machine, save a **private** numeric-OID walk. Keep it **out of GitHub**, because SNMP payloads may reveal addresses, VPN keys and users:

```bash
snmpwalk -On -v3 -l authNoPriv -u '<user>' -a SHA -A '<password>' '<utm-ip>' 1.3.6.1.4.1.28553 > /tmp/securepoint-private.snmp
python tools/analyze_snmpwalk.py /tmp/securepoint-private.snmp --json
```

For deployments using `authPriv`, adapt your flags. Be aware shell command lines and histories can expose credentials. Prefer an SNMP config file with restrictive permissions where possible. Script output contains only **counts** of rows and missing fields, not their values or indices; review before sharing anyway.

This checks OID coverage, **not** whether the returned status value means healthy, whether the manufacturer implements it correctly, or whether Zabbix imported the template.

## v5.5 interface acceptance (additions)

- [ ] Verify full interface list in the new **Interfaces** page, including WAN/LAN/WG/VLAN when they actually exist; carousel 1/6 means six graphs were detected, not one interface.
- [ ] Verify admin/oper status names from value maps and compare with Securepoint GUI.
- [ ] Verify ifHighSpeed zero/unknown for virtual interfaces is not presented as a real physical link capacity.
- [ ] Compare own 64-bit bps graph against generic SNMP parent traffic graph per interface.
- [ ] Confirm in/out packet errors and discards are rates, not cumulative counters; no unsupported IF-MIB columns for configured interfaces.
- [ ] Keep original `Network Generic Device by SNMP` linkage and its dashboard untouched unless deciding on a separate shared-template removal plan.

## Standalone v5.6 acceptance checklist

- [ ] Confirm no `templates` linkage on the new standalone template; technical name `Securepoint UTM Standalone v5.6 by SNMP`.
- [ ] Import independently as **new template**, without deleting the existing one. Confirm dashboard references resolve.
- [ ] On host Firewall, **Unlink and clear** old Unified v5.5 and generic (only if directly linked); save; then link v5.6 in second update to avoid duplicate item keys.
- [ ] Confirm generic **Network interfaces** dashboard disappears on this host, but the generic template remains available elsewhere.
- [ ] Ensure SNMPv3 host interface stays intact and newly collected uptime/CPU/RAM/IF-MIB items report actual values.
- [ ] Confirm 15-minute no-data trigger and opt-in interface-link-down macros; no false alerts for intentional VPN disconnects.
- [ ] Confirm interface metadata Items remain disabled unless manually verified.
- [ ] Confirm legacy vendor firmware/license OIDs are still pending live validation.

## RC1 live validation progress (2026-10-21)

The second batch of user screenshots confirms that **all six interface states/link-speed values, interface RX/TX rates and graphs, error/discard rates and graphs, CPU/RAM/TCP/UDP, manufacturer firmware and license fields, and firmware-mismatch Zabbix Problem** are working on the initial Securepoint test host. See [RC1 release report](RELEASE_CANDIDATE_1.md) for precise evidence and exceptions.

Remaining work, in recommended test order:

1. Open Host → Latest data, filter `Not supported` in Host Items and record **counts** and anonymized item keys (never paste credentials or customer addresses).
2. Use **one known-active WireGuard peer**: verify down→connected status, last handshake, and transfer counters against the Securepoint UI.
3. Verify IPsec and OpenVPN LLD only if the device is configured with them; `0 clients` / an empty IPsec list may be legitimate.
4. Review antivirus patterns and core service states against the Securepoint UI, especially services intentionally disabled.
5. Check **firmware mismatch recovery** during a legitimate future firmware upgrade, not an artificial production outage.
6. In a **disposable Zabbix test host or isolated lab**, exercise license warning 30d, critical 7d and zero-day semantics, 15m SNMP no-data and recovery, and opt-in link-down behavior; never change a production firewall/license to simulate an alert.
7. Verify configured **Action/Media** sends alerts to an intended recipient; Zabbix Problems alone demonstrates trigger evaluation, not delivery.
8. After 24h, inspect unsupported Items, LLD count stability, polling latency, and persistent nonzero LAN inbound discards. Record known-good baselines before setting drop thresholds.
