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

