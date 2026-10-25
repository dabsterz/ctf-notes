# 21 ftp


### Scanning
```bash
nmap -sC -sV -A -p21 10.129.42.253
nc -nv 10.129.42.253 21
telnet 10.129.42.253 21
ftp -p 10.129.42.253
ftp 10.129.42.253
openssl s_client -connect 10.129.14.136:21 -starttls ftp (if server has TLS/SSL)
```

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

### FTP Console Enumeration
- Change directory using cd at least once (might have a message)
- Login as different users as they might be placed in their own home directories

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

### Download All Available Files
```shell
vernonlim03@htb[/htb]$ wget -m --no-passive ftp://anonymous:anonymous@10.129.14.136
tree .
```
### vsFTPd server files
```bash
/etc/vsftpd.conf (file for server logs)
```
![Pasted image 20250328224040.png](../assets/Pasted%20image%2020250328224040.png)

#### FTPUSERS file (/etc/ftpusers) 
![Pasted image 20250328224556.png](../assets/Pasted%20image%2020250328224556.png)
USED TO DENY PEOPLE FROM ACCESSING THE FTP SERVICE



### Service Hardening Techniques
```bash
hide_ids=YES [All user and group information in directory listings will be displayed as "ftp".]
ls_recurse_enable=YES [Allows the use of recurse listings.]
```
