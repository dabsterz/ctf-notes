# Crontabs (Scheduled Tasks)


1. Add new scheduled tasks/cron jobs
2. Trick them to execute a malicious software

Check if we have write privileges on these directories
```bash
ls -al /etc/cron*

crontab -l

cat /etc/crontab
ls -al /etc/cron.d
cat /var/spool/cron/crontabs/root

find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null
```

Inspect cron log file for running cron jobs
```bash
grep "CRON" /var/log/syslog
```

Use pspy to do a live monitoring of running processes
```bash
./pspy32
(rmb to look at the uid to see who is running the command uid=0 is root)

./pspy64 -pf -i 1000
#(The -pf flag tells the tool to print commands and file system events and -i 1000 tells it to scan procfs every 1000ms (or every second))
```
## REMEMBER to cat and ls -al sus cron jobs 

If we can write to a directory called by a cron job, we can write a bash script with a reverse shell command, which should send us a reverse shell when executed.


