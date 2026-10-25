# Search for flag on compromised system


#### Linux
```bash
find / -type f -iname "flag.txt" 2>/dev/null
find / -type f -iname "local.txt" 2>/dev/null
find / -type f -iname "proof.txt" 2>/dev/null
find / -type f -iname "user.txt" 2>/dev/null
find / -type f -iname "root.txt" 2>/dev/null
```

#### Windows
```cmd
dir /r /s c:\*local.txt
dir /a /s c:\*proof.txt
Get-ChildItem -Path C:\ -Recurse -Force -Filter *local*.txt
Get-ChildItem -Path C:\ -Recurse -Force -Filter *proof*.txt
```

