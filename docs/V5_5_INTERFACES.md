# v5.5 — Interface monitoring, dashboard consolidation

**Candidate:** [securepoint-utm-unified-v5.5-interfaces.yaml](../templates/securepoint-utm-unified-v5.5-interfaces.yaml)

## Why the old dashboard shows only one graph

The existing **Network interfaces** dashboard comes from the linked, official **Network Generic Device by SNMP** template; its graph-prototype widget displays one discovered interface at a time, with a carousel (e.g. 1 / 6). It is **not** evidence that the other interfaces were not found.

Our own **Securepoint UTM | Command Center** now has four tabs:
1. Overview — CPU, memory, uptime, processes, tunnel/service state summaries, live traffic.
2. Network — TCP/UDP/IP troubleshooting.
3. **Interfaces (new)** — tables of **all** discovered interfaces at once, plus per-interface graph carousels.
4. VPN & Security — VPN/service status, vendor firmware and license (when SNMP supported).

## New metrics

All are indexed using existing `ifName` discovery under IF-MIB; the LLD rule uses `{$SP.DASHBOARD.IF.MATCHES}` to limit eligible interfaces.

| Item group | SNMP OID column | Interpretation |
| --- | --- | --- |
| RX/TX throughput | `ifHCInOctets` / `ifHCOutOctets` | Existing 64-bit octet counters; bytes/s converted to **bits/s** |
| Operational state | `ifOperStatus` — `1.3.6.1.2.1.2.2.1.8` | Up, Down, Testing, Unknown, Dormant, Not Present, Lower Layer Down |
| Administrative state | `ifAdminStatus` — `1.3.6.1.2.1.2.2.1.7` | Enabled, Disabled, Testing |
| Link speed | `ifHighSpeed` — `1.3.6.1.2.1.31.1.1.1.15` | Mbps; may be zero or nonsensical on virtual/VPN links |
| RX/TX errors | `ifInErrors` / `ifOutErrors` — `1.3.6.1.2.1.2.2.1.14/.20` | Cumulative packet-error counters converted to events/s |
| RX/TX discards | `ifInDiscards` / `ifOutDiscards` — `1.3.6.1.2.1.2.2.1.13/.19` | Cumulative discards converted to events/s |

Seven new item prototypes and one error/discard graph prototype per interface; total nine metrics per eligible interface including existing RX/TX. Intervals range from 3m to 30m. This is a targeted subset, **not** the old problematic `hrStorage/hrDevice` all-device discovery.

Default filter includes LAN/WAN/DMZ, vlan, eth/en, WLAN, WireGuard, tunnel, PPP and bridge types. For additional actual `ifName` values, override `{$SP.DASHBOARD.IF.MATCHES}` in **Data collection → Hosts → Firewall → Macros**. Do not use `.*` on a device with hundreds of dynamic interfaces without assessing SNMP load. It can take two samples for rate calculations to appear.

## Can we remove the separate "Network interfaces" Host Dashboard?

**Yes, but this requires a separate Zabbix configuration change, not just an import of the Securepoint YAML.** That dashboard is owned by the linked `Network Generic Device by SNMP` template and is inherited by hosts. Our child template cannot selectively suppress its parent's dashboards while retaining normal template inheritance.

**Safer default: keep the parent linked and ignore the old dashboard**. It continues collecting existing interface counters, triggers and graphs, while the new **Interfaces** page inside Command Center provides the consolidated view.

If **all** hosts using the generic template should lose that dashboard: export/back up the generic template, open **Data collection → Templates → Network Generic Device by SNMP → Dashboards**, and delete **Network interfaces** (dashboard only; do not delete the template, LLD or Items). This affects every host inheriting that template and may be overwritten by an official template update. Confirm other host impact first.

If the change should affect **only Firewall**, do **not** edit the shared parent. A per-host variant requires a separately maintained copy without this dashboard, or careful parent unlinking with **Unlink (never Unlink and clear)** while preserving Items. That changes inheritance, macros and update behavior; first export and test in a separate host/template. **Do not perform this as part of the v5.5 import automatically.**

Zabbix documentation: [Template nesting](https://www.zabbix.com/documentation/8.0/en/manual/config/templates/nesting) · [Linking and unlinking](https://www.zabbix.com/documentation/8.0/en/manual/config/templates/linking).

## Install/acceptance

1. Back up the current Securepoint template and verify its linked parent still contains interface monitoring.
2. Import v5.5 with **Update existing** and **Create new** enabled, **Delete missing disabled**.
3. Open **Monitoring → Hosts → Firewall → Dashboards → Securepoint UTM | Command Center → Interfaces**.
4. Wait for LLD (up to 1h, or safely execute its discovery rule once), and wait for at least two samples for rate metrics.
5. Verify all known LAN/WAN/WireGuard/VLAN interfaces are listed; confirm names/indexes and compare RX/TX to existing Zabbix **Network interfaces** graphs.
6. Inspect **Data collection → Hosts → Firewall → Items** for any unsupported status/speed/error/discard OID. Virtual interfaces may not implement all optional IF-MIB fields; remove only failing fields after actual evidence.
7. Never delete parent template or old Items to make the UI cleaner; avoid **Unlink and clear** and accidental historical data loss.

No live Zabbix importer or real SNMP access is available to this repository's CI. YAML validation alone is not device certification.
