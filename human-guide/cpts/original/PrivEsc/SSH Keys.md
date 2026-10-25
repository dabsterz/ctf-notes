


Check home directory of users using extended ls for .ssh directory and keys, remember to check the root directory as well
```bash
ls -al
```

If we are able to read the file, we can copy it over to our base kali and ssh into the server
```bash
vernonlim03@htb[/htb]$ vim id_rsa
vernonlim03@htb[/htb]$ chmod 600 id_rsa
vernonlim03@htb[/htb]$ ssh root@10.10.10.10 -i id_rsa

root@10.10.10.10#
```

### Create new SSH Keys

Can be done if there is no ssh keys present in the user home directory

```bash
ssh-keygen -f key
```
(-f flag is to specifically output the file)
