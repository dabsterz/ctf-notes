# Pwn practice atlas

Use supplied local practice artifacts; [event rules](../COMPETITION.md). Historical claims need verification against your binary/runtime. All 43 case explanations remain in Full reference. [Offset workflow](08-binary-exploitation.md#quick-measure-the-crashing-input).

## Quick: inventory one exercise

**Kali · Bash**

```bash
read -r -p 'Local exercise binary path: ' FILE
file "$FILE"
rabin2 -I "$FILE"
rabin2 -i "$FILE"
rabin2 -R "$FILE"
```

**Look for:** architecture, imports, relocation targets and supplied runtime files.
**If not:** recover the matching artifact first; old addresses are not measurements.

## Quick: inspect a control or index primitive

**Kali · Bash**, then **radare2** ([commands](https://book.rada.re/refcard/intro.html)).

| Cases | First checkpoint |
| --- | --- |
| start, calc, silver_bullet, dubblesort | Read size, index/length change, sorting |
| 3x17, starbound, babystack | Reentry, dispatch index, stale input |
| unexploitable, de_aslr, printable | Missing output and usable existing pointers |

```bash
read -r -p 'Local exercise binary path: ' FILE
r2 "$FILE"
```

```text
aaa
ii
afl
pdf @ main
```

**Look for:** one controlled value reaching one later consumer.
**If not:** select a discovered function with `pdf @` plus its exact name; inspect the parser before a long chain.

## Quick: check constrained code and descriptors

**Kali · Bash**

| Cases | First checkpoint |
| --- | --- |
| orw, kidding | Permitted syscalls and open descriptors |
| death_note, alive_note, mno2 | Validator, byte limits and fragment boundaries |

```bash
read -r -p 'Local executable path (include ./ or use absolute): ' FILE
strace -f -o descriptors.log -e trace=close,read,write,openat,prctl,seccomp "$FILE"
```

**Windows WSL · raw x86 shellcode inspection**

```bash
read -r -p 'Raw payload file: ' FILE
xxd "$FILE"
objdump -D -b binary -m i386 -M intel "$FILE"
```

**Look for:** valid instruction boundaries and live descriptors; use `-m i386:x86-64` only for 64-bit code.
**If not:** reproduce the exact validator. Printable bytes alone do not satisfy `mno2`'s grammar.

## Quick: prove an object outlives its storage

**Windows WSL · compatible Linux x86-64 ELF; Bash**, then **GDB**.

| Cases | First checkpoint |
| --- | --- |
| hacknote, secret_garden, tcache_tear, heap_paradise | Stale pointer and actual reuse |
| secret_of_my_heart, bookwriter, spirited_away | Changed size/terminator boundary |
| applestore, re_alloc, re_alloc_revenge, break_out | Owner survives free or return |
| caov, ghost_party, food_store, babyallocator | Destruction, initialization or segment metadata |

```bash
read -r -p 'Local ELF path: ' FILE
gdb -nx -q "$FILE" -ex 'break free' -ex run
```

```text
bt
info registers rdi
x/4gx $rdi
```

**Look for:** the freed address still reachable through an application object; RDI applies to x86-64.
**If not:** trace allocation and slot clearing; `re_alloc`'s historical description is contradictory.

## Quick: inspect FILE and library state

**Kali · static Bash inspection**

| Cases | First checkpoint |
| --- | --- |
| seethefile, wannaheap | Next FILE consumer and two size variables |
| criticalheap, criticalheap_pp | Format sink or resolved-path write length |
| bounty_program_a, bounty_program_b | Retained strtok pointer and delimiter write |

```bash
read -r -p 'Local exercise binary path: ' FILE
rabin2 -i "$FILE" > imports.txt
rg 'fclose|fread|fwrite|printf|realpath|strtok|localtime' imports.txt
```

**Look for:** the exact state consumed by the next call.
**If not:** inspect static functions; old FILE layouts require their matching libc.

## Quick: test parser state before exploitation

**Windows WSL · Bash; inspect a supplied ELF.**

| Cases | First checkpoint |
| --- | --- |
| hitcon_ftp, seccomptools | Type/length validation or evaluator disagreement |
| stupid_boss, digimon, omegago | Field layout, tokenization or history growth |

```bash
read -r -p 'Local ELF path: ' FILE
objdump -d -M intel "$FILE" > exercise.asm
strings -a -t x "$FILE" > exercise.strings
```

**Look for:** the first mismatched width, type, bound or state transition.
**If not:** record one valid input and change one field; several catalog summaries disagree with detailed cases.

## Quick: inspect a historical shell artifact

**Windows WSL · static only; bash and bash_revenge cases.**

```bash
read -r -p 'Supplied historical shell binary path: ' FILE
objdump -f "$FILE"
strings -a "$FILE" > shell-strings.txt
```

**Look for:** exact build, builtin and allocator assumptions in the supplied lab.
**If not:** stop at static analysis; the workstation shell is not that practice image.

## Quick: save a reproducible checkpoint

**Windows WSL · Bash/Python**

```bash
read -r -p 'Artifact to fingerprint: ' FILE
python3 - "$FILE" <<'PY'
import hashlib, sys
from pathlib import Path
p = Path(sys.argv[1])
print(p.name, hashlib.sha256(p.read_bytes()).hexdigest())
PY
```

**Look for:** saved input, binary/libc hashes, first primitive, observed trigger and one failed assumption.
**If not:** repeat from a fresh local process before retaining an exploit claim.
