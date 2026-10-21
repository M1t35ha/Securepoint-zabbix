# Troubleshooting — Standalone RC1

Use [the current YAML](../templates/securepoint-utm-standalone-v5.6.yaml), [OID reference](OID_REFERENCE.md) and [test checklist](TESTING.md). The **old v2/v3 discovery floods and v4/v5 YAML schema conflicts** are development history, not recommended configurations.

| Symptom | Interpretation / next action |
| --- | --- |
| `No Such Instance currently exists at this OID` | Device does not expose the requested instance. Check the exact numeric OID **in current YAML**, optional feature availability and real SNMP index. Do not automatically add `.0` to Securepoint vendor OIDs. |
| Firmware/license shows `No data` | In current RC1 the vendor addresses omit a trailing `.0`; verify Items → Info and direct read-only SNMP response. Those values worked on one device; not guaranteed on others. |
| `Cannot evaluate function: not enough data` | A calculated/rate Item lacks valid source samples; inspect its SNMP source first. |
| RX/TX, errors or discards empty just after import | `CHANGE_PER_SECOND` needs at least two polls. Wait for next samples; if still empty, inspect Item errors or virtual-interface availability. |
| Interface link speed says 0 Mbps | Can be normal for virtual/VPN interfaces without a physical link speed. |
| 6 interfaces, but graph carousel shows one | Zabbix graph-prototype widget shows **one interface at a time** with paging. The Interfaces Top Items tables show all discovered instances simultaneously. |
| Interface Up, WireGuard peer Disconnected | Different layers: the Linux interface can be up without a recent connected peer/handshake. |
| Firmware-update Problem persists | Compares two **different version strings**; verify manufacturer-reported available build, active update channel and genuine recovery. This is not semantic-version ordering. |
| License 90 days left but no alert | Default warning window is 30 days, critical 7 days. External email/Teams delivery requires Zabbix Media and Action configuration. |
| Unexpected service Down | Some services can be intentionally off. Compare with UTM GUI before enabling service-level alarms. |
| Hundreds of unsupported LLD objects | Check if a legacy template remains attached. RC1 deliberately excludes broad `hrStorage` and `hrDevice` inventories. |
| Missing `Network interfaces` host dashboard | Expected! Standalone RC1 has its own **Interfaces** page and intentionally no parent generic SNMP template. |
| Dashboard import complains of external graph prototype | Use current RC1 export. Earlier v5.1 linked to a parent template graph prototype and could not import; this was removed. |

## Quick debugging procedure

1. Identify the exact **Host → Items → Not supported** key or graph name and error text.
2. Determine whether the metric is a vendor scalar, LLD table column, or rate/calculated item.
3. Verify real numeric OID and index on the device, with restricted, read-only SNMPv3.
4. Compare any enumerated state or tunnel status with the Securepoint GUI.
5. Make the smallest template change and test in a separate Git branch; **keep existing UUIDs / item keys stable** if fixing an existing Item.
6. Re-import with **Update existing** and **Delete missing OFF**. Do not relink old experimental templates unless performing a deliberate rollback.

For historical issues (v2/v3 incorrect storage, `discovery_rules.tags` import failure, UUIDv4 errors and duplicate CPU graphs), see the [development history](../CHANGELOG.md). Never publish credentials, public management IPs, customer names, license IDs or raw SNMP dumps.
