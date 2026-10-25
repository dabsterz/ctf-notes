
### Common Username conventions
![[Pasted image 20250429140747.png]]

### Use Username Anarchy to create a possible list
```shell
./cpts-tools/username-anarchy/username-anarchy -i /home/ltnbob/names.txt 
```

Then spray it with netexec
```shell
netexec smb 10.129.201.57 -u bwilliamson -p /usr/share/wordlists/fasttrack.txt
```