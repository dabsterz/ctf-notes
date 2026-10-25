# Password Hunting

### CeWL (generate passwords on a website)

```shell
cewl https://www.inlanefreight.com -d 4 -m 6 --lowercase -w inlane.wordlist
wc -l inlane.wordlist
```

- -d  (to specify the depth to spider)
- -m (to specify minimum length of the word)
- -w (store results where)

## HashCat (mutate passwords based on custom rule)

```shell
hashcat --force password.list -r custom.rule --stdout | sort -u > mut_password.list
```



## Default Credentials - CSV DUMP
<https://github.com/ihebski/DefaultCreds-cheat-sheet/blob/main/DefaultCreds-Cheat-Sheet.csv>
