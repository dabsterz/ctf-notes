
#### Dig Command
- the most basic dns query command
![[Pasted image 20250401192631.png]]
```bash
dig soa www.inlanefreight.com
dig ns inlanefreight.htb @10.129.14.128
```

#### DNS server version query
```shell
dig CH TXT version.bind 10.129.120.85
```

#### List all available DNS Records (almost all)
```shell
dig any inlanefreight.htb @10.129.14.128
```
#### Dig AXFR Zone Transfer
```shell
dig axfr inlanefreight.htb @10.129.14.128
dig axfr internal.inlanefreight.htb @10.129.14.128
```

#### Subdomain Bruteforcing
```shell
for sub in $(cat /opt/useful/seclists/Discovery/DNS/subdomains-top1million-110000.txt);do dig $sub.inlanefreight.htb @10.129.14.128 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done

dnsenum --dnsserver 10.129.42.195 -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt inlanefreight.htb

```

DNS Abbreviations

| Abbv | Meaning                         |
| ---- | ------------------------------- |
| FQDN | Fully Qualified Domain Name     |
| AXFR | Asynchronous Full Transfer Zone |



Default Config Files (bind9)
- `named.conf.local`
- `named.conf.options`
- `named.conf.log`
-  all can be found in the /etc/bind directory 