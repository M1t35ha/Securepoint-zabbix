# Securepoint manufacturer OID reference

These are our **own selected OID notes**, transcribed from the manufacturer modules `SECUREPOINT-MIB.mib` and `SECUREPOINT-UTM.mib` (reported `LAST-UPDATED 202505270000Z`). The manufacturer files are not redistributed here. Decimal OIDs have been retained for unambiguous troubleshooting.

| Component | Name / numeric OID | Meaning |
| --- | --- | --- |
| Product | `1.3.6.1.4.1.28553.1.1.0` | Product name |
| Installed firmware | `...28553.1.2.7.0` | Current firmware |
| New firmware | `...28553.1.2.8.0` | Reported available firmware |
| License | `...28553.1.3.3.0/.4.0/.5.0` | Type / maximum users / days remaining |
| Conntrack | `...28553.2.1.10.1.0/.2.0` | Maximum / active tracked connections |
| Services | `...28553.2.1.1.1.1.2/.3` | Name / state (indexed) |
| IPsec | `...28553.2.1.2.1.1.2/.3` | Tunnel name / state (indexed) |
| OpenVPN | `...28553.2.1.3.1.1.2/.3/.4` | Name / state / client count |
| Antivirus | `...28553.2.1.5.1.1.2/.5` | Engine name / update state |
| WireGuard interface | `...28553.2.1.11.1.1.2/.4/.6/.7` | Interface name / state / port / peer count |
| WireGuard peers | `...28553.2.1.11.2.1.2/.3/.6/.7/.8` | Name / state / handshake raw / sent / received bytes |
| HA (optional) | `...28553.2.1.12.1.0` | Cluster enabled |

**Scalar vs table:** scalar OIDs use a final `.0`; table columns use a row index. WireGuard peers can have composite SNMP indices; LLD uses the actual `{#SNMPINDEX}`.

## Manufacturer enum meanings

| Item | Values |
| --- | --- |
| App/service | 1 Up, 2 Down, 3 Starting, 4 Error, 5 Should Down, 6 Should Up, 7 Unconfigured, 8 Disabled, 9 No Service |
| IPsec | 0 Unknown, 1 Up, 2 Down |
| OpenVPN | 1 Connecting, 2 Assign IP, 3 Add Routes, 4 Connected, 5 Reconnecting, 6 Exiting, 7 Unknown |
| WireGuard | 0 Disconnected, 1 Connected, 2 Unknown, 3 Deleted |
| AV update | 1 OK, 2 Failed, 3 In progress |
| HA enabled | 0 Disabled, 1 Enabled |

The MIB defines the **meaning** of a number, but only a real SNMP response confirms that a particular instance exists. The WireGuard handshake OID's time base/units are *not* assumed in this project.
