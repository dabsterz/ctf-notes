
1. Simple Enumeration
2. Use our own scripts
3. Powerview.ps1
4. PsLoggedon.exe

---

Use Net to find out more about user,domain etc
```cmd
net user /domain
net user jeff
net user jeffadmin /domain
net group /domain
net group "Sales Department" /domain
```

Use our own scripts
```powershell
powershell -exec bypass
Import-Module .\function.ps1\ #can get it from cpts-tools

LDAPSearch -LDAPQuery "(samAccountType=805306368)"
LDAPSearch -LDAPQuery "(objectclass=group)"
foreach ($group in $(LDAPSearch -LDAPQuery "(objectCategory=group)")) {
$group.properties | select {$_.cn}, {$_.member}

$sales = LDAPSearch -LDAPQuery "(&(objectCategory=group)(cn=Sales Department))"
$sales.properties.member
}
```

Powerview
```powershell
powershell -exec bypass
Import-Module .\PowerView.ps1 #get from cpts-tools

# List of enumeration commands
Get-NetDomain
Get-NetUser
Get-NetUser | select cn
Get-NetUser | select cn,pwdlastset,lastlogon
Get-NetGroup | select cn
Get-NetGroup "Sales Department" | select member

Get-NetComputer
Get-NetComputer | select operatingsystem,dnshostname

#See where user accounts have logged into
Find-LocalAdminAccess
Get-NetSession
Get-NetSession -ComputerName files04 -Verbose
Get-NetSession -ComputerName web04

#Object enumeration
Get-ObjectAcl -Identity stephanie
Convert-SidToName S-1-5-21-1987370270-658905905-1781884369-1104

# use this command and look out for generic all, then use the sid to see what it is
Get-ObjectAcl -Identity "Management Department" | ? {$_.ActiveDirectoryRights -eq "GenericAll"} | select SecurityIdentifier,ActiveDirectoryRights
"S-1-5-21-1987370270-658905905-1781884369-512","S-1-5-21-1987370270-658905905-1781884369-1104" | Convert-SidToName

#domain share enumeration
Find-DomainShare

```

PsLoggedOn (this can check for logon sessions btr than powerview)
```powershell
.\PsLoggedon.exe \\files04 #where the \\files04 is the name of the pc
.\PsLoggedon.exe \\web04
```

Get Service principal names
```cmd
setspn -L iis_service
```
```powershell
Get-NetUser -SPN | select samaccountname,serviceprincipalname
```

---
#### Bloodhound
```powershell
# run sharphound on the target domain first
powershell -ep bypass
Import-Module .\Sharphound.ps1
Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\Users\stephanie\Desktop\ -OutputPrefix "corp audit"

#ON BASE KALI
sudo neo4j start
bloodhound #AUTH USING neo4j1:neo4j1
```