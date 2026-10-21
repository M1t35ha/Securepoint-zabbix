# Install / migrate — Standalone Securepoint v1.0.0-rc.1

[Template YAML](../templates/securepoint-utm-standalone-v5.6.yaml) · [Russian guide](README_RU.md) · [RC1 tests](TESTING.md)

**Target:** Securepoint NextGen UTM 14.x with SNMP enabled; Zabbix 8.0. The exported YAML uses the Zabbix 7.0 format, accepted by the tested 8.0 RC instance. This RC has no parent template dependency.

## Fresh host

1. Download the YAML and go to **Data collection → Templates → Import**. Enable **Create new** and **Update existing** where appropriate; **Delete missing OFF**.
2. Create a monitored Host with one SNMP interface targeting the firewall on UDP/161. Configure read-only SNMPv3 credentials **in Zabbix**, not in Git. Prefer `authPriv` if available, and restrict access to your Zabbix server/proxy.
3. Link only **Securepoint UTM Standalone v5.6 by SNMP**. No Zabbix Agent and no `Network Generic Device by SNMP` required.
4. Navigate to **Monitoring → Hosts → [host] → Dashboards → Securepoint UTM | Standalone Command Center**.
5. Four pages should appear: Overview, Network, Interfaces, VPN & Security. Allow up to the LLD interval (default 1 hour) and two samples for per-second counters; then verify [Latest data and unsupported items](TESTING.md).
6. Customize host macros only after determining intended behavior. VPN interfaces may legitimately report zero traffic or disconnected peers.

## Migration from old Securepoint unified templates

**Do not link old and standalone templates together**: overlapping item keys and graphs can cause host update errors.

1. Import v5.6 as a **new template**, do not link yet.
2. Export the old Zabbix configuration for rollback. Record host macros and SNMP interface settings.
3. In the old Host, **Unlink and clear** `Securepoint UTM Unified v5 by SNMP` and any *directly linked* old generic/experimental templates if they are no longer wanted; save the Host **Update**.
4. Reopen the Host and add **Securepoint UTM Standalone v5.6 by SNMP**; **Update** again.
5. Confirm the inherited `Network interfaces` Host Dashboard disappears and own Dashboard loads. Old history and template-derived Items cleared in step 3 **cannot be restored by relinking**.
6. Do not delete the global generic template if other hosts depend on it.

The detailed migration rationale and rollback can be found in the [v5.6 migration record](V5_6_STANDALONE.md).

## Alerts and support caveats

- Firmware *difference* and license 30/7-day trigger definitions are included. The firmware field and a mismatch Problem are observed working; renewal thresholds, exactly-zero days, and alert **delivery** still need verification.
- `{$SP.LICENSE.ZERO.IS.EXPIRED}=0` by default, because a zero may mean an unlimited or different license model. Only opt in after confirming the license semantics.
- `{$SP.IF.ALERT}` is off by default. Enable a context macro for an always-on interface; do not alert on intentionally disconnected VPNs.
- SNMP 15-minute no-data trigger is enabled but its failure/recovery handling requires a controlled lab test.
- No SSH/API access or configuration changes to the firewall are required by this template.

See [Troubleshooting](TROUBLESHOOTING.md), [OID reference](OID_REFERENCE.md), and [RC1 acceptance status](RELEASE_CANDIDATE_1.md).
