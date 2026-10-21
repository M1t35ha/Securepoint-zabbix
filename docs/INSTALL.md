# Installation (test host first)

## Unified v5 candidate (read before importing)

v5 is at `templates/securepoint-utm-unified-v5.yaml`. It has its own template name/UUIDs and may be tested **alongside** the v4 reference. The old v2/v3 experiments with unsupported-items storms are not part of v5.

**Until live-device acceptance tests pass, do not import v5 into the production host.** On the test day: export existing templates, create a separate test host, link v5 only (with its inherited generic template), and verify SNMPv3 read-only connectivity. Confirm that LLD creates only expected devices and that raw counter rates and firmware/HA/licence mappings are accurate. After validation, retire only the obsolete monitoring attachment; avoid `Delete missing` during initial import. Any `Unlink and clear` destroys data history and must be explicitly approved.

See [design](V5_DESIGN.md) and [test checklist](TESTING.md).


**Target:** Zabbix 8.0 / Securepoint NextGen UTM 14.x / read-only SNMPv3. This repository currently publishes a **test-stage** template.

1. In Zabbix, make sure the official `Network Generic Device by SNMP` template is installed.
2. Import `templates/securepoint-utm-mib-v4.yaml` in **Data collection → Templates → Import**. Do **not** enable **Delete missing** for unrelated objects.
3. Add a **new test host** with one SNMP interface set to the *firewall's management IP*. Set its SNMP version/security to match the Securepoint service. Use credentials stored **only in Zabbix**. Never copy them to issues, source control or SNMP logs.
4. Restrict firewall SNMP access to the Zabbix server/proxy. Verify IP reachability, UDP/161 rules, and SNMPv3 security level before troubleshooting individual OIDs.
5. Link **Securepoint UTM MIB Mapped v4 by SNMP**; the template already inherits `Network Generic Device by SNMP`.
6. Wait for discovery. Check **Monitoring → Latest data** and the discovered Items, then collect evidence with [TESTING.md](TESTING.md).
7. The 0/1/2/3 state numbers are decoded with manufacturer value maps where documented. Alerts remain disabled by default through `{$SP.*.ALERT}` macros; enable per required always-on service/tunnel *only after* confirming expected behavior.
8. If a device does not implement one scalar OID, disable that Item for that device and record this in the compatibility matrix.

**Do not use Unlink and clear on the existing production host during initial tests:** it deletes existing items/history. Do not bulk-import experimental old v2/v3 discovery rules.

## SNMPv3

Securepoint and Zabbix must agree on username, security level, authentication algorithm and authentication secret. Confirm reachability without publishing any authentication secrets in logs or ticket screenshots. SNMPv3 `authNoPriv` does **not encrypt** the data payload; prefer `authPriv` if supported by both device and operational policy.

## Upgrade procedure

Use a branch + PR → CI offline checks → sandbox import → test host SNMP checks → review generated LLD count → production migration. Keep a backup of your original template and Zabbix configuration.
