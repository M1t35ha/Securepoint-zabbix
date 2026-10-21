# Dashboard v5.2 — corrective iteration (test-stage)

## What was observed on the live Zabbix screen (2026-10-21)

- Working: dashboard CPU (about 2%), memory (~33%), process count (around 307), host uptime, MIB-II TCP/UDP and per-interface generic traffic charts.
- Not yet supplying values: vendor firmware, remaining license days, conntrack and HA cards.
- WireGuard throughput flat at 0 B/s and OpenVPN connected clients at 0: may be **legitimate inactivity**, not proof of broken polling.
- These are screenshots, **not** a raw SNMP walk; do not claim live vendor scalar compatibility until verified.

## Corrections

1. Fixed **13 Securepoint-specific scalar OIDs** by removing the trailing `.0` that was added in v4/v5 despite the older known-working vendor template and official Securepoint examples using base addresses without `.0`. Retained the original keys and UUIDs for continuity; no alarm behavior changed.
2. Added two conservative standard `system` OIDs for hostname and device description to ensure the overview can show identity even if proprietary OIDs are absent.
3. Rebuilt the dashboard so **Overview** emphasizes confirmed CPU, RAM, processes, uptime and TCP history. Firmware/license and optional conntrack appear on the VPN & Security tab instead of occupying the primary status bar.
4. Added targeted `ifName` discovery and **only two IF-MIB 64-bit counter Items per interface**, transformed from cumulative octets into bits/s. This deliberately duplicates a tiny part of inherited generic interface monitoring because Zabbix does not permit template dashboard graph references to a linked parent's graph prototypes. Avoid reintroducing the noisy hrStorage/hrDevice sweeps.
5. Added `Top items` tables for discovered service, WireGuard, IPsec and antivirus statuses. These require live acceptance testing; a profile may be intentionally inactive.

## Acceptance: do not declare fixed just because import works

1. Import `templates/securepoint-utm-unified-v5.2-dashboard.yaml` with **Update existing / Create new** enabled and **Delete missing** disabled.
2. Inspect the overview and the status of newly created `sp.dashboard.interface.*` items. It may take 2+ samples for per-second graphs to populate.
3. Specifically inspect `sp.mib.firmware.current`, `sp.mib.license.days` and `sp.mib.conntrack.current` under **Monitoring → Latest data**. If no data, inspect the Item information tooltip for the precise error.
4. Compare SNMPv3 `get[1.3.6.1.4.1.28553.1.2.7]` with `get[1.3.6.1.4.1.28553.1.2.7.0]` as read-only checks using the same SNMPv3 Zabbix interface. Do not reveal SNMP passwords or write full walks into public issues.
5. If both forms fail, enumerate actual returned OIDs using a secured numeric snmpwalk of `1.3.6.1.4.1.28553.1.2`, and adjust only verified Items in a new PR.
6. Keep existing production template linkage unchanged until v5.2 tests pass. Do not Unlink and clear history; do not delete unrelated LLD objects.
7. If the new Top-items dashboard widgets cause an importer error, record the exact widget type/field and fix the YAML schema rather than deleting working monitored Items.

## Expected coverage

- Overview: six headline cards; CPU and RAM gauges; Problems; history graphs; interface throughput graph prototypes; service and WireGuard status summaries.
- Network: 64-bit interface traffic panel plus TCP/UDP/IP counters, rates, and diagnostic graphs.
- VPN & Security: WireGuard/IPsec/OpenVPN and antivirus statuses; tunnel/client graphs; firmware/license and optional conntrack.

The template is not production-certified and no integration with a live Zabbix API has been performed. CI checks can confirm YAML structure only.
