
- If the service is configured poorly, we might get free authentication
- If we are included in /etc/hosts.equiv or .rhosts files on the system

![[Pasted image 20250403224738.png]]

Basic Commands
```shell
sudo nmap -sV -p 512,513,514 10.0.17.2
```

Logging in using Rlogin
```shell
rlogin 10.0.17.2 -l htb-student
```


Finding Authenticated users using R-Commands
![[Pasted image 20250403224858.png]]

![[Pasted image 20250403225049.png]]
