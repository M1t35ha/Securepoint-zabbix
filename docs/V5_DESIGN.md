# Unified v5 design (experimental, not imported)

## Purpose and source of truth

`templates/securepoint-utm-unified-v5.yaml` is the integration candidate. The previous `securepoint-utm-mib-v4.yaml` is retained unchanged as a reference baseline; older v2/v3 all-in-one experiments are **not** shipped. The v5 template has a different technical name and unique object UUIDs to permit safe side-by-side testing.

## What is inherited, what is new

| Component | Source | Collection policy |
| --- | --- | --- |
| Inventory, firmware and license | SECUREPOINT-MIB (manufacturer) | SNMP scalar values; alert opt-in |
| Conntrack count/limit | SECUREPOINT-UTM MIB | Numeric count/limit graph; zero-safe alert opt-in |
| Applications/services | Securepoint MIB LLD | Status/flags; per-service alarm opt-in |
| IPsec tunnels | Securepoint MIB LLD | State + subnet count; per-profile alarm opt-in |
| OpenVPN profiles | Securepoint MIB LLD | State + client count; no session/user information |
| Antivirus patterns | Securepoint MIB LLD | State + timestamps |
| WireGuard interfaces and peers | Securepoint MIB LLD | State, counts, ports, raw handshake, RX/TX counters, B/s graphs; alarms opt-in |
| System resource overview | HOST-RESOURCES-MIB scalar | RAM, process and logged-in-user counts; avoids broad storage/device scans |
| TCP/UDP/IP/ICMP diagnostics | MIB-II/RFC standard scalar | Curated rates and graph panels |
| Network interface traffic and availability | Linked `Network Generic Device by SNMP` | Do **not** duplicate interface discovery |
| Per-core CPU | hrProcessorLoad-only LLD | Disabled until queried on target firmware |
| HA details, IPsec subnets, backup inventory | Securepoint MIB | Disabled until feature/API validation |

The manufacturer MIB files are not published in GitHub. Only independently written OID references, template definitions and tests are published.

## Deliberate exclusions

* No `hrStorage` / `hrDevice` blanket discovery: previous import produced hundreds of unsupported objects.
* No SWAP division or calculated percentage with a potential zero denominator.
* No WireGuard endpoint address, public key, IP whitelist, VPN username, user-session history, mailqueue recipients, Fail2Ban IP lists, or raw alert bodies.
* No SSH, HTTP API or Syslog collection **until independently secured and tested**. These are separate optional future integrations, not promised working parts of v5.
* No unverified handshake age expression: manufacturer describes a time value but unit/epoch still needs live confirmation.
* No unconditional tunnel alarms: mobile/on-demand clients can legitimately be disconnected.

## Remaining gates before release

1. CI validation of all YAML files, UUIDs, references, basic OID syntax and exclusions.
2. Manual Zabbix 8.0 import to a disposable test host (never production first).
3. Confirm manufacturer OIDs via sanitized read-only SNMPv3 queries.
4. Resolve unsupported items and confirm graphics are rates, not ever-growing counters.
5. Verify state maps against firewall UI and enable only always-on tunnel alerts by host macros.
6. Record firmware/build, LLD counts and anonymized successes/failures in `docs/TESTING.md`.

**Offline validation is not device compatibility evidence.**
