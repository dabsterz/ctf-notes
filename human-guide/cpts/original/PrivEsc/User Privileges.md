
Check for what sudo privileges we have
```bash
sudo -l
```

Check if we can change to root (if lucky)
```bash
sudo su -
```

Running sudo as another user
```bash
vernonlim03@htb[/htb]$ sudo -u user /bin/echo Hello World!

    Hello World!
```

Change user command
```bash
sudo -su user2
```

#### GTFOBins

If there is a service that is capable of running as the root user, check GTFOBins for it
https://gtfobins.github.io/


#### LOLBAS

Contains a list of Windows applications which we may be able to leverage to perform certain functions, like downloading files or executing commands in the context of a privileged user
https://lolbas-project.github.io/#