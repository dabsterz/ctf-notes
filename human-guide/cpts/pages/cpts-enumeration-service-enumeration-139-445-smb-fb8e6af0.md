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
![Pasted image 20250401015814.png](../assets/Pasted%20image%2020250401015814.png)
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

##### ADD ! IN FRONT OF BASH COMMANDS WITHOUT INTERRUPTING CONNECTION

smbclient commands
![Pasted image 20250401014737.png](../assets/Pasted%20image%2020250401014737.png)

Check for live connections on victim machine
```shell-status
root@samba:~# smbstatus
```


Recursive download of whole share
```bash
smbclient //server/share -U username%password -c "prompt; recurse; mget *"
```
