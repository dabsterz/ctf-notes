# Password Policy Discovery

#### Using rpcclient
```shell
rpcclient -U "" -N 172.16.5.5
rpcclient $> querydominfo
rpcclient $> getdompwinfo
```

#### Using enum4linux
```shell
enum4linux -P 172.16.5.5
enum4linux-ng -P 172.16.5.5 -oA ilfreight #use this for output
```

#### Using ldapsearch
```shell
ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "*" | grep -m 1 -B 10 pwdHistoryLength
```

### net.exe (from windows cmd)
```cmd
net accounts
```

#### Using PowerView (from windows powershell)
```powershell
import-module .\PowerView.ps1
Get-DomainPolicy
```
