1. compare.json contains constants extracted from a checker: stored[i] = ROL8(input[i] XOR repeated_key[i], rotation). Recover and verify input.
2. machine.json gives the decoded instructions of a one-byte VM. Recover its accepted input.
3. register.txt contains the crash bytes. Recover and verify the offset.
4. Given an unfamiliar stripped ELF executable, find instructions to locate the input comparison and derive the constants yourself; no binary is supplied, assess whether the guide actually bridges this gap.
