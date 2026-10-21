# Securepoint UTM SNMP OID reference — RC1

This is a **selected, independently written reference** for the current [Standalone v5.6 YAML](../templates/securepoint-utm-standalone-v5.6.yaml), not a complete manufacturer MIB. Manufacturer source modules are `SECUREPOINT-MIB.mib` and `SECUREPOINT-UTM.mib` (reported updated 2025-05-27); their copyrighted contents are **not redistributed**.

## Vendor scalar OIDs used in the tested template

| Measurement | SNMP OID as configured | Evidence |
| --- | --- | --- |
| Installed firmware | `1.3.6.1.4.1.28553.1.2.7` | Actual value observed |
| Vendor-reported new firmware | `1.3.6.1.4.1.28553.1.2.8` | Actual value observed |
| License type | `1.3.6.1.4.1.28553.1.3.3` | Actual value observed |
| License days remaining | `1.3.6.1.4.1.28553.1.3.5` | Actual value observed |
| Conntrack current / maximum | `1.3.6.1.4.1.28553.2.1.10.2` / `...10.1` | Present in YAML, not independently confirmed in latest screenshots |
| HA enabled | `1.3.6.1.4.1.28553.2.1.12.1` | Optional; not confirmed on test device |

**Important historical correction:** early v4/v5 documentation added `.0` to all manufacturer scalar addresses; that produced `No data` on the test system. The final vendor OID **expressions above omit the extra suffix** and returned values on the tested UTM. Standard scalar OIDs such as `sysUpTime.0` do use `.0`. Always follow the actual numeric OID tested with your SNMP agent rather than assuming one suffix rule applies everywhere.

## Manufacturer LLD table columns

| Component | Selected columns | Mapping / limits |
| --- | --- | --- |
| Service | `...28553.2.1.1.1.1.2/.3` | Name / service state |
| IPsec | `...28553.2.1.2.1.1.2/.3` | Name / tunnel state |
| OpenVPN | `...28553.2.1.3.1.1.2/.3/.4` | Name / state / connected-client count |
| AV | `...28553.2.1.5.1.1.2/.5` | Engine name / update state |
| WireGuard interfaces | `...28553.2.1.11.1.1.2/.4/.6/.7` | Interface name / state / port / peer count |
| WireGuard peers | `...28553.2.1.11.2.1.2/.3/.6/.7/.8` | Peer name / state / raw handshake / sent and received counters |

Table columns require an **actual instance index**; WireGuard peer indices can be composite. Do not create guessed instances from unrelated inventory discovery.

## Standard operating-system and interface OIDs

| Group | Numeric OID |
| --- | --- |
| Host uptime | `1.3.6.1.2.1.25.1.1.0` |
| sysObjectID / SNMP agent sysUpTime | `1.3.6.1.2.1.1.2.0` / `1.3.6.1.2.1.1.3.0` |
| Interface enumeration | `ifName: 1.3.6.1.2.1.31.1.1.1.1.{index}` |
| 64-bit RX/TX octets | `ifHCInOctets: ...31.1.1.1.6.{index}` / `ifHCOutOctets: ...31.1.1.1.10.{index}` |
| Admin / operational status | `...2.2.1.7.{index}` / `...2.2.1.8.{index}` |
| Link speed | `ifHighSpeed: ...31.1.1.1.15.{index}` (Mbps) |
| Input / output errors | `...2.2.1.14.{index}` / `...2.2.1.20.{index}` |
| Input / output discards | `...2.2.1.13.{index}` / `...2.2.1.19.{index}` |

RX/TX octets are transformed into **bits/s**, and packet counters into **events/s**. At least two polls are required to calculate rates.

## Manufacturer value meanings

| Metric | Values |
| --- | --- |
| Service | 1 Up, 2 Down, 3 Starting, 4 Error, 5 Should Down, 6 Should Up, 7 Unconfigured, 8 Disabled, 9 No Service |
| IPsec | 0 Unknown, 1 Up, 2 Down |
| OpenVPN | 1 Connecting, 2 Assign IP, 3 Add Routes, 4 Connected, 5 Reconnecting, 6 Exiting, 7 Unknown |
| WireGuard peer | 0 Disconnected, 1 Connected, 2 Unknown, 3 Deleted |
| AV update | 1 OK, 2 Failed, 3 In progress |

**Evidence distinction:** the initial test GUI confirms that a WireGuard peer state `Disconnected (0)` can be read and rendered; it does *not* confirm handshakes, active peer transitions or behavior across all firmware. For complete OIDs and item keys, consult the actual YAML.
