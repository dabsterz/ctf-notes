# Domain Discovery

1. Check SSL Certificate of Company's main website
2. Use https://crt.sh to look up for subdomains

#### CURL
```bash
curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u
```
```bash
for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done
```
(checks which domains are accessible on the internet)

#### Shodan
```shell
vernonlim03@htb[/htb]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f4 >> ip-addresses.txt;done
vernonlim03@htb[/htb]$ for i in $(cat ip-addresses.txt);do shodan host $i;done
```

#### Checking DNS Records
```shell
dig any inlanefreight.com
```
