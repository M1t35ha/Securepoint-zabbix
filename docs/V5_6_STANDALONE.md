# Standalone Securepoint UTM v5.6 — migration guide (Zabbix 8.0)

**Template:** [securepoint-utm-standalone-v5.6.yaml](../templates/securepoint-utm-standalone-v5.6.yaml)

This is a **separate technical template** named `Securepoint UTM Standalone v5.6 by SNMP`; it has new UUIDs and does **not** inherit `Network Generic Device by SNMP` (or any other template). This avoids the redundant inherited **Network interfaces** host dashboard. The official generic Zabbix template stays installed for any unrelated hosts; we are only detaching it from the Securepoint host.

## What is inside

- Existing standard Securepoint/Net-SNMP metrics from v5.5: CPU, RAM, process count, uptime, TCP/UDP/IP/ICMP.
- Official Securepoint MIB features: IPsec, WireGuard, OpenVPN, AV, services, firmware and license, where those OIDs are supported on the current firmware.
- Built-in, independent IF-MIB `ifName` discovery. Per eligible interface: 64-bit RX/TX bits/s, admin/oper status, ifHighSpeed Mbps, errors/s and discards/s.
- Existing own Dashboard: **Securepoint UTM | Standalone Command Center** (Overview, Network, Interfaces, VPN & Security).
- Standard `sysObjectID.0` and `sysUpTime.0` standalone system Items.
- **15 minute SNMP no-data alarm** (enabled by `{$SP.SNMP.NODATA.ALERT}=1`), using known-good `sp.dashboard.uptime` which returns OS uptime through HOST-RESOURCES-MIB.
- Optional link-down alarm, **off by default**, opt-in for important always-on interfaces with `{$SP.IF.ALERT:"LAN1"}=1`. Uses operational/admin states and 10 minute window.
- Optional disabled per-interface alias (`ifAlias`) and IANA type metadata Items. Disabled until device responses are verified.

No large hardware/storage discovery, no SNMP passwords, no VPN private keys.

## Migration — old history is not required

**Do not link v5.5 and v5.6 simultaneously on the same host**: their Items have intentionally overlapping keys.

1. Download and **import v5.6 first** under **Data collection → Templates → Import** with **Create new** enabled and **Delete missing** disabled. Because the template has a **different name and UUID**, it will coexist as an imported template but is not yet linked to any host.
2. Export the existing host and old templates as a configuration backup (even if old history is unimportant); record any host-specific SNMPv3 authentication, custom macros, interface-selection filters, and Action scope.
3. Open **Data collection → Hosts → Firewall**. For **Securepoint UTM Unified v5 by SNMP** click **Unlink and clear**. Also clear any old v2/v3 Securepoint experimental templates that are still linked and conflict. If **Network Generic Device by SNMP** is also linked **directly** to this host, Unlink and clear it too. When it was only inherited from v5.5, clearing the old template should remove that inherited monitoring as well.
4. Click **Update** to save the removal **before attempting to link v5.6**. This two-step operation avoids duplicate key/graph conflicts.
5. Reopen the host, select **Securepoint UTM Standalone v5.6 by SNMP**, then **Update**. The existing SNMPv3 host interface remains; confirm correct SNMP interface/address/authentication after the update.
6. Open Monitoring → Hosts → Firewall → Dashboards → **Securepoint UTM | Standalone Command Center**. The inherited **Network interfaces** Dashboard should be absent when no other linked template provides it.
7. Run or wait for the interface LLD (default 1h), wait two samples for per-second graphs, and verify SNMP uptime, interface names, firmware/licence when supported, and the operational/admin status value maps.
8. Under **Monitoring → Latest data / Data collection → Hosts → Items**, review unsupported items. Virtual/VPN interfaces may legitimately not implement all optional IF-MIB columns; no live-device compatibility claim is made by CI.
9. Verify firmware and license SNMP Items return real data before depending on license-renewal / update notifications. Triggers are not a substitute for an Action/Media notification configuration.

**Consequences of Unlink and clear:** it deletes old template-derived host items/triggers/graphs and their collected history, including old generic interface measurements. New items start collecting afresh. The actual Securepoint device, its SNMP configuration and Zabbix SNMP host interface are not deleted. The generic template **itself** is not deleted globally.

## Rollback

If the standalone import or host monitoring fails, Unlink and clear **Standalone v5.6** from this host and link the prior **Unified v5 by SNMP** (or import v5.5 again from the repository) to recover the previous configuration. Historical measurements cleared during the migration cannot be recovered by re-linking.

## What to validate on real device

- Import/host link to Zabbix **8.0** completes.
- There is **no parent template** listed on the standalone template.
- The host has no inherited **Network interfaces** dashboard once the old nested template is removed.
- Interfaces page discovers the expected LAN/WAN/VLAN/WireGuard links; newly collected counters match physical traffic.
- Service/HA/VPN state mappings agree with the Securepoint GUI.
- SNMP no-data alert triggers only when data is missing; do not mistake SNMP polling failure for total network outage.
- Firmware/license vendor OIDs still require live verification; **No data** can reflect unsupported OIDs, not a valid/invalid license.

Zabbix official guidance: [Linking / Unlinking](https://www.zabbix.com/documentation/8.0/en/manual/config/templates/linking) and [Template nesting](https://www.zabbix.com/documentation/8.0/en/manual/config/templates/nesting).

This file is a lab/test candidate, **not** certified against a live Zabbix instance. The GitHub CI validator only checks structural consistency.
