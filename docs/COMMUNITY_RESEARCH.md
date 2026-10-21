# Community solutions and provenance

Research date: 2026-10-21. We do not copy external third-party code into this repository. We use published design ideas and independently implement against manufacturer MIBs.

| Source | What is useful | Limitation / decision |
| --- | --- | --- |
| [Securepoint support: Zabbix SNMP MIB](https://support.securepoint.de/viewtopic.php?t=11806) | Manufacturer confirms **both** MIB modules must be loaded to translate symbols. Users report limited results from automatic mib2zabbix output. | Verify raw OIDs rather than generating every discovered entry automatically. |
| [Checkmk forum: Securepoint IPsec](https://forum.checkmk.com/t/snmp-check-fur-securepoint/29622) | Concrete IPsec tunnel table: vendor subtree `28553.2.1.2.1.1`, name column 2, state column 3; 0 unknown, 1 up, 2 down. | Checkmk plug-in is not a Zabbix template. Our IPsec status semantics also derive directly from official Securepoint MIB. |
| [cryptage21/wireguard-zabbix](https://github.com/cryptage21/wireguard-zabbix) | Per-peer LLD, transfer-rate graphs and reachability-alert architecture. | Depends on Linux Zabbix agent, sudo and `wg show`, so **not** directly usable on Securepoint; we use vendor SNMP OIDs instead. |
| [alkalim/wireguard-zabbix](https://github.com/alkalim/wireguard-zabbix) | Alternative example of WireGuard LLD + traffic collection. | GPL-2.0, Linux agent commands; no code imported. |
| [Zabbix official SNMP templates](https://www.zabbix.com/integrations/snmp) | Generic SNMP interface-discovery module. | Link existing `Network Generic Device by SNMP` rather than reimplement it. |
| [Zabbix low-level discovery docs](https://www.zabbix.com/documentation/8.0/en/manual/discovery/low_level_discovery) | Item prototypes, filters, overrides and graceful removal of lost resources. | We still need live table-index validation. |
| [Securepoint SNMP feature list](https://www.securepoint.de/en/for-companies/utm-firewall/firewall-functions) | Securepoint advertises IPsec/OpenVPN and application/network status through SNMP; Syslog is a separate channel. | Claims about product features do not guarantee every OID in every firmware/license. |
| [Securepoint SNMP slowdown discussion](https://support.securepoint.de/viewtopic.php?t=11871) | Real user observed unexpectedly slow broad SNMP detection on 14.0.2. | Favor minimal frequent polling and targeted LLD rather than aggressive walks. |

## Provenance rules

* Securepoint enums and vendor OID columns come from the official manufacturer MIB files, not from unreviewed forum guesses.
* Standard OS/network counters use IETF MIB-II and HOST-RESOURCES-MIB semantics.
* Community projects are background research, not bundled dependencies.
* Source licenses must be reviewed **before** borrowing implementation code. No proprietary MIB copies are committed.
