# 80,443 http

**Editor correction:** directory fuzzing varies the URL path. The copied Host-header example and fixed response-size filter were corrected below; compare candidates with a missing-path response. The original vault snapshot is unchanged.


- Check URL address for clues such as .html .php
- Ctrl-U and check source for further clues like comments or file extensions
- Inspect element as well just to be sure

- Inspect the network tab for when requests are being sent (request headers and body)
- lookout for sitemap.xml and robots.txt

#### Nmap

```shell
sudo nmap -p80 -sC -sV 192.168.50.20
sudo nmap -p80 --script=http-enum 192.168.50.20
```

#### Directory/File Enumeration
```bash
gobuster dir -u http://10.10.10.121/ -w /usr/share/seclists/Discovery/Web-Content/common.txt

URL='http://challenge.example'  # replace with the challenge URL
printf '%s\n' admin api backup export > words.txt
ffuf -u "$URL/FUZZ" -w words.txt -mc all -ac -t 1 -rate 1 -maxtime 30
```

#### SubDomain Enumeration
```bash
gobuster dns -d inlanefreight.com -w /usr/share/SecLists/Discovery/DNS/namelist.txt

ffuf -u http://siteisup.htb -H "Host: FUZZ.siteisup.htb" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -fs 1131
```

#### Banner Grabbing/Web Server Headers
```bash
curl -IL https://www.inlanefreight.com
whatweb 10.10.10.121
whatweb --no-errors 10.10.10.0/24
```

#### Firefox (Browse to IP)
Don't forget to do this and hit CTRL-U

#### CURL
```bash
curl http://10.129.42.190
```


#### Nikto
```shell
nikto -h <ip>
```

#### CEWL
<https://github.com/digininja/CeWL>


Additional Steps 
- View SSL/TLS Certificate
- Robots.txt
- View Source Code
- Add discovered domain into /etc/hosts

#### Burp

- to bypass client side validation
- Use repeater to keep repeating the sent request by manually changing
- Use intruder to automate the attack
- rmb to toggle foxyproxy

#### API Enumeration

- Often has ```/api_name/v1``` naming convention

Create the pattern first
```shell
{GOBUSTER}/v1
{GOBUSTER}/v2
```

Launch gobuster
```shell
gobuster dir -u http://192.168.50.16:5002 -w /usr/share/wordlists/dirb/big.txt -p pattern
```

We can then proceed to curl the found api endpoints to enumerate it further
```shell
curl -i http://192.168.50.16:5002/users/v1

#adding payload and changing to PUT
curl -X 'PUT' \
  'http://192.168.50.16:5002/users/v1/admin/password' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: OAuth eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDkyNzE3OTQsImlhdCI6MTY0OTI3MTQ5NCwic3ViIjoib2Zmc2VjIn0.OeZH1rEcrZ5F0QqLb8IHbJI7f9KaRAkrywoaRUAsgA4' \
  -d '{"password": "pwned"}'
```


