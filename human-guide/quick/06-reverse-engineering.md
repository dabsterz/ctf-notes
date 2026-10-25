# Reverse engineering

Run recipes from the extracted guide root (the folder containing `recipes`). Use supplied artifacts; [event rules](../COMPETITION.md). Tools: [chooser](../TOOL-CHOOSER.md#reverse-engineering).

## Quick: enter the correct environment

**Windows native · PowerShell**

```powershell
wsl --list --verbose
wsl
```

**Windows WSL · Bash**

```bash
command -v python3 gdb objdump strings xxd
python3 --version
```

**Look for:** installed paths; Ghidra also belongs to WSL.
**If not:** use Kali radare2; native Windows uses x64dbg/dnSpyEx.

## Quick: identify the file and search strings

**Windows WSL · Bash**

```bash
read -r -p 'Local binary path: ' FILE
objdump -f "$FILE"
objdump -x "$FILE" > headers.txt
strings -a -t x "$FILE" > strings.txt
xxd -l 32 "$FILE"
```

**Look for:** architecture, imports, success/failure strings; open `strings.txt` in your editor.
**If not:** try wide strings with `strings -a -e l "$FILE"`; packed strings may appear only at runtime.

## Quick: follow callers in radare2

**Kali · Bash**, then **radare2 prompt** ([command reference](https://book.rada.re/refcard/intro.html)).

```bash
read -r -p 'Local binary path: ' FILE
r2 "$FILE"
```

```text
aaa
ii
izz
afl
pdf @ main
```

**Look for:** comparison imports and the branch reaching success.
**If not:** run `ie`; inspect entry-point calls when `main` is stripped. Use `axt @` followed by an exact import flag from `ii`.

## Quick: read the checker in a decompiler

**Windows WSL · Ghidra GUI:** File → New Project → Non-Shared Project → File → Import File → select binary → open → Analyze → Search → For Strings → select success text → Show References to → open caller in Decompiler.

**Look for:** input length, byte width, operation order, key array and comparison array; follow each array address into Listing.
**If not:** inspect Listing instructions; inferred types can hide truncation and signedness.

## Quick: turn observed constants into helper input

**Windows WSL · illustrative example**, not a solved unknown binary:

```c
uint8_t key[2] = {0x31, 0x72};       // key_hex: 3172
uint8_t expected[4] = {194,124,224,120};
for (i = 0; i < 4; i++) {
    uint8_t x = input[i] ^ key[i % 2];
    out[i] = (uint8_t)((x << 1) | (x >> 7)); // ROL8: rotation 1
}
ok = memcmp(out, expected, 4) == 0;
```

```bash
cat > checker-example.json <<'JSON'
{"key_hex":"3172","rotation":1,"expected":[194,124,224,120]}
JSON
python3 recipes/transform.py checker-example.json --out example-plain.bin
xxd example-plain.bin
```

**Look for:** `PLAN` and a passing forward check. Copy your binary's actual bytes into equivalent JSON.
**If not:** this helper handles only repeated-key XOR followed by byte rotation; addition, permutations or state need another model.

## Quick: inspect comparison buffers live

**Windows WSL · compatible Linux x86-64 ELF; Bash**, then **GDB**.

```bash
read -r -p 'Local ELF path: ' FILE
gdb -nx -q "$FILE" -ex 'break memcmp' -ex run
```

```text
bt
info registers rdi rsi rdx
x/16bx $rdi
x/16bx $rsi
```

**Look for:** relevant caller, two buffers and comparison length in RDX; inspect only readable bytes ([GDB memory](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Memory.html)).
**If not:** inline/custom comparisons need a breakpoint at their instruction; Windows x64 uses RCX/RDX/R8.

## Quick: find missing files or runtime checks

**Kali · Bash; executes the selected local binary.**

```bash
read -r -p 'Executable path (include ./ or use absolute): ' FILE
ltrace -s 128 -o library.log "$FILE"
strace -f -s 128 -o syscalls.log "$FILE"
rg -n 'memcmp|strcmp|open|read|ptrace|mprotect' library.log syscalls.log
```

**Look for:** actual comparison values, required companion files and failed opens.
**If not:** static linking/inlining can hide library calls; follow the check in the debugger.

## Quick: switch to the format-specific reader

**Windows native · dnSpyEx:** File → Open → select .NET assembly → expand assembly/types → inspect entry point → follow comparison method.

**Kali · Android GUI**

```bash
read -r -p 'Local APK path: ' FILE
jadx-gui "$FILE"
```

**Look for:** input handler and success-string usages; verify the recovered candidate against the original checker.
**If not:** native `.so` checks need Ghidra/radare2; transformed bytes alone are not the answer.
