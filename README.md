# Securepoint UTM → Zabbix

## Release Candidate 1 — v1.0.0-rc.1

**Current tested baseline:** [Securepoint UTM Standalone v5.6 YAML](templates/securepoint-utm-standalone-v5.6.yaml) · [RC1 release notes and open tests](docs/RELEASE_CANDIDATE_1.md).

This is the integration snapshot for testing: independent of the generic SNMP template, four host dashboard tabs, own network discovery, VPN/security monitoring, and firmware/license alert definitions. **Real Zabbix 8.0 import and six-interface state discovery have been observed; all SNMP metrics and alerts have not yet passed acceptance.** This branch is a release *candidate*, not the stable release.


[![Template validation](https://github.com/M1t35ha/Securepoint-zabbix/actions/workflows/validate.yml/badge.svg)](https://github.com/M1t35ha/Securepoint-zabbix/actions/workflows/validate.yml)

**[Русская инструкция](docs/README_RU.md)** · [Current tasks](https://github.com/M1t35ha/Securepoint-zabbix/issues)

Community-maintained, **experimental** monitoring template for Securepoint NextGen UTM 14.x and Zabbix 8.0 (7.0 export compatibility).

> [!WARNING]
> This is a test-stage project. The OID names, table definitions and enumerations were cross-checked against Securepoint's official MIB modules (2025-05-27), **but an MIB is not proof that an OID exists on every device/firmware**. This template has not yet passed a live-device acceptance test. Do **not** replace your production template without testing.

## New standalone candidate — v5.6 (no parent templates)

**[Download Standalone v5.6 YAML](templates/securepoint-utm-standalone-v5.6.yaml)** · **[Migration and rollback procedure](docs/V5_6_STANDALONE.md)**.

This completely self-contained template contains the Securepoint-specific metrics, the 4-page interface/security Dashboard, its own IF-MIB discovery and an SNMP no-data trigger. It does **not** link `Network Generic Device by SNMP`, so the inherited one-graph-per-interface Dashboard disappears from a host after old template linkage is cleared.

**Switching is a clean replacement:** import v5.6 as a **new** template, Unlink and clear v5.5 (and a separately linked generic parent, if present) from the Firewall host, save, then link v5.6. Do not link v5.5 and v5.6 concurrently, because they share item keys. **Unlink and clear erases old history**; the user has accepted that. Avoid deleting the generic template globally.

CI is structural only; live Zabbix import and firmware/licence OIDs still need verification.

## Latest development candidate — v5.5 (interfaces)

**[Download v5.5 YAML](templates/securepoint-utm-unified-v5.5-interfaces.yaml)** · [Interface monitoring & dashboard removal notes](docs/V5_5_INTERFACES.md) · [Russian installation notes](docs/README_RU.md).

The new **Interfaces** page in **Securepoint UTM | Command Center** lists all discovered LAN/WAN/VLAN/WireGuard/other eligible interfaces at once with operational/admin status, link speed, RX/TX, input/output errors and discards. Graph carousels remain available for in-depth traffic and packet-error analysis. The earlier firmware/license notification feature from v5.4 is retained.

The separate **Network interfaces** host dashboard comes from the inherited **Network Generic Device by SNMP** template. It cannot be removed just by editing this child dashboard. **Do not unlink-and-clear the generic template**: see [safe alternatives and shared-host impact](docs/V5_5_INTERFACES.md).

**Status:** experimental; CI checks structure and cannot prove device SNMP support or successful Zabbix 8.0 import. Keep `Delete missing` off on first import.

## Legacy v5 design (development branch)

**Recommended next version:** [Unified v5 YAML](templates/securepoint-utm-unified-v5.yaml) — combines official Securepoint MIB status monitoring with curated standard SNMP TCP/UDP/IP/ICMP, process/RAM metrics and graphs. This is a **release candidate, not a validated production template**. The v4 file remains in the repository for comparison and rollback.

- [Detailed scope and exclusions](docs/V5_DESIGN.md)
- [Existing community research and component provenance](docs/COMMUNITY_RESEARCH.md)
- [Acceptance test checklist](docs/TESTING.md)
- [Safe installation / side-by-side testing](docs/INSTALL.md)

**Do not import yet:** Offline CI checks structure but cannot demonstrate real UTM availability, correct access to every SNMP column, or the behavior of the Zabbix 8.0 importer.

## What it monitors

| Area | Source | Status |
| --- | --- | --- |
| Product and installed/available firmware | Securepoint SNMP | MIB-mapped; requires live verification |
| License limits and days remaining | Securepoint SNMP | MIB-mapped; requires live verification |
| Conntrack count and limit | Securepoint SNMP | MIB-mapped; requires live verification |
| Application/service states | SNMP LLD | MIB-mapped; requires live verification |
| IPsec tunnels | SNMP LLD | MIB-mapped; requires live verification |
| OpenVPN profiles and client counts | SNMP LLD | MIB-mapped; requires live verification |
| Antivirus update state | SNMP LLD | MIB-mapped; requires live verification |
| WireGuard interfaces, peers, counters | SNMP LLD | MIB-mapped; requires live verification |
| System uptime and interface traffic | Linked generic SNMP template | Depends on installed Zabbix template |
| HA detail, IPsec subnets, backup inventory | Optional | Disabled until validated |

Known limitations: a WireGuard handshake value is collected **raw** because its unit/epoch must be verified; no handshake-age alarm yet. Tunnel/service alerts are opt-in to avoid alarming on deliberately inactive instances.

## Quick start (test host first)

1. Ensure **Zabbix 8.0** and the official built-in `Network Generic Device by SNMP` template are available.
2. Import [the template](templates/securepoint-utm-mib-v4.yaml) under **Data collection → Templates → Import**. Do **not** select *Delete missing* on unrelated templates.
3. Make a **dedicated test host**, and configure its Securepoint IPv4 address and **SNMPv3 interface credentials in Zabbix**, not in this repository. Use only a read-only SNMP account, with access restricted to the Zabbix server/proxy.
4. Link the imported Securepoint template to the test host. Do not simultaneously link the generic template explicitly if it is already inherited.
5. Wait for discovery, then inspect **Latest data**, **Discovery**, and **Not supported** items. Record what exists on your actual firmware.
6. Enable per-tunnel and per-service alerts only after confirming their status semantics and whether they should stay online.

For more detail see [Installation](docs/INSTALL.md), [Troubleshooting](docs/TROUBLESHOOTING.md), and [OID inventory](docs/OID_REFERENCE.md).

## Why this project exists

Earlier attempts generated hundreds of unusable items by blindly discovering `hrStorage` and `hrDevice`, including non-existent instances, cascading calculated-item errors and a zero-denominator swap formula. This repository deliberately excludes those experiments from the maintained template. See [lessons learned](docs/TROUBLESHOOTING.md).

## Development and checks

Changes should be made on a branch and merged via a PR after automated structural checks and a manual SNMP acceptance run.

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_template.py templates/securepoint-utm-mib-v4.yaml
```

The check is **offline only**. Passing CI does not mean Zabbix accepted the import or the firewall returned the items. Provide sanitized findings using the [test checklist](docs/TESTING.md).

## Official MIBs and intellectual property

The proprietary `SECUREPOINT-UTM.mib` and `SECUREPOINT-MIB.mib` contain restrictive Securepoint GmbH copyright notices. **They are intentionally not redistributed here.** Authorized users can download both through [Securepoint's reseller portal](https://my.securepoint.de/) (Downloads → UTM, *MIB File – Securepoint NextGen UTM* and *MIB File – Securepoint Systeme Allgemein*). The project is **not affiliated with, endorsed by, or supported by Securepoint GmbH**.

Source-code licensing has not yet been selected by the repository owner; until then do not assume that repository contents carry an open-source license.

## Planned work

See [Roadmap](docs/ROADMAP.md). Priority is to establish a known-good device-specific OID inventory, then add useful graphs, selective trigger rules and dashboards. No blind broad SNMP-walk ingestion.

Contributions and sanitized test reports are welcome via GitHub Issues and PRs. Do not post SNMP secrets, public IP addresses, account names or client-specific tunnel names.
