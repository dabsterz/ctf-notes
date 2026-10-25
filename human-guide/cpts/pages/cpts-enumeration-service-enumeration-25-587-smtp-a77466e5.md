# 25,587 smtp


#### Basic Scanning
```shell
sudo nmap 10.129.14.128 -sC -sV -p25,587
sudo nmap 10.129.14.128 -p25 --script smtp-open-relay -v
```

#### Connecting to the target
```bash
telnet 10.129.14.128 25
```

#### Basic telnet commands
![Pasted image 20250401220050.png](../assets/Pasted%20image%2020250401220050.png)
![Pasted image 20250401220100.png](../assets/Pasted%20image%2020250401220100.png)

#### SMTP User Enum
![Pasted image 20250401225300.png](../assets/Pasted%20image%2020250401225300.png)

#### Default Config File
```shell
cat /etc/postfix/main.cf | grep -v "#" | sed -r "/^\s*$/d"
```

