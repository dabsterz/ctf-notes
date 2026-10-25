# 3389 rdp

Basic Commands
```shell
nmap -sV -sC 10.129.201.248 -p3389 --script rdp*
nmap -sV -sC 10.129.201.248 -p3389 --packet-trace --disable-arp-ping -n
sudo cpan
```

RDP Security check
```bash
#In cpts-tools/rdp-sec-check
./rdp-sec-check.pl 10.129.201.248
```

RDP Initiation command
```shell
xfreerdp /u:cry0l1t3 /p:"P455w0rd!" /v:10.129.201.248
```
