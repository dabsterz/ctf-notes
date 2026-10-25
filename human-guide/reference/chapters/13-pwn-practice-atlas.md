# Pwn practice atlas: 43 cases, each with a specific lesson

**Quick route:** [Short commands](../QUICKSTART.md#crash-offset) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#binary-exploitation). Use this chapter for deeper explanations.

Use this atlas after the binary-exploitation chapter. It preserves the individual exercises from `ctf-pwn/pwnable-tw/` without presenting historical offsets as universal exploits. The cases are preparation material, not an instruction to connect to public practice servers during the competition. Use locally supplied practice artifacts or an explicitly assigned challenge service.

The case descriptions below come from the repository's individual writeups. Their original binaries, exact runtimes, and exploit success claims were not reproduced for this handbook. Several directory-index summaries disagree with their detailed writeups; the disputed claims are identified below. Treat the individual mechanisms as hypotheses to verify against your copy of the binary.

## How to work through a case

For every case, record the binary and libc hashes, architecture, input protocol, protections, and the exact state transition that creates the primitive. Stop after each checkpoint. A working local leak is more useful than an unexplained full exploit copied from an old environment.

**Kali, approved tools, with the exercise binary named `chall`:**

```bash
file chall
checksec --file=chall
rabin2 -I chall
rabin2 -i chall
r2 chall
```

In radare2, use `aaa`, `afl`, `pdf @ main`, and `axt @ IMPORT`, replacing `IMPORT` with the exact flag shown by `ii`. Follow the vulnerable caller, identify the input operation and the state it changes, then inspect the next consumer of that state. The GDB commands in the pwn chapter are the **Windows WSL** debugging route; Kali debugging requires the supplied GDB environment to work. **Windows native** x64dbg is for Windows PE targets, not these Linux ELF cases.

For stdlib packing use Windows WSL Python, or Kali Python after checking its availability. Pwntools is not individually listed as preinstalled. PDF p.5 permits non-AI libraries in either environment; permission does not establish availability or satisfy native-tool dependencies. Keep original template scripts as study references; the pwn chapter describes their defects and standard-library alternatives.

## First control-flow and parsing exercises

### 1. `start`: obtain the stack address before using it

**Prerequisites:** i386 syscall conventions, little-endian packing, executable-stack behavior, two-stage input framing.

The detailed writeup describes a 60-byte read into a 20-byte message region, followed by a return. An existing write sequence can disclose the stack value before another input stage. Identify the read count and the exact saved return slot in the disassembly; then reuse the output path and parse its raw bytes before considering a stack target.

**Checkpoint:** the recovered pointer falls inside the current stack mapping and the next read lands where you predict. A successful first write does not mean the second payload has enough space. Source: `ctf-pwn/pwnable-tw/start.md`.

### 2. `orw`: the permitted end goal is smaller than a shell

**Prerequisites:** i386 Linux syscalls, shellcode placement, seccomp policy interpretation.

Input is executed in a writable/executable region, but a syscall filter limits what it can do. Decode the actual policy and implement the permitted file-read sequence: open the exact challenge path, preserve the returned descriptor, read into a valid buffer, and write the returned count. The historical alternative involving a missing architecture check requires a very specific kernel and filter; do not confuse x32 ABI calls with a 32-to-64-bit mode switch.

**Checkpoint:** every syscall and argument is permitted, and errors are distinguished from successful reads. Source: `ctf-pwn/pwnable-tw/orw.md`.

### 3. `calc`: an arithmetic parser can become a stack-index primitive

**Prerequisites:** expression parsing, stack layout, signed arithmetic, ROP in a static i386 binary.

The source describes a mismatch between pushing an operand and evaluating an operator when a token converts to zero. That mismatch changes the operand-pool index. Trace a minimal expression in the debugger and record the pool counter before and after each operation; derive which expression reads or adjusts one chosen stack word before assembling a longer chain.

**Checkpoint:** one selected word changes by the predicted delta while surrounding state remains usable. Preserve any canary and account for arithmetic width. Source: `ctf-pwn/pwnable-tw/calc.md`.

### 4. `silver_bullet`: the terminator changes the next operation's length

**Prerequisites:** struct layout, `strncat` semantics, staged ret2libc on i386.

When the description reaches its nominal capacity, the appended NUL reaches the adjacent power field. The next append trusts that altered field and can write farther. Measure the field boundary and demonstrate the reset with a complete-length input before using the enlarged append to reach saved control data.

**Checkpoint:** the first operation changes length state, and the second demonstrably uses that new state. Leak and reentry stages must each preserve the game's expected flow. Source: `ctf-pwn/pwnable-tw/silver_bullet.md`.

### 5. `dubblesort`: the program rearranges the payload

**Prerequisites:** i386 stack layout, unterminated-string disclosures, failed numeric conversions, sorting constraints.

An unterminated name can disclose neighboring stack data; an excessive element count reaches past the number array. A failed `scanf` conversion may leave an existing canary word unchanged, but the subsequent sort still permutes the entire array. Reconstruct the actual comparison type and positions before choosing numeric values.

**Checkpoint:** model the sorted array locally and confirm the canary and final control words end up at the intended slots. A “skip input” trick is insufficient if sorting later moves the preserved word. Source: `ctf-pwn/pwnable-tw/dubblesort.md`.

### 6. `3x17`: a small write becomes a staged sequence

**Prerequisites:** ELF destructors, static x86-64 layout, `leave; ret` stack pivots.

The source describes a fixed-size arbitrary write and writable destructor-related state. Reentering the input routine through the finalization path can provide repeated writes, after which a prepared fake frame pivots to a chain. Confirm the actual finalizer order and guard counter: “infinite writes” in the source is shorthand and may be bounded by program state.

**Checkpoint:** two consecutive writes succeed through the planned reentry, and the fake frame has both a replacement BP word and a return word. Source: `ctf-pwn/pwnable-tw/3x17.md`.

### 7. `starbound`: a menu choice becomes an indirect call

**Prerequisites:** indexed addressing, function-pointer dispatch, stack pivots and disclosure calls.

The main menu uses the parsed choice as an unchecked index into a function table. A negative index can reach the player-name buffer. Derive `(controlled_buffer - table_base) / pointer_size` from the actual image rather than copying the historical index, and confirm the resulting indirect call target.

**Checkpoint:** the dispatcher reads the intended pointer from your name data. Then prove the chosen gadget's stack and register effects before using it for a leak or pivot. Source: `ctf-pwn/pwnable-tw/starbound.md`.

### 8. `babystack`: an authentication oracle and stale stack bytes compose

**Prerequisites:** prefix comparisons, NUL termination, repeated stateful requests, stack-copy behavior.

The comparison length comes from the supplied string, so empty input or a correct prefix can change authentication behavior. A later copy uses a stack buffer previously filled by another operation; bytes outside the shorter read can survive and extend a `strcpy`. Separate oracle recovery from the overflow and preserve the original password/check value where the exit path validates it.

**Checkpoint:** a known correct and known wrong prefix produce distinct results under the same process state. Then demonstrate the stale tail used by the copy. Source: `ctf-pwn/pwnable-tw/babystack.md`.

## Constrained code and missing-output exercises

### 9. `death_note`: a negative index reaches a relocation slot

**Prerequisites:** i386 GOT layout, signed bounds checks, printable shellcode encoding.

The note index is checked only against an upper bound. Derive which negative slot reaches a writable function pointer and inspect whether the allocated note memory is executable at runtime. The input filter constrains bytes, so ordinary machine code must be encoded or constructed in stages.

**Checkpoint:** the target slot changes to the allocated buffer and the next call actually dereferences it. Check every input byte against the filter before attempting execution. Source: `ctf-pwn/pwnable-tw/death_note.md`.

### 10. `alive_note`: tiny fragments need a reliable bridge

**Prerequisites:** the negative-index primitive, alphanumeric encoding, heap placement, short jumps.

This variant combines a small per-note limit with a restricted character set. The source chains tiny code fragments across allocations, but allocator padding and terminators are part of the instruction stream. First draw fragment addresses, usable bytes, and gaps; then derive each jump and verify the initial register state used by the decoder.

**Checkpoint:** a local disassembly follows the intended fragment sequence without executing chunk headers or NUL terminators. Source: `ctf-pwn/pwnable-tw/alive_note.md`.

### 11. `mno2`: bytes must satisfy two grammars

**Prerequisites:** x86 instruction encoding, alphanumeric self-modification, parser tokenization.

The executed input must also parse as a chemical formula. A sequence that is valid x86 and alphanumeric can still fail the element-symbol grammar. Reproduce the validator and test each encoded fragment through both the parser and disassembler; preserve the known entry registers that make arithmetic/XOR construction possible.

**Checkpoint:** the full first stage passes the original validator and reconstructs the intended unrestricted bytes in writable memory. Element-looking bytes are not harmless padding if they change a needed register. Source: `ctf-pwn/pwnable-tw/mno2.md`.

### 12. `kidding`: account for descriptors closed before control transfer

**Prerequisites:** static i386 ROP, descriptor lifetime, tight payload budgets.

The binary reads once, then closes standard input/output/error before returning. The obvious second read or stdout write is therefore unavailable. Trace the descriptor closures and count the first payload's usable bytes; any restored communication must stay within an explicitly authorized local practice topology.

**Checkpoint:** the complete first-stage path works with descriptors 0, 1 and 2 already closed. The historical helper/flag path is specific to that challenge image. No public callback endpoint or listener is provided by this handbook. Source: `ctf-pwn/pwnable-tw/kidding.md`.

### 13. `unexploitable`: manufacture a missing primitive from existing code

**Prerequisites:** x86-64 ROP, ret2csu, partial pointer writes, syscall return values.

The overflow is simple, but the binary lacks an ordinary output routine and convenient syscall gadget. The detailed source describes a writable relocation at a page boundary and a low-byte redirection into a nearby syscall instruction in the matching libc. Verify actual runtime page permissions rather than assuming the RELRO summary identifies every boundary correctly.

**Checkpoint:** the redirected call reaches the intended instruction and its registers have the expected values. A read returning 15 is usable for SROP only if the trigger and frame are also correct. Source: `ctf-pwn/pwnable-tw/unexploitable.md`.

### 14. `de_aslr`: use a pointer already present without printing it

**Prerequisites:** constrained x86-64 ROP, stack pivots, arithmetic gadgets, dynamic linker internals.

The detailed writeup describes an unbounded `gets`, no normal output function, and Full RELRO. Study how a known libc pointer can be loaded or transformed through existing register/memory operations without first leaking it. The directory index's generic writable-GOT/dynamic-resolver story is not sufficient evidence for this target.

**Checkpoint:** track one existing pointer through every gadget and prove the resulting indirect target. Test newline restrictions and carry/overflow side effects. Source: `ctf-pwn/pwnable-tw/de_aslr.md`.

### 15. `printable`: a format string can still act when output is closed

**Prerequisites:** `%n` count writes, stdio buffering, finalization, partial overwrite probabilities.

The format sink executes after stdout is closed, and the program then calls `exit`. A useful path must create repetition or redirect a usable output stream before ordinary leaks become available. Measure how much formatting occurs before a failed flush aborts the operation; do not assume arbitrary large counts are possible.

**Checkpoint:** distinguish a successful loop, a restored output channel, and final control flow as three separate milestones. Historical argument positions and retry probabilities depend on the original runtime. Source: `ctf-pwn/pwnable-tw/printable.md`.

## Heap ownership and allocator exercises

### 16. `hacknote`: metadata can be reclaimed as content

**Prerequisites:** UAF, allocation size classes, i386 function pointers.

Deleting a note frees its metadata and content but leaves the table pointer. A later allocation can occupy that metadata region and replace the print callback/data interpretation. Track the metadata allocation separately from its content allocation; otherwise a superficially similar size may reclaim the wrong object.

**Checkpoint:** a new buffer overlaps the stale note object, and the print action reads the expected callback and argument. Start with a controlled disclosure before a final call. Source: `ctf-pwn/pwnable-tw/hacknote.md`.

### 17. `secret_garden`: free state and table membership disagree

**Prerequisites:** glibc fastbins/unsorted bins, stale references, partial writes.

Removing a flower releases its name but leaves enough object state to revisit the allocation. The source combines disclosure of freed metadata with repeated frees/reallocation. Distinguish a slot's active flag from whether its pointer has been cleared; cleanup operations can change the heap history.

**Checkpoint:** after removal, identify exactly which later action still accesses the freed name and what bytes an allocation preserves. Source: `ctf-pwn/pwnable-tw/secret_garden.md`.

### 18. `secret_of_my_heart`: one NUL changes consolidation

**Prerequisites:** off-by-one terminators, chunk headers, backward consolidation, heap disclosures.

A full content read is followed by a terminator one byte beyond the requested buffer. A separate unterminated name can expose the adjacent pointer. Recover the heap layout, then verify which size flag the zero byte changes and which neighboring fields must remain consistent for the allocator.

**Checkpoint:** freeing the affected neighbor produces the intended overlap without an integrity abort. A time-derived metadata address or hidden menu route is an alternative to investigate, not a required assumption. Source: `ctf-pwn/pwnable-tw/secret_of_my_heart.md`.

### 19. `tcache_tear`: repeated free plus a fixed scratch region

**Prerequisites:** the supplied early-tcache libc, free-list state, fake-chunk prerequisites, unsorted disclosures.

The detailed source's reliable core is a global pointer left live after free, plus a known BSS region useful for shaping metadata. Prove the actual tcache behavior of the supplied build and the allocation sequence leading to the target region. Do not transplant this chain to modern safe-linking allocators.

**Checkpoint:** repeated allocation returns the intended overlap, and a forged larger chunk satisfies the target allocator's checks. The source's additional claim that a small `malloc(size)` plus `read(..., size)` is itself an overflow is not established by that code and is not used here. Source: `ctf-pwn/pwnable-tw/tcache_tear.md`.

### 20. `heap_paradise`: build a leak before relying on absolute addresses

**Prerequisites:** fastbin duplication, unsorted-bin residue, partial stdout corruption.

The menu has allocation/free operations and stale pointers but no convenient normal disclosure. The source uses allocator metadata and a partial overwrite to reach a stdout-related disclosure. Draw the relative chunk layout before making an absolute-address hypothesis.

**Checkpoint:** a recognizable libc pointer is emitted and confirmed against the supplied library. Record the unknown low bits and measured retry rate instead of calling the initial partial overwrite deterministic. Source: `ctf-pwn/pwnable-tw/heap_paradise.md`.

### 21. `bookwriter`: no delete operation does not mean no freed chunk

**Prerequisites:** unterminated strings, top-chunk behavior, historical House of Orange/FILE exploitation.

The editor updates capacity from `strlen`, which can exceed the original allocation when no NUL is present. The source combines this with top-chunk manipulation to enter allocator paths that free old top memory without a menu delete. Also inspect the off-by-one page slot and author-string disclosure.

**Checkpoint:** the edited length really increases, the next write reaches the intended metadata, and the old top follows the predicted allocator path. The final FILE technique requires the old challenge libc. Source: `ctf-pwn/pwnable-tw/bookwriter.md`.

### 22. `applestore`: a list keeps a pointer to an expired stack object

**Prerequisites:** stack lifetimes, linked-list layout, constrained reciprocal writes.

A specific cart total creates a promotional node as a local variable and links it into a longer-lived list. After checkout returns, later input can overlap its fields. Solve the cart-total arithmetic from the supplied prices, then show the same stack bytes being reused as the node's name/link fields.

**Checkpoint:** listing the cart dereferences your chosen name pointer. Before using unlink, calculate both writes and ensure the secondary write does not crash or destroy a needed field. Source: `ctf-pwn/pwnable-tw/applestore.md`.

### 23. `spirited_away`: decimal formatting changes a length field at a threshold

**Prerequisites:** precise stack layout, decimal string lengths, fake-chunk allocation.

The feedback counter is formatted into a buffer near a length field. As the digit count grows, the formatted suffix corrupts that field and enables a larger later read. An unterminated reason supplies useful disclosures; the historical chain then places a fake chunk on the stack.

**Checkpoint:** observe the exact counter threshold and changed length byte. Verify the fake chunk and next allocation before targeting a saved return slot. Source: `ctf-pwn/pwnable-tw/spirited_away.md`.

### 24. `re_alloc`: audit the zero-size return path carefully

**Prerequisites:** glibc `realloc` semantics, two-slot ownership, tcache poisoning, GOT redirection.

The intended lesson is a stale-pointer/lifetime error around zero-size reallocation and a later conversion-function redirection. However, this source contradicts itself: its overview says the old pointer remains, while one subsection says the NULL return is stored. Ordinary `realloc(NULL, n)` followed by a write is not by itself a UAF.

**Checkpoint:** establish from the binary whether the zero-size path leaves a dangling pointer, duplicate alias, or another invalid lifetime. Only then consider the proposed tcache/GOT/format-string chain. Source: `ctf-pwn/pwnable-tw/re_alloc.md`.

### 25. `re_alloc_revenge`: an error branch preserves an invalid owner

**Prerequisites:** realloc failure/zero-size behavior, two-slot heap choreography, disclosure alternatives.

The detailed source describes `realloc(ptr, 0)` freeing storage and returning NULL, followed by an error path that does not clear the stored pointer. Model both slots after every operation and inspect how allocator duplicate-free checks are handled in the exact provided runtime.

**Checkpoint:** show an actual subsequent access through the dangling slot and prove a controlled overlap. The harder version's protection changes require a new target choice; do not carry over writable-GOT assumptions. Source: `ctf-pwn/pwnable-tw/re_alloc_revenge.md`.

### 26. `caov`: C++ temporaries and stale stack fields both affect ownership

**Prerequisites:** copy assignment, destructors, stack-frame reuse, arbitrary-free consequences.

Returning a data object by value can create a temporary whose destructor releases shared storage. A separate routine leaves stack bytes where a later object expects its pointer field, allowing destruction to act on stale data. Draw the copy/destruction sequence rather than treating every menu operation as one allocation.

**Checkpoint:** identify which destructor frees which address, and whether the same pointer still has a live owner. Source: `ctf-pwn/pwnable-tw/caov.md`.

### 27. `ghost_party`: shallow copies violate unique ownership

**Prerequisites:** C++ copy constructors, raw owning pointers, virtual dispatch.

The Vampire class's default copy preserves a pointer that its destructor frees, while another object's temporary string can leave a dangling `c_str` pointer. Compare the vulnerable classes with those that implement correct copying; that contrast helps identify the actual lifetime error.

**Checkpoint:** after the source object or temporary is destroyed, demonstrate the remaining reference and the allocation that reuses its storage. Source: `ctf-pwn/pwnable-tw/ghost_party.md`.

### 28. `break_out`: a freed note remains reachable through a linked object

**Prerequisites:** UAF, overlapping objects, linked-list traversal, read/write through pointer fields.

Punishment frees a prisoner's note without clearing its pointer and size. Reallocation can turn that stale access into an overlapping object; modifying a next pointer can make listing traverse a forged prisoner. Preserve enough list structure to keep the menu usable during each stage.

**Checkpoint:** a list operation reads a controlled note pointer and an edit writes the predicted region. Validate both before selecting a libc-specific endpoint. Source: `ctf-pwn/pwnable-tw/break_out.md`.

### 29. `food_store`: an uninitialized link inherits old allocation contents

**Prerequisites:** heap reuse, uninitialized fields, linked structures, old-libc FILE constraints.

The individual writeup identifies a recipe `next` pointer never initialized after allocation. A reclaimed chunk can therefore supply a controlled or allocator-derived link. This is more specific than the directory index's generic heap-overflow summary and should guide the first experiment.

**Checkpoint:** record the chunk's previous contents, allocate the recipe, and show which bytes become its next pointer without being written. Follow the resulting list before considering advanced FILE or allocator chains. Source: `ctf-pwn/pwnable-tw/food_store.md`.

### 30. `babyallocator`: stack-segment metadata is an allocation target

**Prerequisites:** GCC split stacks, `alloca`, recursive frames, libc stack usage.

The source describes split-stack segment metadata being corrupted by a non-split-stack libc call at a carefully chosen depth and allocation size. This is not an ordinary one-buffer overflow: the runtime's segment header and dynamic allocation list must be reconstructed.

**Checkpoint:** identify the segment boundary and the exact libc write that reaches a metadata field, then prove the resulting returned allocation or frame overlap. Depth/size constants depend on the complete runtime. Source: `ctf-pwn/pwnable-tw/babyallocator.md`.

## FILE, stateful library and complex application exercises

### 31. `seethefile`: a pointer overflow reaches `fclose`

**Prerequisites:** BSS layout, file disclosures, glibc 2.23 FILE structures.

An unbounded exit-name input reaches the neighboring `FILE *`, and the program subsequently closes it. The file-viewing feature can disclose memory mappings in the original lab. Separate that address disclosure from the fake-object construction; identify every field consumed before virtual dispatch.

**Checkpoint:** the overwritten pointer reaches your object at `fclose`, with valid supporting state. The old fake-vtable route is not applicable unchanged to modern glibc. Source: `ctf-pwn/pwnable-tw/seethefile.md`.

### 32. `wannaheap`: validation updates one size but not another

**Prerequisites:** mmap-relative layouts, single-byte writes, stdin FILE behavior, treap-dependent residue.

The first requested size is remembered even after a replacement size is validated and used for allocation. The terminator is then written using the original value. The source turns this into a null-byte change to stdin buffering, while a separate uninitialized string can disclose a libc pointer.

**Checkpoint:** trace both size variables and observe the terminator address. Verify any mmap-to-libc distance for the supplied runtime and distinguish a probabilistic tree-layout leak from a guaranteed one. Source: `ctf-pwn/pwnable-tw/wannaheap.md`.

### 33. `criticalheap`: data types and library side effects matter

**Prerequisites:** format-string reads, stale slot state, environment variables, libc allocation behavior.

The detailed source describes several independent observations: a user-controlled format sink, unterminated output, reused slot contents, timezone file loading through `localtime`, and a `realpath` output buffer issue. Treat them as alternative routes with separate prerequisites rather than assuming one combined exploit.

**Checkpoint:** distinguish the challenge's stated objective from any decoy file, and identify which local operation yields the required information or write. File paths and helper behavior are specific to the original image. Source: `ctf-pwn/pwnable-tw/criticalheap.md`.

### 34. `criticalheap_pp`: the expanded path exceeds the input allocation

**Prerequisites:** `realpath` output semantics, heap grooming, environment-triggered allocations.

The detailed route uses the same small buffer for a relative input path and its longer resolved output, reaching adjacent allocation metadata. Environment and timezone operations provide additional allocation/free behavior. The directory index's broad C++ type-confusion explanation is not a substitute for measuring this path.

**Checkpoint:** demonstrate the exact resolved path length and write boundary, then record the neighboring chunk affected. Verify the real challenge objective independently of any decoy. Source: `ctf-pwn/pwnable-tw/criticalheap_pp.md`.

### 35. `bounty_program_a`: a NULL argument has stateful library meaning

**Prerequisites:** `strtok` continuation state, allocation failure, object pointer overwrites, digest oracles.

Failed allocation returns NULL, but passing NULL to `strtok` continues a previous tokenization rather than starting an empty one. The detailed source also describes a password overflow into a contact pointer and a contact-hash oracle. Prove each capability independently; a digest reveals a byte only when the remaining hashed bytes and candidate space are controlled.

**Checkpoint:** inspect the tokenizer's retained pointer and show the next read or delimiter NUL-write reaches the intended stale buffer. Source: `ctf-pwn/pwnable-tw/bounty_program_a.md`.

### 36. `bounty_program_b`: a delimiter write can alter a pointer

**Prerequisites:** the alpha variant's tokenizer state, heap overlap, protection-aware object reuse.

The hardened variant retains stateful tokenization on freed data. Because `strtok` replaces a matching delimiter with NUL, it can modify a byte inside a pointer if that byte equals the delimiter. Recover a real pointer containing that byte and calculate the resulting address before using the overlap.

**Checkpoint:** the intended pointer byte changes while the surrounding object survives its consistency checks. Keep alpha and beta runtime/protection assumptions separate. Source: `ctf-pwn/pwnable-tw/bounty_program_b.md`.

### 37. `hitcon_ftp`: protocol state supplies both a leak and a copy size

**Prerequisites:** MessagePack parsing, multi-packet protocol state, stack canaries, seccomp-aware ROP.

The detailed writeup identifies an option-type check performed only for one array length, enabling type confusion with a longer array. It separately describes a large negotiated block length used for formatting into a fixed **stack** buffer. The index's generic heap-corruption wording loses this distinction.

**Checkpoint:** decode a minimal valid request first, then show the unchecked object interpretation and the measured stack-write length independently. Preserve the canary and use the actual permitted output descriptor for a later ORW chain. Source: `ctf-pwn/pwnable-tw/hitcon_ftp.md`.

### 38. `seccomptools`: emulator/kernel disagreement is the first bug

**Prerequisites:** classic BPF, `seccomp_data`, return actions, FILE dispatch.

The detailed source says the user-space emulator fails to implement a length-load instruction that the kernel evaluates differently. A filter accepted under one model can therefore produce a different syscall result in the other. The proposed chain then exploits a synthetic zero return and a stream-pointer overwrite; it is not simply a generic heap-hook attack as the index suggests.

**Checkpoint:** compare both evaluators on the exact small filter before constructing a larger chain. Distinguish `ERRNO(0)` suppressing a syscall from a real successful file open. Source: `ctf-pwn/pwnable-tw/seccomptools.md`.

### 39. `stupid_boss`: compatible names do not imply compatible layouts

**Prerequisites:** C++ class layouts, type confusion, floating-point bit encoding, failed numeric conversions.

The detailed source describes compatibility checks that allow one language object's setter to operate on another layout. A double-valued setter can overwrite a pointer field, while another setter later dereferences it for reading or writing. The directory index's employee-UAF story is inconsistent with these details and is not used as the primary explanation.

**Checkpoint:** compare the two concrete field layouts and show exactly which eight bytes the setter changes. A failed `scanf` conversion may expose stale stack data, but confirm the leaked value's origin before using it. Source: `ctf-pwn/pwnable-tw/stupid_boss.md`.

### 40. `digimon`: start with parser state, not an assumed race

**Prerequisites:** unterminated input, `strtok` mutation, stack indices, asynchronous program state.

The individual writeup prioritizes a full command buffer lacking a NUL terminator, allowing tokenization to reach an adjacent partner index. It also identifies failed numeric conversions as a disclosure path and marks several apparent races/overflows as non-exploitable. The index's generic race-UAF description is therefore insufficient.

**Checkpoint:** use a full-length command to observe the exact index mutation and the subsequent task lookup. Preserve negative findings; do not spend time racing a path the detailed analysis says lacks the needed primitive. Source: `ctf-pwn/pwnable-tw/digimon.md`.

### 41. `omegago`: gameplay controls memory representation

**Prerequisites:** game-state transitions, history bounds, packed two-bit cells, fake-object construction.

The detailed route overfills a board-history array through repeated legal capture cycles, reaching adjacent state. A regret operation then dereferences altered history pointers. Controlled board bits can encode metadata, but each desired bit pattern must also be reachable through the game's rules.

**Checkpoint:** reproduce a short cycle and count history growth, then verify the first out-of-bounds history slot. This differs from the directory index's simpler coordinate-to-GOT narrative. Source: `ctf-pwn/pwnable-tw/omegago.md`.

## Restricted-shell and historical runtime exercises

### 42. `bash`: distinguish policy gaps from memory corruption

**Prerequisites:** executable permissions, dynamic loader behavior, shell builtins, exact lab confinement.

One historical route relies on the sandbox removing execute permissions from programs while leaving a readable program usable through an executable loader. Another investigates an old `popd` memory-corruption bug. These are different mechanisms; enumerate only the capabilities of the supplied challenge image before selecting one.

**Checkpoint:** establish which permission or builtin behavior is actually available in the local lab. The original loopback flag service is internal to that image; do not treat loopback services on a competition workstation as challenge targets. Source: `ctf-pwn/pwnable-tw/bash.md`.

### 43. `bash_revenge`: a shell variable can become the reclaimed object

**Prerequisites:** the exact old Bash build, out-of-bounds free, Bash's allocator, `SHELL_VAR` layout.

The detailed writeup turns a malformed `popd` index into a free operation and reclaims the region through shell-variable activity. A variable's value pointer can disclose data, and its dynamic callback is a distinct later control target. Model Bash's allocator and variable lifetime rather than applying glibc chunk offsets blindly.

**Checkpoint:** show which address is freed, what allocation reuses it, and when variable expansion dereferences the changed field. All helper/service access stays inside the explicitly supplied practice environment. Source: `ctf-pwn/pwnable-tw/bash_revenge.md`.

## What to retain after finishing a case

Write five short items: the initial bug, the first reliable primitive, the missing information it supplies, the final trigger, and the assumptions specific to this artifact. Include a failing attempt that taught you something about layout or protocol. This produces a reusable solver notebook without turning old offsets into folklore.

The source directory index, `ctf-pwn/pwnable-tw/README.md`, is preserved as a historical catalog. Its entries for `re_alloc`, `de_aslr`, `food_store`, `hitcon_ftp`, `seccomptools`, `stupid_boss`, `digimon`, `omegago`, and related advanced cases require comparison with the individual files and actual binary. The atlas favors concrete per-case observations and explicitly leaves unverified exploit claims unverified.
