# Acceptance test checklist

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
