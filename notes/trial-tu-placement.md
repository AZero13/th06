# Trial versus release placement: TU constraints

2026-10-02. Scope: function placement, movement, linkage and compilation-unit boundaries. No IAT or opcode investigation. Trial functions were identified from machine code, not CSV mappings. The experiments themselves do not change game source; the validated follow-up edit is recorded below.

## Calibrating MSVC 7 before interpreting movement

The fixture `build/trial-layout/order-probe/layout.cpp` is compiled through the original `scripts/build.py` toolchain. It contains external functions, file-local static helpers, explicitly inline helpers and an address-taken static function. One identical source file is used for all four runs:

- /Od /Ob1
- /O2 /Ob1
- /O2 /Ob0
- /O2 with its default inlining

Common options include /G5 /Op /Gy /GF. These are standalone fixtures: they do not alter production PCH configuration. This is a COFF emission experiment, not a linked-image equivalence test.

Reading function symbols in COFF section order gives:

```
/Od /Ob1:
ordinary_before
public_a
private_before
public_b
private_middle
public_c
addressed
public_d

/O2 (all three tested inlining settings):
shared_before
private_before
ordinary_before
public_a
private_middle
shared_middle
public_b
public_c
addressed
public_d
```

The static helper `private_before` is defined before ordinary_before/public_a in the source. Under /Od it is emitted immediately after public_a, its first caller. Under /O2 it is emitted before them, in definition order. The second static helper repeats the pattern. External functions retain relative order in this fixture. Inline COMDAT bodies that were absent under /Od are emitted under /O2, although their eventual retention requires a linker experiment.

The existing ABI probe independently shows a file-local helper switching to an EAX argument under /O2, while an external version retains its stack interface.

**What this licenses:** private-helper movement past its caller is possible without any TU split. It gives us a concrete alternative model to test against the trials.

**What it does not license:** claiming all /O2 function order is source order; equating COFF emission with final retention; asserting this fixture reproduces every PCH or COMDAT-selection effect in the game.

## Strong application: all four EoSD bombs share a private helper

The EoSD trial DarkenViewport-equivalent is at 0x404660. Identification is by the rectangle (32,16,416,464), the 60-frame fade intervals, 176 maximum darkness, bomb timer fields and the rectangle drawing call.

Its first draw caller begins at 0x404770; the helper therefore precedes that caller. All four calls to it are:

- 0x40477D
- 0x404C8D
- 0x404FFD
- 0x4053F1

Each prepares the player pointer in EAX. The helper reads player fields through EAX without loading a stack argument.

In release the corresponding helper is 0x406020, immediately after Reimu A draw. Calls at 0x405C1D, 0x4065EA, 0x406B1A and 0x4071BA instead push the player pointer and clean the stack afterwards.

This combines two independent observations that the original compiler reproduces for file-local functions: movement across the first caller and private register argument passing under optimization.

**Preferred ordinary-source model, assuming ordinary per-TU compilation:** one bomb.cpp containing all four bomb implementations and a loose file-local static DarkenViewport helper, defined before the first draw routine (its exact earlier position is not uniquely determined). Under /Od the helper is emitted after that first caller; under /O2 it appears before it.

The trial may have used /GL and link-time code generation; this has not been established or excluded. Cross-TU optimization can weaken the same-TU inference from private register arguments. The no-/GL control proves that /GL is not necessary for this effect, not that the trial lacked it.

A header-local helper instantiated in several TUs and then folded is an alternative that the final EXE alone cannot categorically exclude. There is currently no positive evidence requiring that more complicated model. Separate TH08 bomb files do not establish separate EoSD bomb files.

The current reconstructed `static` member of BombData has external class-member linkage, unlike a file-local static free function. It is therefore worth testing a loose-static version in isolation for byte matching. The follow-up below applies and verifies this change.

## Applying the same standard to other areas

- **Score/result:** the trials have private-register list helpers shared by parsing/cleanup and result wrappers, alongside externally called score entry points. Moving only the parsers into score.cpp cuts through that relationship. Reconstruct the helper/caller group first; parser placement alone does not justify the extraction. Some current method names may represent original loose private functions.
- **ECL/extended handlers:** preserve the existing interpreter/extension division as a plausible working boundary. Both EoSD images have the 17-handler cluster. The two handlers that move ahead of the others need an address-taken-function/visibility experiment; the simple non-address-taken static probe is not proof of their cause.
- **Supervisor/timer/archive/config:** still unproven. Relative movement among these methods must be classified by helper visibility and emission before using it to create Supervisor2 or additional units. Earlier/later placement by itself does not settle the boundary.
- **ANM/ASCII:** retained wrappers coexist with expanded uses in both trials. This supports shared inline-capable definitions, not a new animation split. The first location of a retained helper is not necessarily the location of its only source definition.

## Practical reconstruction order

1. Keep ANM merged and the current two-part ECL organization.
2. Prefer correcting linkage/visibility of private helpers over adding more files to explain movement.
3. First concrete source-layout candidate: the loose static bomb helper, with all bombs in one TU.
4. Next inspect the complete score-helper group; do not move parser functions alone or infer boundaries from Rich counts.
5. Only propose an additional TU after a same-TU compiler model fails and multiple independent code/data groups support the boundary.

Artifacts: `build/trial-layout/order-probe/order.json`, compiler assembly listings, build.log, the fixture and run.py; `build/trial-layout/abi-probe` for register-passing controls. These probes do not modify or relink the game executable.

## Validated release follow-up

Changed DarkenViewport to a loose file-local static helper in BombData.cpp, with its definition and existing var_order pragma before BombReimuADraw. Removed the class-member declaration and updated the four calls. All four bombs remain in one TU. No flags, PCH settings, archive, linker or link order were changed for this edit.

Built the current source baseline and the final edit through scripts/build.py. Full .text bytes, virtual size and VA are identical; .data and .rsrc bytes are identical; import names, slot order and slot addresses are identical. The unchanged .text hash is 1e01ad07caa6943f41669573c03621c36eda5eff68f5fcf022ae732fb83ee712. This proves no .text matching regression from this edit; it does not claim that the pre-existing build matches the target. See build/trial-layout/bomb-static-check/comparison.json.
