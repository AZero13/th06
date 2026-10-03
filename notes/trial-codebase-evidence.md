# What the two supplied trials expose about the source

Analysis date: 2026-10-02. Inputs: the supplied EoSD trial `th06tr.exe` and PCB trial `th07tr.exe`. All addresses below are virtual addresses in those binaries. Identifications use instructions, constants, data layouts and call relationships; no CSV address mappings were used. Names describe corresponding behavior in the reconstruction, not recovered original symbols.

Reproducible evidence is in `build/trial-layout/analyze_inline_evidence.py`, `inline-evidence.json`, and the two `*-inline-excerpts.asm` files. The JSON includes input SHA-256 hashes and every direct caller of the listed helpers. Direct-call counts exclude indirect calls and inlined uses. Tail jumps are recorded separately.

## 1. The ASCII/ANM helper is selectively expanded in both trials

| Behavior | EoSD trial | PCB trial |
|---|---:|---:|
| Initialize VM | 0x4010E0 | 0x401170 |
| Initialize VM, then set sprite | 0x401180 | 0x401240 |
| ASCII VM setup | 0x401220 | 0x4013F0 |
| Set active sprite | 0x420C40 | 0x42F5A0 |

Both binaries retain a callable wrapper taking a VM and sprite index. It invokes VM initialization, then sprite selection, and returns with `ret 8`.

EoSD has three direct calls to that wrapper: 0x4196D1, 0x419762, 0x41EE16. PCB has one at 0x42D410.

Nevertheless, ASCII VM setup in **both** binaries directly invokes VM initialization and sprite selection twice, for indices 0 and 32. The manager pointer is captured before initializing the VM and then used for sprite selection. This agrees with expansion of the manager wrapper; it does not require a separately written, manually expanded ASCII implementation. Equivalent handwritten code remains possible, so this is strong source-model evidence rather than proof of the original spelling.

There is also a matching expanded pair elsewhere: EoSD calls at 0x40EB1C/0x40EB27 and PCB calls at 0x41AB7A/0x41AB85.

**Consequence:** retain an inline-capable `InitializeAndSetSprite` abstraction. Its callable body and expanded uses can coexist. Do not split animation solely to force the same inlining decision at every call site. This does not yet resolve release stack padding or identify precisely where the definition was visible.

ASCII VM setup itself is called three times in each trial:

- EoSD: 0x401303, 0x413174, 0x4131DC.
- PCB: 0x40161E, 0x41F7E0, 0x4205BB.

Thus a retained callable ASCII initializer is normal in these optimized builds; retention alone does not distinguish an explicitly inline declaration from an ordinary function.

## 2. The nested RNG operations survive as both callable and expanded code

| Routine | EoSD trial | PCB trial |
|---|---:|---:|
| GetRandomU16 | 0x413C70 | 0x4209D0 |
| GetRandomU32 | 0x413CA0 | 0x420A00 |
| GetRandomF32ZeroToOne | 0x413D00 | 0x420A60 |
| GetRandomU32InRange | 0x405630 | 0x401110 |

The U16 routines are byte-identical across trials (35 bytes), as are the U32 routines (84 bytes). U32 contains two seed transitions using XOR 0x9630 and subtraction 0x6553, increments the generation count by two, and combines the generated words. It does not call the retained U16 routine. The float routines contain that same two-transition computation rather than calling the retained U32 routine.

This strongly supports nested optimizer expansion. It does **not** require adding `inline` to the RNG source: ordinary definitions visible in the same TU can produce it under optimization.

EoSD's range helper has three direct callers at 0x40636E, 0x4063B7 and 0x406FE6. PCB's has 22, including 0x431E29 well beyond the earlier cluster. The EoSD caller observation must not be generalized to PCB. A helper surviving near the front of the executable does not locate its users or uniquely locate its original TU.

