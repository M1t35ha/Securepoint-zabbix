#!/usr/bin/env python3
"""Offline structural checks for Securepoint → Zabbix templates (not a Zabbix import test)."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

UUID = re.compile(r"^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$")
FORBIDDEN_OID_PREFIXES = ("1.3.6.1.2.1.25.2.3.", "1.3.6.1.2.1.25.3.2.")
SNMP_OID = re.compile(r"^(get|discovery)\[.*\]$")
PRIVATE_KEYS = {"authpassphrase", "privpassphrase", "password", "privatekey", "token", "apikey"}


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def check(path: Path) -> list[str]:
    errors = []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"Could not read YAML: {exc}"]
    export = (doc or {}).get("zabbix_export", {})
    templates = export.get("templates", [])
    if not templates:
        return ["Missing zabbix_export.templates"]
    if export.get("version") not in {"7.0", "7.2", "7.4", "8.0"}:
        errors.append("Unexpected Zabbix export version")
    all_uuids = [v["uuid"] for v in walk(doc) if "uuid" in v]
    for u in all_uuids:
        if not isinstance(u, str) or not UUID.fullmatch(u):
            errors.append(f"UUID does not look like v4: {u}")
    for u, n in Counter(all_uuids).items():
        if n != 1:
            errors.append(f"Duplicate UUID: {u}")
    for obj in walk(doc):
        for k in obj:
            if k.lower() in PRIVATE_KEYS:
                errors.append(f"Potential credential field: {k}")
    for template in templates:
        name = template.get("template")
        if not name:
            errors.append("Template has no identifier")
        items = template.get("items", [])
        rules = template.get("discovery_rules", [])
        keys = [x.get("key") for x in items + rules]
        keys += [p.get("key") for rule in rules for p in rule.get("item_prototypes", [])]
        for key, n in Counter(keys).items():
            if not key or n != 1:
                errors.append(f"Empty/duplicate item or LLD key: {key}")
        regular = {x["key"] for x in items if "key" in x}
        all_keys = set(keys)
        for rule in rules:
            if "tags" in rule:
                errors.append(f"LLD rule has unsupported tags field: {rule.get('name')}")
            local = {p["key"] for p in rule.get("item_prototypes", [])}
            for p in rule.get("item_prototypes", []):
                if p.get("type") == "DEPENDENT":
                    master = (p.get("master_item") or {}).get("key")
                    if master not in local:
                        errors.append(f"Missing prototype master item: {p.get('key')} -> {master}")
                if p.get("type") == "CALCULATED" and "/0" in str(p.get("params", "")):
                    errors.append(f"Potential zero divisor: {p.get('key')}")
            for graph in rule.get("graph_prototypes", []):
                for series in graph.get("graph_items", []):
                    ref = (series.get("item") or {}).get("key")
                    if ref not in local:
                        errors.append(f"Graph prototype {graph['name']} references missing prototype: {ref}")
        for graph in export.get("graphs", []):
            for series in graph.get("graph_items", []):
                ref = (series.get("item") or {}).get("key")
                if ref not in regular:
                    errors.append(f"Top-level graph {graph['name']} references non-static item: {ref}")
        for obj in items + [p for r in rules for p in r.get("item_prototypes", [])]:
            if obj.get("type") == "SNMP_AGENT":
                oid = obj.get("snmp_oid", "")
                if not SNMP_OID.fullmatch(oid):
                    errors.append(f"Bad SNMP OID expression: {obj.get('key')}: {oid}")
                if any(prefix in oid for prefix in FORBIDDEN_OID_PREFIXES):
                    errors.append(f"Known noisy host-resources OID: {obj.get('key')}")
        for rule in rules:
            oid = rule.get("snmp_oid", "")
            if not SNMP_OID.fullmatch(oid):
                errors.append(f"Bad LLD SNMP OID: {rule.get('key')}: {oid}")
            if any(prefix in oid for prefix in FORBIDDEN_OID_PREFIXES):
                errors.append(f"Known noisy host-resources LLD: {rule.get('key')}")
        # Template dashboards cannot refer to graph prototypes belonging to a linked parent template.
        # Zabbix otherwise rejects the import with "Graph prototype with ID ... is not available".
        dashboard_graphs = {g.get("name") for g in export.get("graphs", [])}
        dashboard_prototypes = {g.get("name") for r in rules for g in r.get("graph_prototypes", [])}
        for dashboard in template.get("dashboards", []):
            for page in dashboard.get("pages", []):
                for widget in page.get("widgets", []):
                    for field in widget.get("fields", []):
                        if field.get("type") not in {"ITEM", "GRAPH", "GRAPH_PROTOTYPE"}:
                            continue
                        value = field.get("value") or {}
                        if value.get("host") != name:
                            errors.append(f"Dashboard {dashboard.get('name')} widget {widget.get('name')} references external template {value.get('host')}")
                        elif field["type"] == "ITEM" and value.get("key") not in regular:
                            errors.append(f"Dashboard widget {widget.get('name')} references missing item {value.get('key')}")
                        elif field["type"] == "GRAPH" and value.get("name") not in dashboard_graphs:
                            errors.append(f"Dashboard widget {widget.get('name')} references missing graph {value.get('name')}")
                        elif field["type"] == "GRAPH_PROTOTYPE" and value.get("name") not in dashboard_prototypes:
                            errors.append(f"Dashboard widget {widget.get('name')} references missing graph prototype {value.get('name')}")
        # Vendor OID regression guard v5.2: Securepoint example and previous observed walk omit scalar .0.
        if path.name.endswith("v5.2-dashboard.yaml"):
            vendor_scalars = [i for i in items if i.get("snmp_oid", "").startswith("get[1.3.6.1.4.1.28553.")]
            for item in vendor_scalars:
                if item["snmp_oid"].endswith(".0]"):
                    errors.append(f"v5.2 vendor scalar with unverified .0 suffix: {item['key']}")
            iface = next((r for r in rules if r.get("key") == "sp.dashboard.interface.discovery"), None)
            if not iface or not iface.get("filter", {}).get("conditions"):
                errors.append("v5.2 interface discovery missing safety filter")
            if "{$SP.DASHBOARD.IF.MATCHES}" not in {m.get("macro") for m in template.get("macros", [])}:
                errors.append("v5.2 interface discovery filter macro missing")
            for dashboard in template.get("dashboards", []):
                overview = next((p for p in dashboard.get("pages", []) if p.get("name") == "Overview"), None)
                if overview:
                    top_cards = [w for w in overview.get("widgets", []) if w.get("type") == "item" and int(w.get("y", "0")) == 0]
                    for card in top_cards:
                        if any(f.get("type") == "ITEM" and (f.get("value") or {}).get("key", "").startswith("sp.mib.")
                               for f in card.get("fields", [])):
                            errors.append(f"v5.2 overview top card depends on unverified vendor metric: {card.get('name')}")
        if path.name.endswith("v5.4-firmware-license.yaml"):
            keys_needed = {"sp.mib.firmware.current", "sp.mib.firmware.new", "sp.mib.license.days", "sp.mib.license.type"}
            found = {item.get("key"): item for item in items}
            if keys_needed - found.keys():
                errors.append(f"v5.4: missing firmware/license items: {keys_needed - found.keys()}")
            cfg = {m.get("macro"): m.get("value") for m in template.get("macros", [])}
            required = {"{$SP.FIRMWARE.ALERT}": "1", "{$SP.LICENSE.ALERT}": "1",
                        "{$SP.LICENSE.WARN.DAYS}": "30", "{$SP.LICENSE.CRIT.DAYS}": "7",
                        "{$SP.LICENSE.ZERO.IS.EXPIRED}": "0"}
            for m, desired in required.items():
                if cfg.get(m) != desired:
                    errors.append(f"v5.4: invalid default for {m}: {cfg.get(m)}")
            trigger_expressions = [tr.get("expression", "") for item in items for tr in item.get("triggers", [])]
            if not any("sp.mib.firmware.new" in exp and "sp.mib.firmware.current" in exp and "<>" in exp for exp in trigger_expressions):
                errors.append("v5.4: missing vendor firmware comparison trigger")
            if not any("{$SP.LICENSE.WARN.DAYS}" in exp for exp in trigger_expressions):
                errors.append("v5.4: missing license warning threshold")
            if not any("{$SP.LICENSE.CRIT.DAYS}" in exp and ">0" in exp for exp in trigger_expressions):
                errors.append("v5.4: missing license urgent threshold")
            if not any("{$SP.LICENSE.ZERO.IS.EXPIRED}=1" in exp for exp in trigger_expressions):
                errors.append("v5.4: missing opt-in zero-license trigger")
            vpn_pages = [page for dash in template.get("dashboards", []) for page in dash.get("pages", []) if page.get("name") == "VPN & Security"]
            if not vpn_pages or not keys_needed.issubset(
                {f.get("value", {}).get("key") for w in vpn_pages[0].get("widgets", []) for f in w.get("fields", []) if f.get("type") == "ITEM"}):
                errors.append("v5.4: missing firmware/license dashboard cards")
        if path.name.endswith("v5.5-interfaces.yaml"):
            rule = next((r for r in rules if r.get("key") == "sp.dashboard.interface.discovery"), None)
            expected = {"in.bps", "out.bps", "oper.status", "admin.status", "speed", "in.errors", "out.errors", "in.discards", "out.discards"}
            if rule is None:
                errors.append("v5.5: missing interface discovery")
            else:
                actual = {p.get("key", "").split("[")[0].removeprefix("sp.dashboard.interface.") for p in rule.get("item_prototypes", [])}
                if expected != actual:
                    errors.append(f"v5.5: unexpected interface prototype keys {actual ^ expected}")
                if len(rule.get("graph_prototypes", [])) != 2:
                    errors.append("v5.5: expected traffic and errors/discards graph prototypes")
                if not rule.get("filter", {}).get("conditions"):
                    errors.append("v5.5: missing interface discovery filter")
            pages = [p.get("name") for d in template.get("dashboards", []) for p in d.get("pages", [])]
            if pages != ["Overview", "Network", "Interfaces", "VPN & Security"]:
                errors.append(f"v5.5: incorrect dashboard pages: {pages}")
            vmap_names = {m.get("name") for m in template.get("valuemaps", [])}
            if not {"Securepoint interface operational status", "Securepoint interface administrative status"}.issubset(vmap_names):
                errors.append("v5.5: missing interface state value maps")
        if path.name.endswith("standalone-v5.6.yaml"):
            if template.get("templates"):
                errors.append("Standalone v5.6 must have zero linked parent templates")
            if template.get("template") != "Securepoint UTM Standalone v5.6 by SNMP":
                errors.append("Standalone v5.6 missing separate technical template identity")
            needed = {"sp.dashboard.uptime", "sp.core.snmp.uptime", "sp.core.system.objectid"}
            if not needed.issubset(regular):
                errors.append(f"Standalone v5.6 system Items missing: {needed - regular}")
            iface = next((r for r in rules if r.get("key") == "sp.dashboard.interface.discovery"), None)
            if not iface or len(iface.get("item_prototypes", [])) < 9 or len(iface.get("graph_prototypes", [])) != 2:
                errors.append("Standalone v5.6 lacks own IF-MIB monitoring")
            else:
                operative = next((p for p in iface["item_prototypes"] if p.get("key","").startswith("sp.dashboard.interface.oper.status")), {})
                if not operative.get("trigger_prototypes"):
                    errors.append("Standalone v5.6 missing opt-in IF link-state trigger")
            upitem = next((i for i in items if i.get("key") == "sp.dashboard.uptime"), {})
            if not any("nodata(" in t.get("expression","") for t in upitem.get("triggers", [])):
                errors.append("Standalone v5.6 missing SNMP no-data alert")
            pages = [p.get("name") for d in template.get("dashboards",[]) for p in d.get("pages", [])]
            if pages != ["Overview", "Network", "Interfaces", "VPN & Security"]:
                errors.append(f"Standalone v5.6 missing dashboard pages: {pages}")
        alerts = {m.get("macro"): m.get("value") for m in template.get("macros", [])}
        for macro, value in alerts.items():
            enabled_for_v54 = path.name in {"securepoint-utm-unified-v5.4-firmware-license.yaml", "securepoint-utm-unified-v5.5-interfaces.yaml", "securepoint-utm-standalone-v5.6.yaml"} and macro in {"{$SP.FIRMWARE.ALERT}", "{$SP.LICENSE.ALERT}"}
            if macro and macro.endswith(".ALERT}") and value != "0" and not enabled_for_v54 and not (path.name.endswith("standalone-v5.6.yaml") and macro == "{$SP.SNMP.NODATA.ALERT}"):
                errors.append(f"Alert macro not off by default: {macro}")
        if not all_keys:
            errors.append(f"Template {name} has no keys")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path)
    args = parser.parse_args()
    errors = check(args.template)
    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1
    print(f"PASS: offline template structure looks consistent: {args.template}")
    print("NOTE: SNMP support, real Zabbix import, performance and alert semantics are NOT verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
