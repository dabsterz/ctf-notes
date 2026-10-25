# Services Automatically Started on Boot


Trial command

```cmd
wmic service get name,displayname,pathname,startmode |findstr /i "auto" 
|findstr /i /v "c:\windows\\" |findstr /i /v """ 
```
