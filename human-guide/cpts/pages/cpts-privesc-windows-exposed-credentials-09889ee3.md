# Exposed Credentials


```
history (linux)

PSReadLine (Windows)
Get-History
(Get-PSReadlineOption).HistorySavePath
type history.txt
```

#### Windows
```powershell
#Search for stored passwords
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include *.txt,*.ini -File -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path C:\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx -File -Recurse -ErrorAction SilentlyContinue
```

```cmd
findstr /si password *.txt *.ini *.config*
```

