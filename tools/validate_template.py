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
        alerts = {m.get("macro"): m.get("value") for m in template.get("macros", [])}
        for macro, value in alerts.items():
            if macro and macro.endswith(".ALERT}") and value != "0":
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
