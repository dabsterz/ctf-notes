# DLL Hijacking


##### DLL Search order for Windows Machines (SafeDLL Search)
```
1. The directory from which the application loaded.
2. The system directory.
3. The 16-bit system directory.
4. The Windows directory. 
5. The current directory.
6. The directories that are listed in the PATH environment variable.
```

Get a list of installed applications
```powershell
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
```

Search up google/searchsploit for potential sus programs for DLL hijacking

Check for write privileges in the programs directories (just echo txt file)
