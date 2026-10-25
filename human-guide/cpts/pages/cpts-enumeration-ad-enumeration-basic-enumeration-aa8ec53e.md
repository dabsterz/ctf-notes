# Basic Enumeration


```powershell
Get-Module
Import-Module ActiveDirectory
```

### Get Domain Info
```powershell
Get-ADDomain
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
Get-ADTrust -Filter *
Get-ADGroup -Filter * | select name
Get-ADGroup -Identity "Backup Operators"
Get-ADGroupMember -Identity "Backup Operators"
```

### Powerview
```powershell
import-module .\Powerview.ps1

Get-DomainUser -Identity mmorgan -Domain inlanefreight.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,useraccountcontrol

Get-DomainGroupMember -Identity "Domain Admins" -Recurse

Get-DomainTrustMapping

Test-AdminAccess -ComputerName ACADEMY-EA-MS01

Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName
```

### Snaffler
Searches for sensitive files in shares and displays them (VERY USEFUL)
```powershell
.\Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data
```

#### ARP (find other hosts)
```powershell
arp -a
```

#### View routing table
```powershell
route print
```

#### Quick WMI checks
```powershell
wmic ntdomain get Caption,Description,DnsForestName,DomainName,DomainControllerAddress
```

#### Net checks
![Pasted image 20250831200044.png](../assets/Pasted%20image%2020250831200044.png)

#### Dsquery
```powershell
dsquery user
dsquery computer
dsquery * "CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
dsquery * -filter "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))" -attr distinguishedName userAccountControl
dsquery * -filter "(userAccountControl:1.2.840.113556.1.4.803:=8192)" -limit 5 -attr sAMAccountName
```
