
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



#### Wordpress config file MIGHT contain mysql creds so be a lookout for wp-config.php (use the command to fish for the MYSQL creds)
```shell
grep 'DB_USER\|DB_PASSWORD' wp-config.php
```