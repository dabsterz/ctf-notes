# Round 2 assigned tasks

1. checker.json gives expected[i] = ROL8(input[i] XOR repeated key[i], rotation). Recover input and verify forward.
2. crash.bin is four bytes in memory order from the guide pattern; the input sent was 512 bytes. Find and verify the offset.
3. vm.json contains a straight-line 8-bit input-check VM. LOAD_INPUT loads one byte; XOR and ADD modify it; CMP must match; HALT ends. Recover input.
4. Choose an approved static Windows/WSL alternative to radare2; compare tools for native, .NET and Android binaries.
