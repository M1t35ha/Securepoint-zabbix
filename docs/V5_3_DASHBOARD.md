# v5.3 Dense dashboard iteration (2026-10-21)

The candidate file is [templates/securepoint-utm-unified-v5.3-dashboard.yaml](../templates/securepoint-utm-unified-v5.3-dashboard.yaml).
It replaces the **dashboard layout** while retaining the same Zabbix template name, item keys, LLD configuration, existing graphs, mappings, optional alerts and dashboard UUIDs from v5.2.

## Changes based on screenshots

- **46 widgets across 3 pages**: Overview (18), Network (14), VPN & Security (14).
- Cards for CPU, RAM, process count and TCP now show a **value, label and six-hour sparkline**, using Zabbix Item value's built-in `show` and `sparkline` controls.
- Removed large empty panels and repeated raw service flags, WireGuard `raw state` and undocumented counters from summary tables. The source data still exists in Latest data for diagnostics.
- Overview focuses on CPU/RAM gauges, active interface throughput, TCP/UDP trends, filtered service and WireGuard status, and current problems.
- Network summarizes IF-MIB 64-bit per-interface receive/transmit rates and TCP/UDP/IP counters. Interface discovery remains filtered via `{$SP.DASHBOARD.IF.MATCHES}`.
- VPN page gives narrow status tables for WireGuard peers/interfaces, IPsec tunnels, OpenVPN client count, antivirus state, plus graph prototypes.
- Firmware, license, conntrack and HA vendor scalars are **not advertised as working** because real SNMP support has not been verified. They remain in Latest data rather than occupying headline dashboard slots.
- **No additional SNMP items or LLD rules** added over v5.2; no new broad walks.

## Caveats

This is a layout improvement, not proof that all manufacturer SNMP data is available. Service code `2` is mapped to `Down`, but some services (bird2, bird6, ctproxy, cvpn) may be intentionally stopped. Before configuring alarms, compare them to the UTM GUI. A WireGuard throughput of 0 B/s or OpenVPN clients 0 can be normal.

The v5.3 host dashboard imports on top of the same template via **Update existing**, with **Delete missing disabled**. Keep production history and existing host linkage; do not Unlink and clear for a dashboard redesign.

**Acceptance**: successful template import in Zabbix 8.0, verify sparkline labels, and verify that top-item filters show statuses rather than raw flags. Run the attached offline structural validator before import. Follow up with user screenshots; if a widget parser error appears, do not alter working Items to make a UI widget import.
