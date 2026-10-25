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
![Pasted image 20250403004448.png](../assets/Pasted%20image%2020250403004448.png)
