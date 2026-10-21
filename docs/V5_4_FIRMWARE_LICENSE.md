# Securepoint UTM v5.4 — Firmware & License Monitoring

This experimental revision extends [v5.3](../templates/securepoint-utm-unified-v5.3-dashboard.yaml), preserving template identity and prior monitoring history.

File: [securepoint-utm-unified-v5.4-firmware-license.yaml](../templates/securepoint-utm-unified-v5.4-firmware-license.yaml)

## MIB sources

These objects are defined by `SECUREPOINT-MIB.mib` (manufacturer file, not redistributed):

| Metric | Item key | Numeric OID (as currently configured) |
| --- | --- | --- |
| Installed version, `comVerCur` | `sp.mib.firmware.current` | `1.3.6.1.4.1.28553.1.2.7` |
| New manufacturer-reported version, `comVerNew` | `sp.mib.firmware.new` | `1.3.6.1.4.1.28553.1.2.8` |
| Remaining license days, `comLicDaysLeft` | `sp.mib.license.days` | `1.3.6.1.4.1.28553.1.3.5` |
| License type, `comLicType` | `sp.mib.license.type` | `1.3.6.1.4.1.28553.1.3.3` |

These are vendor scalar OID definitions used by the previous template. Do **not** assume they respond on every device and firmware. The former tests showed these fields as **No data** on the example firewall. Check Latest data and the SNMP agent's Info before treating the alerts as operational. SNMP scalar instance suffix `.0` convention differs from the manufacturer's earlier base-address examples; inspect raw responses before changing either convention.

## VPN & Security dashboard

Four new cards at top:
- Installed firmware
- New firmware reported (manufacturer feed; not necessarily globally newest, stable or suitable)
- License days remaining
- License type

Existing CPU/RAM/uptime, WireGuard, IPsec, OpenVPN and antivirus widgets are retained and moved down three rows.

## Triggers

| Trigger | Default | Condition |
| --- | --- | --- |
| Firmware update reported | Enabled via macro | Both fresh values contain version-like strings and differ |
| License expires within warning threshold | Enabled via macro | More than 7 and at most 30 days (configurable) |
| License renewal urgent | Enabled via macro | Between 1 and 7 days inclusive |
| 0 license days reported | **Off by default** | Exactly 0, and explicitly opted in after checking license semantics |

Macros:
- `{$SP.FIRMWARE.ALERT}=1`
- `{$SP.LICENSE.ALERT}=1`
- `{$SP.LICENSE.WARN.DAYS}=30`
- `{$SP.LICENSE.CRIT.DAYS}=7`
- `{$SP.LICENSE.ZERO.IS.EXPIRED}=0`

Triggers use `nodata(...,1d)=0` on relevant fields to reduce stale-data alerts. A genuinely unsupported item yields no meaningful renewal alert; the absence of alarms does **not** guarantee that the license is valid.

The firmware trigger compares **strings**, not semantic version tuples. It reports a **manufacturer-reported different version**; visually verify that the upgrade is actually suitable before patching. An update label is not proof that your UTM is behind the globally latest release.

Existing host-level macros override template defaults. For a customer whose license model reports `0` for an unlimited term, **do not enable** `{$SP.LICENSE.ZERO.IS.EXPIRED}`. Configure Zabbix Action + Media types for e-mail/Teams/etc. to receive external notifications; triggers only create Problems.

## Acceptance checklist

1. Export current template, then import v5.4 using `Update existing`, `Create new`, **Delete missing off**.
2. Confirm four cards appear on **VPN & Security** without losing any prior graphs.
3. Verify `sp.mib.firmware.current`, `sp.mib.firmware.new`, `sp.mib.license.days` all have actual values on the test device.
4. If No data, check Items → Info errors; a manufacturer MIB definition alone is not proof of device support.
5. Simulate the alert thresholds in a safe test environment before enabling a fleet-wide Zabbix Action.
6. Confirm the severity/noise fits license models across sites. Enable the zero-day macro only with verified semantics.
7. Do not merge as production-ready until a real Zabbix 8.0 import and SNMP poll succeed.

For Zabbix trigger syntax see [official 8.0 trigger expressions](https://www.zabbix.com/documentation/8.0/en/manual/config/triggers/expression).
