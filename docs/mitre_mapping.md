# MITRE ATT&CK Mapping

| Scenario | Tactic | Technique ID | Technique Name | Detection Rule | Severity |
|---|---|---|---|---|---|
| suspicious-powershell | Execution | T1059.001 | PowerShell | suspicious_powershell_rule | High |
| ssh-bruteforce | Credential Access | T1110 | Brute Force | ssh_bruteforce_rule | High |
| new-admin-user | Persistence | T1136 | Create Account | new_admin_user_rule | High |
| scheduled-task-creation | Execution | T1053 | Scheduled Task/Job | scheduled_task_rule | Medium |
| temp-process-execution | Execution | T1204 | User Execution | temp_process_rule | High |
| suspicious-curl-download | Command and Control | T1105 | Ingress Tool Transfer | suspicious_curl_rule | High |
| process-masquerading | Defense Evasion | T1036 | Masquerading | process_masquerading_rule | High |
| abnormal-login-time | Initial Access | T1078 | Valid Accounts | abnormal_login_time_rule | Medium |
| webshell-like-request | Persistence | T1505.003 | Web Shell | webshell_like_request_rule | Critical |
| dns-exfil-pattern | Exfiltration | T1048 | Exfiltration Over Alternative Protocol | dns_exfil_pattern_rule | High |

## Tactics Coverage

| Tactic | Scenarios | Count |
|---|---|---|
| Execution | suspicious-powershell, scheduled-task-creation, temp-process-execution | 3 |
| Persistence | new-admin-user, webshell-like-request | 2 |
| Credential Access | ssh-bruteforce | 1 |
| Defense Evasion | process-masquerading | 1 |
| Initial Access | abnormal-login-time | 1 |
| Command and Control | suspicious-curl-download | 1 |
| Exfiltration | dns-exfil-pattern | 1 |

## Platform Coverage

| Platform | Scenarios |
|---|---|
| Windows | suspicious-powershell, new-admin-user, scheduled-task-creation, temp-process-execution, process-masquerading |
| Linux | ssh-bruteforce, suspicious-curl-download |
| Identity/IAM | abnormal-login-time |
| Web | webshell-like-request |
| Network | dns-exfil-pattern |
