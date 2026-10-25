
Find available domain user accounts

### Using Enum4linux
```shell
enum4linux -U 172.16.5.5  | grep "user:" | cut -f2 -d"[" | cut -f1 -d"]"
```

### Using rpcclient
```shell
rpcclient -U "" -N 172.16.5.5
rpcclient $> enumdomusers 
```


### Using CrackMapExec --users Flag
```shell
crackmapexec smb 172.16.5.5 --users
sudo crackmapexec smb 172.16.5.5 -u htb-student -p Academy_student_AD! --users
```

### Gathering Users with LDAP Anonymous
```shell
ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "(&(objectclass=user))"  | grep sAMAccountName: | cut -f2 -d" "
```

### Using windapsearch
```shell
./windapsearch.py --dc-ip 172.16.5.5 -u "" -U
```

### Kerbrute User Enumeration
```shell
kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt 
```