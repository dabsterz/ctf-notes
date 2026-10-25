# Advanced Domain Enumeration


### Windapsearch
```shell
cd cpts-tools/windapsearch
python -m venv myfirstproject
source myfirstproject/bin/activate
pip3 install python-ldap

#Domain Admins
python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 --da

#Privileged Users
python3 windapsearch.py --dc-ip 172.16.5.5 -u forend@inlanefreight.local -p Klmcargo2 -PU
```

### Bloodhound
```shell
sudo bloodhound-python -u 'forend' -p 'Klmcargo2' -ns 172.16.5.5 -d inlanefreight.local -c all 

.\SharpHound.exe -c All --zipfilename ILFREIGHT
```
On Kali 2024
```shell
sudo neo4j start
bloodhound
(neo4j/neo4j1)
```
