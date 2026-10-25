# Methodology Checklist


1. Vulnerable programs
2. SeimpersonatePrivilege
3. Unquoted Service Path
4. Service Binary Hijacking
5. DLL hijacking
6. Scheduled tasks
7. Mimikatz/Winpeas


---
## Manual Enumeration

### Get System Information
```cmd
systeminfo
```

### Check Hostname
```cmd
hostname
```

### Patches already implemented on system
```cmd
wmic qfe
wmic qfe get Caption,Description,HotFixID,InstalledOn

wmic logicaldisk get caption,description,providername
```

### Check whoami and privileges that we have
```cmd
whoami
whoami /priv
whoami /groups
```

### Enumerate for existing user accounts
```cmd
net user
net user bob
```

### Enumerate Groups
```cmd
net localgroup
net localgroup administrators
```

### Enumerate exposed credentials

import-module .\PowerView.ps1\
