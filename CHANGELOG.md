# Changelog

The **public project release version** is now `v1.0.0-rc.1`. Earlier internal Zabbix template revisions (`v4`, `v5.1` through `v5.6`) were iterative prototypes, **not** published stable releases.

## [v1.0.0-rc.1] — 2026-10-21 (current)

- Based on **Standalone v5.6**, with no dependence on `Network Generic Device by SNMP`.
- Independent SNMP interface discovery, 64-bit traffic rates, errors/discards, admin/oper status and speed; four Host Dashboard pages.
- Manufacturer-MIB VPN/service/firmware/license Items; conservative opt-in interface alarms and SNMP outage monitoring.
- **Observed in Zabbix 8.0:** import/link, six interface rows, CPU/RAM/network graphs and rate values, installed/available firmware, license type/days, firmware-difference Problem.
- Still **release candidate**: connected VPN peer transitions, selected service/AV behavior, license warning thresholds, alert delivery and multi-day polling remain unverified.

### Development history (preserved, not install targets)

| Internal snapshot | Key change | Archive |
| --- | --- | --- |
| v4 | Manufacturer-MIB mappings, cautious discovery; first isolated vendor template | [v4 YAML](https://github.com/M1t35ha/Securepoint-zabbix/blob/feature/utm-v5-unified/templates/securepoint-utm-mib-v4.yaml) |
| v5 | Unified vendor SNMP + TCP/UDP/IP and system measurements | [v5 YAML](https://github.com/M1t35ha/Securepoint-zabbix/blob/feature/utm-v5-unified/templates/securepoint-utm-unified-v5.yaml) |
| v5.1 | First 3-page Dashboard; removed invalid inherited graph prototype reference | [v5.1 YAML](https://github.com/M1t35ha/Securepoint-zabbix/blob/feature/utm-v5-unified/templates/securepoint-utm-unified-v5.1-dashboard.yaml) |
| v5.2 | Vendor scalar OID fixes, interface traffic dashboard, corrected empty widgets | [v5.2 YAML](https://github.com/M1t35ha/Securepoint-zabbix/blob/feature/utm-v5-unified/templates/securepoint-utm-unified-v5.2-dashboard.yaml) |
| v5.3 | Denser dashboard, compact real-data status panels | [v5.3 YAML](https://github.com/M1t35ha/Securepoint-zabbix/blob/feature/utm-v5-unified/templates/securepoint-utm-unified-v5.3-dashboard.yaml) |
| v5.4 | Firmware and license cards, mismatch and 30/7-day triggers | [v5.4 YAML](https://github.com/M1t35ha/Securepoint-zabbix/blob/feature/utm-v5-unified/templates/securepoint-utm-unified-v5.4-firmware-license.yaml) |
| v5.5 | Separate Interfaces page with traffic, link status, speed, errors/discards | [v5.5 YAML](https://github.com/M1t35ha/Securepoint-zabbix/blob/feature/utm-v5-unified/templates/securepoint-utm-unified-v5.5-interfaces.yaml) |
| v5.6 | Fully standalone template; removed generic parent, independent availability and interface monitoring | **[RC1 template](templates/securepoint-utm-standalone-v5.6.yaml)** |

### Why we keep only one template in RC1

Earlier versions were intentionally experimental and some had known schema, LLD or graph conflicts. Keeping them beside the current build confused new users and made CI slower. **Their commits were not rewritten.** All prior snapshots and version-specific design notes remain in the preserved development branch [`feature/utm-v5-unified`](https://github.com/M1t35ha/Securepoint-zabbix/tree/feature/utm-v5-unified), as well as the Git commit history and archived [development PR #5](https://github.com/M1t35ha/Securepoint-zabbix/pull/5).

Use the current [RC1 template](templates/securepoint-utm-standalone-v5.6.yaml) for testing, not historic YAML files. Previous raw customer-specific Zabbix data was never intended to be stored in this repository.

## Release process

`release/1.0.0-rc.1` is the integration/test branch, reviewed via [PR #6](https://github.com/M1t35ha/Securepoint-zabbix/pull/6). Once the [acceptance gates](docs/ROADMAP.md) pass, merge to `main`, choose a project license with the owner, and publish a stable release/tag. Changes requiring a new tested candidate should be recorded as `rc.2` instead of silently altering the published installer.
