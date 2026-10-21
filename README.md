# Securepoint UTM monitoring for Zabbix

> **Current release candidate: v1.0.0-rc.1** · Standalone template v5.6 · Securepoint NextGen UTM 14.x · tested on Zabbix 8.0

[![Template validation](https://github.com/M1t35ha/Securepoint-zabbix/actions/workflows/validate.yml/badge.svg)](https://github.com/M1t35ha/Securepoint-zabbix/actions/workflows/validate.yml)

**[Download the Zabbix template](templates/securepoint-utm-standalone-v5.6.yaml)** · **[Install / migrate](docs/INSTALL.md)** · **[RC1 test evidence](docs/RELEASE_CANDIDATE_1.md)** · **[Roadmap](docs/ROADMAP.md)** · **[Русская инструкция](docs/README_RU.md)**

Read-only, SNMP-based monitoring for Securepoint firewalls. The template is **standalone**: it does not require `Network Generic Device by SNMP` or a Zabbix Agent on the firewall. Export schema: Zabbix 7.0, successfully imported on one Zabbix 8.0 RC installation.

## Features

| Monitoring | Status on initial UTM 14.x test device |
| --- | --- |
| Uptime, CPU, RAM, processes and TCP/UDP/IP counters | **Observed working** |
| IF-MIB interface discovery, status, speed | **Observed working** (six interfaces) |
| Per-interface 64-bit RX/TX rates, packet errors/discards and graphs | **Observed working** |
| Installed firmware and manufacturer-reported version | **Observed working** (version fields + firmware mismatch Problem) |
| License type and remaining days | **Observed working** (value collection only; renewal thresholds untested) |
| WireGuard peers and interfaces | Partial: peer `Disconnected` state observed; connected/handshake transition **untested** |
| OpenVPN, IPsec, antivirus and service states | Defined; feature-specific live validation **pending** |
| SNMP outage, link-down and license expiry alerting | Defined; complete end-to-end testing **pending** |

Four Host Dashboard pages: **Overview · Network · Interfaces · VPN & Security**. Interface LLD uses a configurable `{$SP.DASHBOARD.IF.MATCHES}` allowlist.

The first device reported ~1 inbound discarded packet/s on two LAN interfaces; treat this as an observation to investigate, not an established hardware fault.

## Quick install

1. Import `templates/securepoint-utm-standalone-v5.6.yaml` in **Data collection → Templates → Import**. Choose **Create new**; keep **Delete missing OFF**.
2. Create a host with a read-only SNMPv3 interface to the Securepoint (restrict polling to Zabbix server/proxy; prefer `authPriv` where supported).
3. Link **Securepoint UTM Standalone v5.6 by SNMP**. Do not link the old unified v5.x template to the same host (overlapping item keys).
4. Open **Monitoring → Hosts → [host] → Dashboards** and select **Securepoint UTM | Standalone Command Center**.
5. Wait for LLD and at least two samples for rate metrics. Examine **Latest data**, unsupported items, Problems and [the acceptance checklist](docs/TESTING.md).

Migrating a host with old experimental templates? Follow the [two-step migration guide](docs/INSTALL.md) before linking this one. `Unlink and clear` discards the old items/history.

## Release status and development

RC1 has **real UI evidence for the core system/network metrics and firmware/license value collection**, not a complete cross-firmware acceptance test. We will not label it stable until alert thresholds, VPN transitions, SNMP availability and long-running polling are checked.

- [RC1 release notes and evidence](docs/RELEASE_CANDIDATE_1.md)
- [Remaining work](docs/ROADMAP.md) · [Test procedure](docs/TESTING.md)
- [Selected manufacturer OIDs](docs/OID_REFERENCE.md) · [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Evolution and older template versions](CHANGELOG.md) · [Community research](docs/COMMUNITY_RESEARCH.md)
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)

**History policy:** only one installable current YAML is kept on the RC branch; prior v4/v5/v5.1–v5.5 files remain in Git commits and the archived development branch `feature/utm-v5-unified`. No history was rewritten.

## Attribution and licensing

Independent integration using standard SNMP and Securepoint manufacturer MIB definitions. **Not affiliated with or supported by Securepoint GmbH.** Official `SECUREPOINT-MIB.mib` and `SECUREPOINT-UTM.mib` are proprietary and are not redistributed; authorized users may obtain them from the [Securepoint portal](https://my.securepoint.de/). No credentials or customer configuration are included.

The repository owner has not selected an open-source license; **public GitHub access does not by itself grant permission to reuse the source under an OSI license**.