There is a floating-point code-generation difference: EoSD stores/reloads a float intermediate and divides by 4294967296.0; PCB multiplies the converted integer by 2^-32 without that intermediate store/reload. This exposes a precision/code-generation or source-expression difference worth preserving. It does not uniquely identify a compiler flag, and does not establish that the final rounded float differs.

## 3. Some differences are real initialization semantics, not just inlining

EoSD's VM initializer ends with a tail jump to the timer initializer at 0x418321. That function writes current=0, previous=-1, subFrame=0.

PCB's VM initializer directly writes the timer fields at VM+0x30/+0x34/+0x38 with previous=-999 and the other two zero. PCB also retains a timer setter at 0x401150 that takes a new current value and writes previous=-999, subFrame=0; its direct callers are 0x4127C6 and 0x412A0B.

**Consequence:** do not replace EoSD's `Initialize()` with PCB's apparent `SetCurrent(0)`/assignment behavior merely to reproduce inlining. The sentinel values differ. The supplied PCB code is evidence about development, not a drop-in specification for EoSD.

VM layout also changed: the ASCII routines operate on VM pairs separated by 0x110 in EoSD and 0x240 in PCB. Do not transport member offsets or infer identical class definitions.

## 4. Public score entry points and private list helpers need separate reasoning

EoSD OpenScore at 0x41DD4F has three direct calls, at 0x412E0F, 0x41EEDD and 0x424E30. PCB OpenScore at 0x42B9D0 likewise has three, at 0x4201A1, 0x42D4F1 and 0x4363D7. EoSD's CATK parser at 0x41CF90 has calls at 0x412E3F and 0x41EF2A. Calls from other subsystems fit public score entry points; earlier placement alone does not make the parsers private static functions.

The list helpers give a different clue. EoSD list cleanup at 0x41DD35 takes its argument in EAX; insertion at 0x41DCEA uses EAX and EBX. PCB cleanup at 0x42B9B6 uses the same EAX interface. Their callers explicitly prepare those registers.

An isolated MSVC 7 experiment (`build/trial-layout/abi-probe`) reproduces the EAX argument for a file-local static cleanup helper. The otherwise identical external helper reads the stack argument. Both fixtures were built through `scripts/build.py` with compiler 13.00.9466, /O2 /Ob0 /Gy.

This favors private list helpers compiled with the score operations and wrappers that use them. It does not prove a unique CPP boundary: internal definitions in a shared header plus folding, or other whole-program machinery, would need separate investigation. A static class member is not automatically a file-local function.

**Consequence:** the current extraction into score.cpp is not established merely by parser ordering. Review the entire set of list operations and result wrappers before treating that split as recovered source structure.

## 5. Early shared helpers are poor standalone boundary markers

Matrix identity is at 0x401080 (EoSD) and 0x4010D0 (PCB). Each has three direct callers, all substantially later in the image. VM initialization contains the identity stores directly.

Timer tick is at 0x4010C0 (EoSD) and 0x401130 (PCB), with four direct callers each. Other timer operations can be expanded without calling these retained bodies.

The vector constructor iterator is present in both trials: 0x401000 in EoSD and 0x401210 in PCB, with identical 42-byte bodies. A placement difference is not evidence that PCB lacks the helper or uses a different iterator implementation.

## Working source model

- Keep ECL interpreter and extended handlers as the existing two candidate TUs; do not add a third merely because shared RNG/timer bodies appear elsewhere.
- Keep ANM merged. Shared inline-capable helpers with selective expansion explain the observed ASCII/ANM pattern without another split.
- Preserve EoSD timer semantics; use PCB to identify candidate abstractions, then validate each against EoSD.
- Investigate score helper linkage and complete caller groups before further score/result extraction.
- Do not infer original filenames, the `inline` keyword, PCH boundaries, or exact flags from retention or address order alone.

No production source refactor was performed for this analysis. The earlier stale AnmVm/AnmDisp build and comparison entries were removed to reflect the user's animation merge. IAT investigation is deferred at the user's request.
