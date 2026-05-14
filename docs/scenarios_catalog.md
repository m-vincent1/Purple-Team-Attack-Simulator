# Scenarios Catalog

| # | ID | Name | Platform | MITRE | Tactic | Rule | Expected Result |
|---|---|---|---|---|---|---|---|
| 1 | `suspicious-powershell` | Suspicious PowerShell Execution | Windows | T1059.001 | Execution | suspicious_powershell_rule | Alert on EncodedCommand pattern |
| 2 | `ssh-bruteforce` | SSH Brute Force Pattern | Linux | T1110 | Credential Access | ssh_bruteforce_rule | Alert on repeated Failed password |
| 3 | `new-admin-user` | New Admin User Created | Windows | T1136 | Persistence | new_admin_user_rule | Alert on Administrators group addition |
| 4 | `scheduled-task-creation` | Scheduled Task Creation | Windows | T1053 | Execution | scheduled_task_rule | Alert on schtasks.exe usage |
| 5 | `temp-process-execution` | Process Execution from Temp Directory | Windows | T1204 | Execution | temp_process_rule | Alert on execution from Temp path |
| 6 | `suspicious-curl-download` | Suspicious Curl Download | Linux | T1105 | C2 | suspicious_curl_rule | Alert on curl + /tmp/ pattern |
| 7 | `process-masquerading` | Process Masquerading | Windows | T1036 | Defense Evasion | process_masquerading_rule | Alert on typosquat process name |
| 8 | `abnormal-login-time` | Abnormal Login Time | Identity | T1078 | Initial Access | abnormal_login_time_rule | Alert on off-hours authentication |
| 9 | `webshell-like-request` | Webshell-like HTTP Request | Web | T1505.003 | Persistence | webshell_like_request_rule | Alert on ?cmd= URL parameter |
| 10 | `dns-exfil-pattern` | DNS Exfiltration Pattern | Network | T1048 | Exfiltration | dns_exfil_pattern_rule | Alert on base64 DNS subdomain |

## Detailed Descriptions

### 1. Suspicious PowerShell Execution
Generates Windows Event 4688 (process creation) logs for powershell.exe with benign commands, plus one event with an EncodedCommand parameter. The detection rule looks for `-enc`, `EncodedCommand`, or `FromBase64String` in the command line.

### 2. SSH Brute Force Pattern
Generates Linux auth log entries showing repeated failed SSH authentication attempts from the same external IP. The detection rule triggers on `Failed password` patterns in the raw_message.

### 3. New Admin User Created
Generates Windows Event 4720 (user created) and 4732 (member added to group) logs. The detection rule triggers when a user is added to the Administrators group.

### 4. Scheduled Task Creation
Generates Windows Event 4698 (scheduled task created) logs via schtasks.exe. The detection rule triggers on any scheduled_task_created event from schtasks.

### 5. Process Execution from Temp Directory
Generates Windows Event 4688 logs showing process execution from `C:\Windows\Temp\` or `AppData\Local\Temp\`. The detection rule triggers on command lines containing these temp paths.

### 6. Suspicious Curl Download
Generates Linux process logs showing curl commands. The suspicious event includes a `/tmp/` download path. The rule triggers on curl processes with `/tmp/` in the command line.

### 7. Process Masquerading
Generates Windows Event 4688 logs for a process named `svch0st.exe` (zero instead of 'o'). The rule detects known typosquat process names.

### 8. Abnormal Login Time
Generates IAM authentication logs, including one at 03:17 AM from an external IP. The rule triggers on `off-hours` in the raw_message.

### 9. Webshell-like HTTP Request
Generates web access log events. The suspicious request contains `?cmd=` in the URL. The rule triggers on webshell command execution URL patterns.

### 10. DNS Exfiltration Pattern
Generates DNS query logs. The suspicious query includes a base64-encoded subdomain. The rule triggers on the specific base64 pattern used in the synthetic log.
