# nmap


 Full and thorough scan
```bash
nmap -sV -sC -p- -v 10.129.42.253
```

 Specific Scripts
```bash
 locate scripts/citrix
 nmap --script <script name> -p<port> <host>
```

 Banner Grabbing
```bash
 nmap -sV --script=banner <target>
 nmap -sV --script=banner -p21 10.10.10.0/24
```

Output to file flags
- Normal output (`-oN`) with the `.nmap` file extension
- Grepable output (`-oG`) with the `.gnmap` file extension
- XML output (`-oX`) with the `.xml` file extension
- ALL of the above (-oA)
```bash
sudo nmap 10.129.2.28 -p- -oA target
```

Viewing in browser with stylesheet
```bash
xsltproc target.xml -o target.html
firefox target.html
```


#### Useful Flags
```bash
--stats-every=5s (Updates console every 5 seconds of progress)

-v (verbose)

-vv (OMEGA verbose)

-T1 to -T5 (Speed)

-sS (stealth scan)

-sU (UDP scan)

-sV (Probe open ports for service/version)

-p (scans top 1000 ports if left blank or you can specify range)

-p- (scans all 65535 ports)

-O (gets operating system information)

-A (basically -O, -sV, -sC, Traceroute) all in one

--packet-trace (show all packets sent and received)
```

#### Firewall Evasion Techniques

Send ACK packet only
```bash
sudo nmap 10.129.2.28 -p 21,22,25 -sA -Pn -n --disable-arp-ping --packet-trace
```
Decoy scan
```bash
sudo nmap 10.129.2.28 -p 80 -sS -Pn -n --disable-arp-ping --packet-trace -D RND:5
```
Scan using different source IP
```bash
sudo nmap 10.129.2.28 -n -Pn -p 445 -O -S 10.129.2.200 -e tun0
```
DNS Proxying
```bash
sudo nmap 10.129.2.28 -p50000 -sS -Pn -n --disable-arp-ping --packet-trace --source-port 53

ncat -nv --source-port 53 10.129.2.47 50000
```

