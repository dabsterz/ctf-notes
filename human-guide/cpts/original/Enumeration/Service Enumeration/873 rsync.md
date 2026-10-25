Basic Commands
```shell
sudo nmap -sV -p 873 127.0.0.1
nc -nv 127.0.0.1 873
rsync -av --list-only rsync://127.0.0.1/dev
```

Sync files 
```bash
rsync -av rsync://127.0.0.1/dev

#if rsync is configured to use ssh to transfer files
rsync -av rsync://127.0.0.1/dev -e "ssh -p2222"
```