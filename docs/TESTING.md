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
