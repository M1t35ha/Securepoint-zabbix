#!/usr/bin/env python3
"""Summarize a numeric Securepoint SNMP walk without echoing potentially sensitive values.

Read a locally saved Net-SNMP walk. Never commit or share the raw walk output.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import sys

OID_LINE = re.compile(r"^\s*(?P<oid>(?:iso\.|\.?1\.)\d+(?:\.\d+)*)\s*=")
BASE = "1.3.6.1.4.1.28553"
TABLES = {
    "services": {"name": BASE + ".2.1.1.1.1.2", "columns": {"state": BASE + ".2.1.1.1.1.3", "flags": BASE + ".2.1.1.1.1.4"}},
    "ipsec": {"name": BASE + ".2.1.2.1.1.2", "columns": {"state": BASE + ".2.1.2.1.1.3", "subnets": BASE + ".2.1.2.1.1.4"}},
    "openvpn": {"name": BASE + ".2.1.3.1.1.2", "columns": {"state": BASE + ".2.1.3.1.1.3", "clients": BASE + ".2.1.3.1.1.4"}},
    "antivirus": {"name": BASE + ".2.1.5.1.1.2", "columns": {"last_update": BASE + ".2.1.5.1.1.3", "last_run": BASE + ".2.1.5.1.1.4", "state": BASE + ".2.1.5.1.1.5"}},
    "wireguard_interfaces": {"name": BASE + ".2.1.11.1.1.2", "columns": {"status": BASE + ".2.1.11.1.1.4", "port": BASE + ".2.1.11.1.1.6", "peer_count": BASE + ".2.1.11.1.1.7"}},
    "wireguard_peers": {"name": BASE + ".2.1.11.2.1.2", "columns": {"status": BASE + ".2.1.11.2.1.3", "handshake": BASE + ".2.1.11.2.1.6", "sent": BASE + ".2.1.11.2.1.7", "received": BASE + ".2.1.11.2.1.8"}},
}
SCALARS = {
    "product": BASE + ".1.1.0",
    "firmware_current": BASE + ".1.2.7.0",
    "firmware_new": BASE + ".1.2.8.0",
    "license_days_left": BASE + ".1.3.5.0",
    "conntrack_max": BASE + ".2.1.10.1.0",
    "conntrack_current": BASE + ".2.1.10.2.0",
    "ha_enabled": BASE + ".2.1.12.1.0",
}

def parse_oids(lines):
    oids = set()
    for line in lines:
        m = OID_LINE.match(line)
        if not m:
            continue
        oid = m.group("oid").removeprefix(".").replace("iso.", "1.", 1)
        oids.add(oid)
    return oids

def indexes(oids, prefix):
    needle = prefix + "."
    return {oid[len(needle):] for oid in oids if oid.startswith(needle) and len(oid) > len(needle)}

def analyze(oids):
    out = {"parsed_oids": len(oids), "securepoint_oids": sum(k.startswith(BASE + ".") for k in oids)}
    out["scalars_present"] = {name: oid in oids for name, oid in SCALARS.items()}
    tables = {}
    for name, schema in TABLES.items():
        rows = indexes(oids, schema["name"])
        # Never expose table index values: some indices can encode addresses or names.
        tables[name] = {"discovered_rows": len(rows), "missing_columns_by_type":
            {column: len(rows - indexes(oids, col_oid)) for column, col_oid in schema["columns"].items()}}
    out["tables"] = tables
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("walk", type=pathlib.Path, help="Private, local numeric SNMP walk file")
    parser.add_argument("--json", action="store_true", help="JSON summary only (no raw values)")
    args = parser.parse_args()
    try:
        with args.walk.open(encoding="utf-8", errors="replace") as handle:
            report = analyze(parse_oids(handle))
    except OSError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Parsed {report['parsed_oids']} numeric OIDs; {report['securepoint_oids']} under Securepoint enterprise")
        for name, found in report["scalars_present"].items():
            print(f"  scalar {name}: {'present' if found else 'absent'}")
        for name, info in report["tables"].items():
            missing = ", ".join(f"{field}:{count}" for field, count in info["missing_columns_by_type"].items() if count)
            print(f"  {name}: {info['discovered_rows']} rows; missing column samples: {missing or 'none'}")
    print("Reminder: raw SNMP walk files may contain client metadata; never publish them.", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
