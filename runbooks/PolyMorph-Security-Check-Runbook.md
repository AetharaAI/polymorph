SECURITY / CONNECTIVITY TRIAGE RUNBOOK

When I say: “run a security check” on a Linux box or my local workstation, do a non-destructive triage pass first. Do not change config, restart services, kill processes, install packages, or modify firewall rules unless I explicitly authorize it.

Goal:
Determine whether the issue is most likely:
1. local machine problem
2. network / route / packet loss problem
3. remote host resource problem
4. ssh / auth / dns problem
5. obvious security indicator

PHASE 1 — LOCAL MACHINE CHECKS
Run:
- uptime
- top -b -n 1 | head -40
- df -h
- free -h
- ss -s
- ss -tulpn
- journalctl -p 3 -xb | tail -100
- dmesg -T | tail -100

Look for:
- high load
- swap pressure
- disk nearly full
- obvious kernel/network errors
- suspicious listeners

PHASE 2 — CONNECTIVITY CHECKS TO TARGET
For both Tailscale IP and public IP if available, run:
- ping -c 20 <target>
- mtr -rwzc 50 <target>
- time ssh -vvv <user>@<target> exit

Determine:
- latency
- packet loss
- whether ssh delay is before connect, during handshake, or after auth

PHASE 3 — REMOTE HOST CHECKS
If ssh succeeds, run on remote:
- uptime
- top -b -n 1 | head -40
- df -h
- free -h
- vmstat 1 5
- ps -el | grep Z
- systemctl status ssh --no-pager
- journalctl -u ssh --since "30 min ago" --no-pager | tail -100
- ss -tulpn
- ufw status verbose || true
- iptables -L -n -v || true

If available, also run:
- iostat -xz 1 5
- sar -n DEV 1 5

Look for:
- cpu saturation
- memory exhaustion
- disk fullness / io wait
- zombie accumulation
- ssh daemon errors
- unexpected exposed ports
- firewall anomalies

PHASE 4 — SECURITY SANITY CHECK
Without making changes, check for:
- unknown listening services
- unexpected recent auth failures
- suspicious new users
- suspicious sudo activity
- unusual cron/systemd timers
- abnormal outbound connections if visible

Useful commands:
- last -a | head -40
- lastb -a | head -40 || true
- getent passwd | tail -20
- sudo journalctl _COMM=sudo --since "24 hours ago" --no-pager | tail -100
- crontab -l || true
- ls -la /etc/cron* 2>/dev/null
- systemctl list-timers --all --no-pager
- ss -tpn

PHASE 5 — OUTPUT FORMAT
Return a short report with:
1. Summary
2. Most likely cause
3. Evidence
4. Security finding level:
   - none obvious
   - suspicious, review needed
   - urgent
5. Recommended next step

Rules:
- Prefer evidence over guesses.
- If both Tailscale and public IP are slow, consider local path / ISP / route issues first.
- If RAM/CPU are normal, do not blame “too many processes” without proof.
- Zombie processes alone are not an incident unless tied to a real failing parent/service.
- If no clear security indicators are found, say so plainly.
- Keep the report concise and operational.
