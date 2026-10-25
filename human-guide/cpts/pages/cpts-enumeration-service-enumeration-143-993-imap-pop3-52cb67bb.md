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

![Pasted image 20250402015201.png](../assets/Pasted%20image%2020250402015201.png)
![Pasted image 20250402015214.png](../assets/Pasted%20image%2020250402015214.png)

##### List all email contents in the inboxes
```bash
a1 LOGIN "username" "password"   # Authenticate
a2 LIST "" "*"                   # List all mailboxes
a3 SELECT INBOX                  # Access INBOX
a4 FETCH 1:* (FLAGS BODY.PEEK[]) # Fetch all emails
a5 LOGOUT                        # Disconnect
```
