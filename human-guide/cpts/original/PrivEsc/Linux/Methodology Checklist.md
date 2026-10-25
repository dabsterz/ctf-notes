
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

## Simple Manual Enumeration

### Get logged in username
```bash
whoami
```

### Get id of logged in user
```bash
id
```

### Enumerate users on the system
```bash
cat /etc/passwd
ls -al /etc/passwd
```

### Check Hostname
```bash
hostname
```

### Operating system release and version
```bash
cat /etc/issue
cat /etc/os-release
uname -a
```

### Enumerate system processes
```bash
ps aux
```

### Look at ip
```bash
ifconfig
ip a
```

### Look at all active connections
```bash
ss -anp
```

### Find writable directories
```bash
find / -writable -type d 2>/dev/null
```

### Check mounted filesystems and available disks
```bash
cat /etc/fstab
mount
lsblk
```

### Finding History Files
```shell
find / -type f \( -name *_hist -o -name *_history \) -exec ls -l {} \; 2>/dev/null
```

### Find running proc
```shell
find /proc -name cmdline -exec cat {} \; 2>/dev/null | tr " " "\n"
```

### Installed packages
```shell
apt list --installed | tr "/" " " | cut -d" " -f1,3 | sed 's/[0-9]://g' | tee -a installed_pkgs.list
```

### Binaries
```shell
ls -l /bin /usr/bin/ /usr/sbin/
```

### Automated GTFOBINS checker
```shell
for i in $(curl -s https://gtfobins.github.io/ | html2text | cut -d" " -f1 | sed '/^[[:space:]]*$/d');do if grep -q "$i" installed_pkgs.list;then echo "Check GTFO for: $i";fi;done
```

### Trace system calls
```shell
strace ping -c1 10.129.112.20
```

### Find config files
```shell
find / -type f \( -name *.conf -o -name *.config \) -exec ls -l {} \; 2>/dev/null
```

### Find scripts
```shell
find / -type f -name "*.sh" 2>/dev/null | grep -v "src\|snap\|share"
```