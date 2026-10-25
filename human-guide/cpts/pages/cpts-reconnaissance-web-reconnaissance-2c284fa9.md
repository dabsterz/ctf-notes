# Web Reconnaissance


| Technique               | Description                                                                 | Example                                                                                                      | Tools                                                                 | Risk of Detection                                                                 |
|-------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Port Scanning           | Identifying open ports and services running on the target.                  | Using Nmap to scan a web server for open ports like 80 (HTTP) and 443 (HTTPS).                               | Nmap, Masscan, Unicornscan                                           | High: Direct interaction with the target can trigger intrusion detection systems (IDS) and firewalls. |
| Vulnerability Scanning  | Probing for known vulnerabilities (outdated software/misconfigurations).    | Running Nessus against a web app to check for SQLi/XSS flaws.                                                | Nessus, OpenVAS, Nikto                                               | High: Exploit payloads may trigger security solutions.                            |
| Network Mapping         | Mapping network topology and device relationships.                          | Using traceroute to reveal network hops and infrastructure.                                                  | Traceroute, Nmap                                                     | Medium-High: Unusual traffic patterns may raise suspicion.                        |
| Banner Grabbing         | Retrieving service banner information.                                      | Connecting to port 80 to identify web server software/version.                                               | Netcat, curl                                                         | Low: Minimal interaction but may be logged.                                       |
| OS Fingerprinting       | Identifying the target's operating system.                                  | Using Nmap's -O flag to detect Windows/Linux.                                                                | Nmap, Xprobe2                                                        | Low: Generally passive, but advanced techniques may be detected.                  |
| Service Enumeration     | Determining specific service versions.                                      | Using Nmap's -sV to check for Apache 2.4.50/Nginx 1.18.0.                                                    | Nmap                                                                 | Low: Similar risk to banner grabbing.                                             |
| Web Spidering           | Crawling websites to discover pages/directories.                            | Using Burp Suite Spider to map website structure.                                                             | Burp Suite, OWASP ZAP, Scrapy                                        | Low-Medium: May trigger alerts if not mimicking human traffic.                    |
| Search Engine Queries   | Using search engines to uncover public target information.                  | Google searching "[Target] employees" for social media profiles.                                              | Google, DuckDuckGo, Shodan                                           | Very Low: Normal internet activity.                                               |
| WHOIS Lookups           | Retrieving domain registration details.                                     | Checking WHOIS records for registrant contact info.                                                           | whois command, online lookup services                                | Very Low: Legitimate DNS activity.                                                |
| DNS Analysis            | Examining DNS records for subdomains/infrastructure.                        | Using dig to enumerate target subdomains.                                                                     | dig, nslookup, dnsrecon                                              | Very Low: Essential internet function.                                            |
| Web Archive Analysis    | Reviewing historical website snapshots.                                     | Using Wayback Machine to find deleted pages.                                                                  | Wayback Machine                                                       | Very Low: Public archive access.                                                  |
| Social Media Analysis   | Gathering info from platforms like LinkedIn/Twitter.                        | Searching LinkedIn for employee roles/responsibilities.                                                       | LinkedIn, Twitter, OSINT tools                                       | Very Low: Public profile viewing.                                                 |
| Code Repository Analysis| Checking public repos for exposed data.                                     | Searching GitHub for target-related code/credentials.                                                         | GitHub, GitLab                                                       | Very Low: Normal repository browsing.                                             |

### WHOIS

```
whois inlanefreight.com
```


### DNS Analysis

###### DIG Command
```bash
#regular
dig google.com

#ptr record
dig -x google.com
```

###### Subdomain Enumeration

- DNS Zone Transfer
- Subdomain Brute Forcing
- Certificate Transparency (CT) Logs
- Search Engines (rmb to add site: )

```bash
dig axfr inlanefreight.htb @10.129.14.128
dig axfr internal.inlanefreight.htb @10.129.14.128
```

```bash
dnsenum --enum inlanefreight.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -r
gobuster dns -d inlanefreight.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt
```

###### Virtual Host Discovery

- RMB if this doesnt work it could be an entry needs to be added in /etc/hosts

```shell
gobuster vhost -u http://inlanefreight.htb:81 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt --append-domain
```

###### CT Logs
<https://crt.sh>

- This command fetches the JSON output from crt.sh for certificates matching the domain facebook.com
- jq -r '.[] | select(.name_value | contains("dev")) | .name_value': This part filters the JSON results, selecting only entries where the name_value field (which contains the domain or subdomain) includes the string "dev". The -r flag tells jq to output raw strings.
- sort -u: This sorts the results alphabetically and removes duplicates.

```shell
curl -s "https://crt.sh/?q=facebook.com&output=json" | jq -r '.[]
 | select(.name_value | contains("dev")) | .name_value' | sort -u
```

#### Fingerprinting

###### Banner Grabbing
```bash
curl -I inlanefreight.com
```

###### Wafw00f
- Detect the precense of a WAF
```shell
wafw00f inlanefreight.com
```

###### Nikto
```shell
nikto -h inlanefreight.com -Tuning b
```

#### Crawling

- robots.txt
- /.well-known/
- /.well-known/openid-configuration

###### Reconspider
```bash
python3 ReconSpider.py http://inlanefreight.com
```

#### Web Archives
<https://web.archive.org>

#### Recon Automation

```shell
./finalrecon.py --headers --whois --url http://inlanefreight.com
```

