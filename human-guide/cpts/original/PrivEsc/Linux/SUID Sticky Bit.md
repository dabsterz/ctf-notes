
Look for sticky bit commands
```bash
find / -perm -u=s -type f 2>/dev/null
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null
```

Suspicious binary with the flag hiding inside
```bash
strings /usr/bin/passwd_flag
cat /usr/bin/passwd_flag
```

If not then go https://gtfobins.github.io/




Enumerate capabilities using getcap
```bash
/usr/sbin/getcap -r / 2>/dev/null
find /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin -type f -exec getcap {} \;
```
![[Pasted image 20250529150333.png]]

If there are any sus binaries just search https://gtfobins.github.io/

