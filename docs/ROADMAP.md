# Roadmap

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
