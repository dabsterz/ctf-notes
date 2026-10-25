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

## Full reference

<details class="deep-reference" markdown="1">
<summary>Explanations, advanced cases and sources</summary>

# Reverse engineering: turn a program into a checkable explanation

**Quick route:** [Short commands](../QUICKSTART.md#static-reversing) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#reverse-engineering). Use this chapter for deeper explanations.

Your first deliverable is a sentence such as “the program XORs each input byte with a repeating key, rotates it, and compares the result with this table.” Once that sentence is accurate, writing a solver is usually straightforward. A decompiler's output is a hypothesis; the bytes and a repeatable run are the evidence.

This chapter is for human, local analysis of supplied challenge files. The event prohibits AI assistance and public online analysis, decompilation, and compilation services. Prepared notes and scripts are expressly allowed by PDF p.7. Do not upload binaries to a comparison site. Work only on the challenge targets assigned to your team.

## 1. Choose the correct machine before choosing a command

The workbook describes two separate environments. A tool listed under Windows with installation location WSL is not a Windows executable and is not automatically available in Kali.

| Route | Approved tools relevant here | Practical use |
| --- | --- | --- |
| **Windows native** | x64dbg (Windows row 40), HxD (42), Notepad++ (44), dnSpyEx (45) | PE debugging, byte inspection, managed .NET analysis |
| **Windows WSL** | Python 3 (14), GDB (16), objdump (17), strings (18), Ghidra (29), llvm-mc (34), xxd (35) | ELF analysis, local decompilation, small scripts |
| **Kali** | radare2 (123), Frida (53), angr (13), GCC/build tools (54), ltrace (90), strace (145), UPX (156), jadx (79), Apktool (15) | ELF triage, instrumentation, APK extraction, local practice builds |
| **Kali, specialized** | GoReSym (62), pycdc (117), pyinstxtractor-ng (118), uncompyle6 (152), unpyc3 (153), Cutter (31), BinDiff (19) | Language and packaging specific follow-up |

Kali tools were installed on a best-effort basis; operation is not guaranteed. Python 3.11's Kali row 121 records no installation information. Check the interpreter actually present before running a Python example. Windows WSL Python is the reliable workbook-backed route for the standard-library scripts below.

**Windows native, PowerShell: enter the supplied WSL distribution.**

```powershell
wsl --list --verbose
wsl
```

**Windows WSL, Bash: check the listed tools without installing anything.**

```bash
command -v python3 gdb objdump strings xxd
python3 --version
gdb --version
```

**Kali, Bash: check the separate tool set.**

```bash
command -v r2 rabin2 python3 frida strace ltrace gcc
r2 -v
python3 --version
```

If a command is missing, use a listed alternative or the other supplied environment. PDF p.5 permits non-AI libraries/plugins/dependencies in both environments, subject to [named exclusions](../COMPETITION.md#what-is-allowed). This chapter's core route needs no extra Python package.

IDA Free and Binary Ninja Free are in the unapproved sheet. MCP servers and AI plugins are out of scope. WinDbg, Scylla/x64dbg plugins, de4dot, online decompilers, and online analysis services are also excluded by the workbook. The approved x64dbg application does not imply approval of every extension.

## 2. Preserve the file and identify its format

Use `chall` below for a local challenge file placed in your working directory. Keep the original untouched; make a separate copy before patching. Record its hash, format, architecture, input channel, and your first observed output.

**Windows native, PowerShell:**

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\chall
Copy-Item -LiteralPath .\chall -Destination .\chall.work
Format-Hex -Path .\chall
```

**Windows WSL, Python standard library:**

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib
p = Path('chall')
data = p.read_bytes()
print('size:', len(data))
print('sha256:', hashlib.sha256(data).hexdigest())
print('first 32 bytes:', data[:32].hex(' '))
PY
```

Interpret the header before running it: `7f 45 4c 46` is ELF; `4d 5a` begins a DOS/PE family file; `00 61 73 6d` is WebAssembly; ZIP containers start with `50 4b` and may be APK, JAR, HAP, or an ordinary archive. A file extension alone proves none of these. An `MZ` stub may itself contain the challenge, so do not automatically discard it.

**Windows WSL:**

```bash
objdump -f chall
objdump -x chall > headers.txt
strings -a -t x chall > strings.txt
python3 - <<'PY'
from pathlib import Path
for line in Path('strings.txt').read_text(errors='replace').splitlines():
    if any(word in line.lower() for word in ('flag', 'correct', 'wrong', 'password', 'usage')):
        print(line)
PY
```

**Kali:**

```bash
file chall
rabin2 -I chall
rabin2 -S chall
rabin2 -zz chall > strings.txt
rg -in 'flag|correct|wrong|password|usage' strings.txt
```

Save full output; a filtered display is an index into it. No matching string means only that this search found none. Packed data, wide strings, runtime decoding, and a different flag format can all hide a useful string. `rabin2 -zz` reports physical and virtual addresses: a file offset is not a runtime address.

| Observation | Next action | Why |
| --- | --- | --- |
| Plaintext candidate flag | Find references and test the candidate against the original | A decoy string is cheap to plant |
| `strcmp`/`memcmp` imported | Find callers, then stop before the relevant call | Comparison arguments may reveal the actual check |
| Few imports and high-entropy sections | Inspect entry point, memory allocation and writes | A loader may create the real code at runtime |
| ELF sections rejected but program headers sensible | Inspect load segments; analyze a repaired copy only | The loader uses segments; corrupt sections can mislead tools |
| Native architecture does not match the host | Continue statically | A foreign ELF cannot run merely because it is executable |
| .NET metadata / CLR header | Open in native dnSpyEx | Managed methods are more informative than native startup stubs |

## 3. A complete small checker to practice on

This local toy accepts four bytes on standard input. It gives you a known reference for practicing strings, cross-references, decompilation, and comparison breakpoints. Save as `checker.c` using an approved editor.

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    unsigned char input[32] = {0};
    const unsigned char key[] = {0x31, 0x72};
    const unsigned char expected[] = {0x61, 0x3f, 0x72, 0x3f};
    unsigned char out[4];
    if (!fgets((char *)input, sizeof input, stdin)) return 2;
    size_t n = strcspn((char *)input, "\r\n");
    if (n != 4) { puts("wrong length"); return 1; }
    for (size_t i = 0; i < 4; i++)
        out[i] = (unsigned char)((input[i] ^ key[i % 2]) + i);
    if (memcmp(out, expected, 4) == 0) puts("correct");
    else puts("wrong");
    return 0;
}
```

**Kali, approved GCC; local practice only:**

```bash
gcc -O0 -g -fno-builtin -o checker checker.c
printf 'AAAA\n' | ./checker
printf 'PLAN\n' | ./checker
```

Expected output is `wrong`, then `correct`. This compiler command is not asserted available in Windows WSL. A compiled Linux file may be inspected statically there; execution also requires a compatible loader and libc.

**Windows WSL Python, or Kali with Python confirmed:**

```bash
python3 - <<'PY'
key = bytes([0x31, 0x72])
expected = bytes([0x61, 0x3f, 0x72, 0x3f])
answer = bytes(((b - i) & 0xff) ^ key[i % len(key)]
               for i, b in enumerate(expected))
reencoded = bytes(((b ^ key[i % len(key)]) + i) & 0xff
                  for i, b in enumerate(answer))
assert reencoded == expected
print(answer.decode('ascii'))
PY
```

The output is `PLAN`. Subtraction must happen before XOR because the checker applies XOR before addition. The round-trip assertion tests the inversion, while running the original checks the input length, newline handling, and surrounding logic.

## 4. Follow a check with radare2 on Kali

The following is an interactive **Kali radare2** session. `checker` is the toy above; for a real target, substitute its filename and use the names or addresses actually printed by the tool.

```text
r2 checker
aaa
iI
ii
izz~correct
afl
pdf @ main
```

`aaa` performs analysis; `afl` lists recognized functions; `pdf` disassembles a function. Find the call to `memcmp` and the conditional branch after it. `test eax,eax` followed by a zero/nonzero branch commonly checks a C comparison result. Follow both destinations and identify which prints `correct`. The presence of one apparent success branch does not establish that it is the final check.

**Kali radare2, continue in the same session:**

```text
axt @ sym.imp.memcmp
pdf @ main
agf @ main
q
```

`axt` lists incoming references; `agf` shows a function graph. If your imported name differs, copy its exact flag from `ii`. If `main` is absent, use `ie` for entry points, `afl` for candidates, and inspect the startup routine's call target. A stripped executable has fewer names, not less machine code.

For a string reference, copy the **virtual address** from `izz`, then use `axt @ ADDRESS`, replacing `ADDRESS` with that number. Use `pdf @ FUNCTION` for the containing function. The placeholder is deliberately not a universal address.

**Kali, save reusable static output:**

```bash
r2 -q -c 'aaa;aflj' checker > functions.json
r2 -q -c 'aaa;pdf @ main' checker > main.asm
r2 -q -c 'izzj' checker > strings.json
```

Do not add `-d` for static work: it starts a debug process. `-w` opens a writable file and is unnecessary for inspection. If analysis is wrong, inspect bytes with `px 32 @ ADDRESS`, disassemble a bounded region with `pd 12 @ ADDRESS`, and correct function boundaries only after checking where execution actually enters. Command meanings are documented in the [official radare2 reference card](https://book.rada.re/refcard/intro.html).

For JSON, check the decoded value's type and length. A failed command can produce an empty value rather than the list you expected. A `json.loads` error may mean diagnostic output polluted stdout, not that the binary has no functions. The optional `r2pipe` library is not individually listed; batch output above needs no plugin.

## 5. Read decompiled code without trusting invented types

**Windows WSL Ghidra:** launch the supplied Ghidra application, create a local non-shared project, import `chall`, and check the detected language, bitness, endianness, and image base before accepting analysis. Open **Search → For Strings**, select a relevant message, and follow its references into the function. Keep Listing and Decompiler panes visible together.

Rename `local_28` to a factual name such as `input_buffer` only after you have identified its use. Rename an unknown function to `candidate_transform` before claiming it is AES. Set array lengths from actual bounds, distinguish a byte count from an element count, and check signed comparisons in the assembly. Save your project separately from the original file.

| Decompiled appearance | Verify in instructions |
| --- | --- |
| `char` becomes negative | `movsx` sign-extends; `movzx` zero-extends |
| Arithmetic looks unbounded | Register width and truncation at each store |
| `memcmp` arguments appear missing | Calling convention, register assignments before the call, function prototype |
| Impossible branch | Flags, unsigned versus signed jump, or earlier mutation |
| Huge single function | Flattened dispatcher, bad boundaries, exception flow, or VM interpreter |
| No ordinary calls | Tail jumps, return chains, callbacks, destructors, signal handlers |

Ghidra in the Windows sheet is installed **in WSL**. Its presence there does not establish a Kali installation. Kali's approved radare2 provides the static fallback. `pdg` requires an r2ghidra plugin; radare2 approval alone is not proof that plugin exists. Use `pdf` immediately if it is absent. PDF p.5 allows non-AI plugins subject to named exclusions, but installation and compatibility may cost more time than this fallback.

## 6. Stop immediately before the comparison

**Windows WSL GDB, Linux x86-64 checker:**

```bash
gdb -q ./checker
```

```text
set disassembly-flavor intel
break main
run
disassemble /r main
break memcmp
continue
```

Enter `AAAA` when the program asks for input. At the relevant `memcmp` call, inspect arguments:

```text
info registers rdi rsi rdx rip
x/4bx $rdi
x/4bx $rsi
bt
```

On Linux x86-64 System V, these registers hold the first pointer, second pointer, and length. For this toy the second buffer should be `61 3f 72 3f` and the length 4. Those bytes are **transformed expected data**, not automatically the plaintext answer. Check the call site if other library calls also hit the breakpoint.

On Windows x64, the first arguments are RCX, RDX, R8, R9. On i386 cdecl they are on the stack; immediately before `call`, argument one is at `[esp]`, and at callee entry it is at `[esp+4]`. On ARM A32 use r0–r3; AArch64 uses x0–x7. Register assumptions must match the ABI, not just the CPU family.

For PIE, first `start` or `starti`, inspect `info proc mappings`, and derive the runtime address from the loaded image plus the correct relative offset. With symbols, `break *main+OFFSET` is convenient; replace `OFFSET` with an instruction offset from this binary. Never copy a raw address from an earlier run with ASLR enabled. The [GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb) documents breakpoints, memory inspection, and process mappings.

**Windows WSL GDB, useful follow-up commands:**

```text
nexti
stepi
finish
info registers
x/16i $pc
x/32bx $sp
```

`nexti` steps over a call; `stepi` enters it; `finish` runs until the current frame returns. If you need to discover who changes a known byte, set `watch *(unsigned char*)ADDRESS` after replacing `ADDRESS` with the live pointer. Watchpoints are limited resources; watch the meaningful field rather than an entire megabyte.

**Windows native x64dbg:** open a copy of the PE using the matching x32dbg or x64dbg executable, follow the entry point, and find the local comparison or imported comparison routine from the Symbols view. Set a breakpoint, run to it, and inspect the ABI argument registers in Dump. Use a hardware breakpoint on a changed byte when a software `INT3` breakpoint would modify self-checked code. Do not assume hardware breakpoints are invisible to the program.

## 7. When tracing reveals more than decompilation

**Kali, only for a local executable you intend to run:**

```bash
ltrace -s 256 -o library.log ./chall
strace -f -s 256 -o syscalls.log ./chall
rg -n 'strcmp|memcmp|open|read|write|ptrace|mprotect|execve' library.log syscalls.log
```

`ltrace` can expose imported function arguments; static linking, inlining, direct syscalls, or custom routines can hide them. `strace` shows kernel interactions, including child processes with `-f`. Neither tool proves that a missing call never occurred through another implementation. A file-open failure can reveal the expected working directory or companion filename.

**Kali Frida:** use this observation-only script when the binary imports `memcmp`. Save it as `compare.js`.

```javascript
const address = Module.findGlobalExportByName('memcmp');
if (address === null) {
  console.log('memcmp is not exported in this process');
} else {
  Interceptor.attach(address, {
    onEnter(args) {
      const length = args[2].toUInt32();
      if (length === 0 || length > 128) return;
      try {
        console.log('length=' + length);
        console.log(hexdump(args[0], { length: length, ansi: false }));
        console.log(hexdump(args[1], { length: length, ansi: false }));
      } catch (error) {
        console.log('unreadable comparison: ' + error);
      }
    }
  });
}
```

```bash
frida -f ./chall -l compare.js
```

Enter the challenge input through the terminal as appropriate for the supplied Frida CLI. Check `frida --help` if its process/input behavior differs. If the library loads later, attach after it is mapped or observe module loading; do not silently accept “no export” as “no comparison.” The script uses the current API spelling from [Frida's JavaScript documentation](https://frida.re/docs/javascript-api/).

## 8. Write down the transform before solving it

Use a table with one row per stage: source bytes, operation, width, key/state, destination. Keep the exact comparison direction: `transform(input) == stored` requires inversion, while `input == transform(stored)` requires forward evaluation.

**Windows WSL Python; Kali after interpreter check:**

```python
def rol8(value, amount):
    amount %= 8
    return ((value << amount) | (value >> ((8 - amount) % 8))) & 0xff

def ror8(value, amount):
    return rol8(value, -amount)

for value in range(256):
    for amount in range(8):
        assert ror8(rol8(value, amount), amount) == value
print('all byte rotations round-trip')
```

For XOR, applying the same key again reverses it. For addition modulo 256, subtract and mask. Reverse a permutation with the inverse index map. For a stateful cipher, restore the complete state before testing the next candidate; reusing mutated state creates plausible-looking wrong output. A non-bijective substitution can have several preimages: retain all candidates until later constraints eliminate them.

A repeated prefix hash can permit byte-by-byte search if each prefix digest is independently known. A single full cryptographic hash generally does not. A branch count or timing oracle must first show a consistent relationship to correct prefixes, with repeated baselines and randomized candidate order. Avoid treating the slowest single run as proof.

### Mixed Boolean-arithmetic expressions

Expressions such as `(x ^ y) + 2*(x & y)` implement `x+y` at a fixed width. Simplifying them can reveal an ordinary checksum hidden in a large expression. Record the width and signedness, simplify one expression, then compare original and replacement on boundary values and many random inputs. Random agreement is a useful check, not a mathematical proof of equivalence. For small widths, exhaustive checking is stronger.

**Windows WSL Python, complete 8-bit check:**

```python
for x in range(256):
    for y in range(256):
        original = ((x ^ y) + 2 * (x & y)) & 255
        replacement = (x + y) & 255
        assert original == replacement
print('equivalent for all 8-bit pairs')
```

The source's msynth/Miasm workflow is a specialized option, not a required installed tool. The manual identity and equivalence check survive without it. Solver-backed synthesis, deobfuscation plugins, and an oracle database each have separate availability requirements.

## 9. Anti-analysis: preserve the real semantics

Start by comparing one normal run with one instrumented run using the same input. Locate the first meaningful divergence. Patching every conditional jump can make a validator print success without recovering the answer.

| Evidence | Human investigation | Common wrong conclusion |
| --- | --- | --- |
| `ptrace`, `TracerPid`, PEB flags | Identify the exact return value or branch consumed | All anti-debugging is a single imported function |
| Time or instruction-counter state | Determine whether time changes the key or merely gates progress | Skipping a delay preserves cryptographic state |
| SIGILL/SIGFPE/SIGTRAP handlers | Trace handler and saved context changes | The first signal is an ordinary crash |
| Parent and child processes | Follow both and inspect writes between them | The child on disk contains its final instructions |
| Writes to executable pages | Dump after decoding, before erasure | A static disassembly describes every later instruction |
| TLS callbacks / constructors / destructors | Analyze startup and teardown too | All validation occurs under `main` |
| Stack-based call-less chaining | Follow saved frame and return pointers | No `call` instruction means no function dispatch |

**Windows WSL GDB, only after proving a handler is intended:**

```text
info signals SIGILL SIGFPE SIGTRAP
handle SIGILL nostop noprint pass
handle SIGFPE nostop noprint pass
set follow-fork-mode child
set detach-on-fork off
info inferiors
```

Do not broadly pass SIGTRAP without understanding debugger breakpoints. Signal-driven code may mutate instructions, adjust the saved PC, or switch decoding modes. For a parent that writes the child's text with `process_vm_writev`, Kali `strace -f` can expose the mechanism; exact dumped bytes may require a larger recorded string limit and careful parsing.

Dump a measured interval in GDB with `dump binary memory decoded.bin START END`, replacing both addresses with mapped runtime bounds. Record the base address alongside the dump. Reimporting at address zero loses pointer relationships. Integrity checks can detect patches and software breakpoints; emulation or observing after the check may preserve more behavior than editing code.

## 10. Custom VMs and emulation

A VM is an interpreter plus a bytecode program. Recover its state before naming every opcode: program counter, registers or operand stack, memory, flags, and input/output operations. Find the dispatch loop, log one instruction's before/after state, and build a table of operand lengths and effects. Compare two runs differing in one input byte to locate the first dependent bytecode region.

**Windows WSL Python; complete tiny VM with no extra libraries:**

```python
# Opcodes: 1=load immediate, 2=XOR immediate, 3=add immediate, 4=emit, 255=halt.
program = bytes([1, 0x61, 2, 0x31, 3, 0, 4,
                 1, 0x3d, 2, 0x71, 3, 0, 4, 255])
pc, accumulator = 0, 0
output = bytearray()
steps = 0
while pc < len(program):
    steps += 1
    if steps > 100: raise RuntimeError('instruction budget exhausted')
    at = pc
    opcode = program[pc]
    pc += 1
    if opcode == 255:
        break
    if opcode in (1, 2, 3):
        if pc >= len(program): raise ValueError('truncated operand')
        operand = program[pc]
        pc += 1
        if opcode == 1: accumulator = operand
        elif opcode == 2: accumulator ^= operand
        else: accumulator = (accumulator + operand) & 255
    elif opcode == 4:
        output.append(accumulator)
    else:
        raise ValueError(f'unknown opcode {opcode} at {at}')
    print(f'pc={at:02x} op={opcode:02x} a={accumulator:02x}')
assert bytes(output) == b'PL'
print(output.decode())
```

The final output is `PL`. A real VM may use variable-length instructions, encoded opcodes, channels between threads, or self-modifying bytecode. Keep program memory writable in the model when STORE can alter instructions. For concurrent interpreters, record message ordering and blocking conditions; arbitrary round-robin scheduling is not automatically equivalent.

| Model | Choose it when | State you must supply |
| --- | --- | --- |
| Small Python interpreter | Only a handful of VM instructions matter | Exact opcode semantics and integer widths |
| radare2 ESIL, Kali | A supported short native routine can be isolated | Registers, stack, memory, stop condition; verify instruction coverage |
| Unicorn, conditional non-AI library | Raw foreign CPU code is the obstacle | Mapped pages, architecture/mode, registers, memory and syscall/MMIO stubs |
| Qiling, conditional non-AI library | OS calls and filesystem behavior matter | Compatible root filesystem and accurate API behavior |
| angr, Kali approved row 13 | Input constraints lead to a small set of branches | Input model, success/failure conditions, bounds and realistic environment |

Unicorn/Qiling are not individually listed as preinstalled. Their library status does not supply missing firmware, OS images, or separate emulators. `qemu-img` approval covers disk-image tooling; it does not establish approval or installation of every `qemu-system-*` or `qemu-user-*` executable.

For Unicorn, map page-aligned code and stack, use a finite instruction budget, and stop at the function's return boundary. An invalid fetch usually means a bad PC or return address; an invalid read/write often means missing data, incorrect ABI arguments, or wrong pointer width. Do not “fix” every fault by mapping zero pages: that can conceal an incorrect model.

Snapshotting registers alone does not reset memory. Restore dirty pages and peripheral state between candidates. ARM Thumb needs the correct execution mode; MIPS needs endianness and delay-slot semantics; mixed x86 modes require compatible register and memory transfer. CPU emulation does not implement operating-system syscalls. MMIO reads need meaningful device behavior, such as a changing ready bit, rather than arbitrary constants.

## 11. Symbolic execution as a bounded experiment

Use symbolic execution after you know the checker's input shape. Avoid launching unconstrained exploration over an entire GUI or runtime. A solver model reaching a success address is a candidate input; replay it through the original file before accepting it.

**Kali, approved angr environment, with its Python import confirmed:**

```bash
python3 -c 'import angr, claripy; print(angr.__version__)'
```

A failed import can mean angr lives in an isolated pipx environment. Use the interpreter provided with that environment rather than assuming system Python shares its packages. If it cannot be located, continue with the byte-transform solver above.

Save as `solve_checker.py`; this is specific to the complete `checker.c` example, including its four-byte input and messages.

```python
import angr
import claripy

project = angr.Project('./checker', auto_load_libs=False)
characters = [claripy.BVS(f'c{i}', 8) for i in range(4)]
content = claripy.Concat(*characters, claripy.BVV(b'\n'))
stream = angr.SimFileStream(name='stdin', content=content, has_end=True)
state = project.factory.full_init_state(args=['./checker'], stdin=stream)
for character in characters:
    state.solver.add(character >= 0x20, character <= 0x7e)
manager = project.factory.simulation_manager(state)
manager.explore(find=lambda s: b'correct\n' in s.posix.dumps(1),
                avoid=lambda s: b'wrong' in s.posix.dumps(1), n=1000)
if not manager.found:
    raise SystemExit('No solution within this exploration budget; inspect states')
answer = manager.found[0].solver.eval(claripy.Concat(*characters), cast_to=bytes)
print(answer.decode('ascii'))
```

Expected candidate: `PLAN`. `n=1000` bounds exploration rounds, not wall-clock runtime; interrupt a stalled run rather than letting it consume the session. If a target reads argv, models a file, or requires more input, change the model accordingly. Hooks must preserve the behavior relevant to the check; replacing a hash with a success constant makes a false solver. File and stream modeling are covered in the [angr filesystem documentation](https://api.angr.io/en/v9.2.112/advanced-topics/file_system.html).

## 12. Language and platform routes

| Target | Approved starting route | What to recover before solving |
| --- | --- | --- |
| Python `.pyc` | Kali pycdc/uncompyle6/unpyc3; WSL matching Python `dis` when available | Interpreter version, constants, nested code objects, opcode mapping |
| PyInstaller | Kali pyinstxtractor-ng | Embedded archive, Python version, actual application module |
| .NET | Windows native dnSpyEx | Entry method, resources, initializer, decryptor, comparison |
| APK/DEX | Kali jadx and Apktool | Java/Kotlin entry flow, resources, native methods, ABI-specific `.so` |
| Electron | Kali approved `asar` utility | `app.asar`, main/preload scripts, native addon boundary |
| Go | Kali GoReSym; radare2 or WSL Ghidra | Runtime versus user functions, string pointer/length pairs, goroutines |
| Rust | WSL Ghidra or Kali radare2 | Slice lengths, enum tags, panic paths, JSON field names |
| Swift/Kotlin/C++ | WSL Ghidra; Kali jadx for JVM bytecode | Witness tables, coroutine state, vtables/RTTI, destructors |
| WASM / exotic bytecode | Local bytes, strings, small interpreter | Linear memory, imports, instruction encoding, host interaction |
| Godot/Roblox/Unity | Inspect supplied assets and scripts first | Resource container, script format, engine/native boundary |
| Firmware / drivers | Kali radare2; WSL Ghidra, binwalk where appropriate | Architecture, load address, entry point, device interfaces |

These are investigation routes, not claims that every specialized decompiler is installed. Flutter/IL2CPP, HarmonyOS ABC, Pyarmor, macOS/iOS, SGX, and proprietary game formats may require tooling absent from the approved list. Preserve the structural reasoning; use approved static tools and challenge-provided resources, or defer that route.

**Kali APK, static extraction:**

```bash
jadx -d jadx-out challenge.apk
apktool d challenge.apk -o apk-out
rg -n 'native |loadLibrary|RegisterNatives|flag|secret|check' jadx-out apk-out
```

When Java calls `native check(...)`, locate the corresponding `lib/<abi>/*.so`. Dynamic registration maps method names and signatures to native function pointers. Android `.so` files may depend on bionic, JNI objects, initialization, and ARM instructions; loading one into desktop Linux with `ctypes.CDLL` is not a general substitute for an Android runtime. Certificates, assets, or logged values can be key material; reproduce exact hashing and byte encodings.

**Kali UPX, work on a copy:**

```bash
cp chall chall.work
upx -t chall.work
upx -d chall.work
rabin2 -I chall.work
```

Failure can mean unsupported UPX, a modified header, or no UPX at all. It is not a reason to patch magic bytes blindly. For a custom packer, identify the decoding loop and inspect memory after it runs.

## 13. Recognize the less common patterns

| Pattern in the source collection | Useful observation and next step |
| --- | --- |
| Multi-layer decryptor / RC4 gate plus VM | Solve and dump one layer at a time; feed the original verified output into the next layer |
| S-box/SPN constants / GF(2^8) elimination | Extract tables exactly; XOR is addition in the field, and multiplication needs the observed reduction polynomial |
| Sliding-window popcount | Adjacent count differences constrain the leaving/entering bits; enumerate only the initial window |
| Decision-tree validator | Convert accepted leaves into constraints rather than reversing every repeated branch |
| CVP/LLL integer validator | Preserve coefficient widths and bounds; a nearby lattice vector still needs original-checker validation |
| Prefix key-chain VM | Each recovered block initializes the next; rollback all state when a candidate fails |
| GBA meet-in-the-middle hash | Separate forward/backward states at a real invertible boundary and retain collision candidates |
| Sprague-Grundy game | Recover legal moves and terminal states, then compute mex values; the winning input is game logic |
| Kernel-module maze | Extract transitions from the module and solve the graph without loading an unknown driver |
| ROPfuscation / return-chain obfuscation | Treat stack words as the instruction stream and track gadget side effects |
| Image XOR / Newton convergence / PE bitmap | The program may generate an image rather than compare a string; recover dimensions, bit order, and palette |
| Quadtree image parser | Recurse using the encoded subdivision rule; validate consumed length and leaf coordinates |
| GLSL texture VM | Separate program memory from rendered output; handle STORE and scheduling effects explicitly |
| Font ligatures / LED Morse / GPIO LCD | Decode the output protocol: glyph substitutions, timing units, enable edges, command/data bits |
| BWT without a terminator | Recover rotations and use the checker's external ordering constraints to select the valid one |
| CRT plus matrix lookup | Solve modular constraints first, then reproduce lookup/index conventions |
| Brainfuck / FRACTRAN / Make VM / OPAL / Glulx | Identify state transitions and input-dependent comparisons before adopting a full language runtime |
| Unusual ROM / custom opcode / KVM HLT chaining | Inspect the emulator or handler implementing the instruction, not only a generic ISA manual |
| Cortex peripheral AES / MIPS coprocessor crypto | Memory-mapped registers or coprocessor calls may perform the cryptography outside ordinary ALU code |
| Bootloader / real-mode x86 / ARM in pixels | Recover load base, segment/mode, and byte packing before disassembly |
| Backdoored library / binary diff | Compare equivalent builds, strings and changed functions; startup and exported wrappers deserve attention |
| Date-derived key / instruction counter | Preserve the exact clock or counter state used by the transform |
| Destructor-hidden or MFC event validation | Trace object teardown or event dispatch as part of the main control flow |
| EBCDIC SAVF / DOS stub / embedded ZIP | Identify the actual nested representation and decode it locally |

AI/ML inversion examples in the source are not competition workflows here: the event's AI/ML restriction takes priority. Likewise, historical C2 enumeration and cloud-function examples do not authorize contacting unrelated services. Study their local control/data-flow lesson only.

## 14. A useful stopping point and a reproducible handoff

Keep the original hash, exact tool/environment, relevant function addresses, transformation pseudocode, extracted constants, solver script, and original-program validation result. Describe unresolved assumptions explicitly. If a patch only displays “correct,” say so; it is not a recovered flag unless the task explicitly asks for a patch.

| Failure | First correction |
| --- | --- |
| “Exec format error” | Match architecture/format; continue static analysis instead of installing an emulator |
| Existing ELF reports “No such file” | Inspect its requested interpreter/loader and supplied runtime |
| Breakpoint never hits | Verify image base, process/thread, optimization, inline comparison, and delayed library load |
| Solver returns printable nonsense | Recheck direction, endian order, widths, and whether the expected table was a decoy |
| Emulator hangs | Find the polling condition, missing interrupt, wrong branch semantics, or incorrect stop address |
| A dump will not decompile | Record its runtime base and segment permissions; raw data has no loader metadata |
| Decompiler disagrees with a run | Inspect the exact instructions, mutated code, ABI and hidden handlers |

Source map: `ctf-reverse/SKILL.md`, `tools.md`, `radare2-r2pipe.md`, `tools-dynamic.md`, `tools-emulation.md`, `tools-advanced.md`, `tools-advanced-2.md`, `mba-simplification.md`, `anti-analysis.md`, `anti-analysis-ctf.md`, `patterns.md`, `patterns-runtime.md`, `patterns-ctf.md`, `patterns-ctf-2.md`, `patterns-ctf-3.md`, `languages.md`, `languages-platforms.md`, `languages-compiled.md`, `platforms.md`, `platforms-hardware.md`, `unicorn-emulation.md`, and `field-notes.md`. Paths after the first share the `ctf-reverse/` prefix. The source `ctf-reverse/tools-mcp.md` is retained as provenance only; its agent integration and unapproved-tool setup are excluded from the human workflow.

</details>
