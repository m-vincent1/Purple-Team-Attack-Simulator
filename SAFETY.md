# SAFETY.md — Purple Team Attack Simulator

## Purpose

This document describes the security boundaries, authorized use cases, and design decisions that make Purple Team Attack Simulator a safe, defensive-only tool.

## What this tool does

Purple Team Attack Simulator generates **synthetic telemetry** — fake but realistic log events — to test whether detection rules correctly identify attacker-like patterns. It is a lab tool for security teams to validate their detection coverage without touching production systems.

## What this tool does NOT do

This tool strictly prohibits and does not implement:

- Malware creation or deployment
- Reverse shells or remote code execution
- Credential theft or credential dumping
- Antivirus/EDR bypass techniques
- Real vulnerability exploitation
- Aggressive network scanning
- Attacks against third-party systems
- Real persistence mechanisms (registry, cron, services)
- Destructive encryption
- System log deletion
- Real lateral movement
- Dangerous payloads
- Any instruction that could be used to attack a real target

## Synthetic-first design

All simulation runs operate in **synthetic mode** by default:

- Log events are generated in memory using Python data structures
- No system calls are made to create processes, files, or network connections
- All "attack" patterns exist only as JSON objects in the database and JSONL files
- The `lab_sandbox/` directory is the only place where local file operations are allowed
- The sandbox uses only temporary dummy files with no system impact
- A `pts clean` command removes all generated artifacts

## lab_sandbox/ constraints

If a future local execution mode is added, it must follow these rules:

1. Only operate inside `lab_sandbox/`
2. Only create temporary dummy files (e.g., empty `.txt` files)
3. No privilege escalation
4. No dangerous system modifications
5. No connections to external targets
6. No persistent changes
7. Fully reversible with `pts clean`

## Authorized use cases

- Local lab environments (VM, homelab, isolated network)
- SOC training and onboarding
- Detection rule validation
- Purple team exercises
- Security portfolio demonstrations
- Academic research and education

## Unauthorized use cases

- Use against any system without explicit written authorization
- Use in production environments
- Use to develop or test actual attack capabilities
- Distribution as part of an offensive toolkit

## Responsible disclosure

If you find a way this tool could be used offensively, please open a GitHub issue with the label `security` so the behavior can be removed or restricted.

## License note

This tool is provided for educational and defensive purposes only. The authors are not responsible for misuse.
