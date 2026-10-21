# Standalone v5.6 — migration and rollback record

**Current RC1 template:** [Standalone v5.6 YAML](../templates/securepoint-utm-standalone-v5.6.yaml) · [Installation](INSTALL.md) · [RC1 live evidence](RELEASE_CANDIDATE_1.md)

## Why standalone?

Earlier v5.5 inherited `Network Generic Device by SNMP`. That added a redundant one-graph-per-interface Host Dashboard. The **current standalone template contains its own IF-MIB discovery** (64-bit RX/TX, status, link speed, errors, discards), plus manufacturer VPN/licensing and four self-contained Host Dashboard pages.

Standalone requires **no nested templates** and does not require installing a Zabbix Agent on the Securepoint firewall.

## Migration performed on the initial test host

1. Import v5.6 with `Create new` and **Delete missing OFF**.
2. In the existing Host, **Unlink and clear** old Unified v5 and, if directly attached and no longer needed, the generic parent. Save Host.
3. In a **second save**, link only `Securepoint UTM Standalone v5.6 by SNMP`; leave existing SNMPv3 interface/security configuration intact.
4. Verify Dashboard `Securepoint UTM | Standalone Command Center`. The inherited `Network interfaces` Dashboard is no longer needed.
5. Wait for LLD and two samples for per-second counters; check latest values and Errors/Problems.

**`Unlink and clear` deletes historical Item measurements.** The user explicitly accepted that loss for the original migration. The official generic template is *not* removed globally; other Zabbix hosts may still use it.

## Actual verification

User screenshots showed successful Zabbix 8.0 import, standalone Host linking, four Dashboard tabs, six interfaces with working states/speed, nonzero RX/TX rates and graphs, error/discard graphs, CPU/RAM/TCP/UDP data, firmware/available version and license type/days, plus a correctly raised firmware mismatch Problem. [Details and remaining acceptance](RELEASE_CANDIDATE_1.md).

This is **not** evidence that every vendor MIB feature works on other models or firmware versions. Live WireGuard peer transition/handshake, SNMP no-data and link-down triggers, licensing thresholds and alert delivery still need tests.

## Rollback options

If a later version fails, re-import the **current working v5.6 RC1 YAML** to restore its configuration. If specifically needing an older unified implementation, the former [v5.5 YAML is archived in the development branch](https://github.com/M1t35ha/Securepoint-zabbix/blob/feature/utm-v5-unified/templates/securepoint-utm-unified-v5.5-interfaces.yaml). Unlink and clear the standalone template and relink the earlier template in two separate Host saves, with full awareness that collected history may be removed.

Do not connect both on the same host: they use overlapping Item Keys. The old `Network Generic Device by SNMP` dependency and Dashboard return if you restore the unified template.

All releases and archive references are described in [CHANGELOG](../CHANGELOG.md).
