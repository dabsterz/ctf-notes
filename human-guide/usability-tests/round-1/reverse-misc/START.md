# Test brief
You have three independent local practice tasks. Use only the human guide as your technical reference.
1. checker.json describes the byte transform extracted from a native checker. Recover its accepted ASCII input. For each input byte x at position i: y=ROL8(x XOR key[i % key_length], 3); compare y with expected[i].
2. crash.bin contains four bytes copied in increasing memory-address order from a corrupted return slot. The input was generated with the exact de_bruijn(b'abcdefgh',4) pattern in the human guide, truncated to 512 bytes. Find the offset.
3. payload.json is a short custom VM program. It starts with accumulator zero and has instructions: LOAD byte, XOR byte, ADD byte (wrap at 8 bits), CMP byte, HALT. Determine the required input byte and verify the comparison. The program reads your input through LOAD_INPUT (no operand).
Common lookup: you are at the Windows workstation, need radare2, and cannot find it in WSL. Determine which supplied environment lists radare2 and name one listed local alternative for static reverse engineering on Windows/WSL.
