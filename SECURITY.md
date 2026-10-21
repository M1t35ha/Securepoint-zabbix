# Security and privacy

This repository contains a read-only SNMP monitoring template, **not** secrets or a firewall configuration. Keep SNMPv3 authentication/privacy credentials and private network information in the Zabbix configuration or an approved secrets vault.

- Prefer SNMPv3 `authPriv` when supported, and restrict SNMP access to Zabbix server/proxy IPs.
- Never paste real firewall IPs, usernames, license identifiers, peer public keys, passwords, client hostnames or unsanitized logs into public issues.
- Never enable user-session inventory or detailed VPN peer identity harvesting by default.
- If you find a vulnerability in the scripts/templates, open a minimal non-sensitive report; do not disclose secrets or exploitation details in public issues.
- No device configuration changes are performed by this template.

The two official Securepoint MIB modules have proprietary copyright notices and **must not be uploaded to this public repository without permission**.
