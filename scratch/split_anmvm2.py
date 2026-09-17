import re

with open('src/AnmVm.hpp', 'r') as f:
    hpp = f.read()

# I want to split at "    D3DXVECTOR3 pos;"
# Let's find that line.
pos_idx = hpp.find("    D3DXVECTOR3 pos;")

part1 = hpp[:pos_idx]
part2 = hpp[pos_idx:]

# part1 ends with:
#     i16 posInterpEndTime;
#     // Two padding bytes
# We need to close AnmVmBase and start AnmVm here.

new_hpp = part1 + "};\nZUN_ASSERT_SIZE(AnmVmBase, 0x84);\n\nstruct AnmVm : public AnmVmBase\n{\n    AnmVm();\n" + part2

# Now we need to remove the old closing of AnmVmBase at the end of the file.
new_hpp = new_hpp.replace("""    u8 fontWidth;
    u8 fontHeight;
    // Two final padding bytes
};
ZUN_ASSERT_SIZE(AnmVmBase, 0x110);

struct AnmVm : public AnmVmBase
{
    AnmVm();
};
ZUN_ASSERT_SIZE(AnmVm, 0x110);""", """    u8 fontWidth;
    u8 fontHeight;
    // Two final padding bytes
};
ZUN_ASSERT_SIZE(AnmVm, 0x110);""")

with open('src/AnmVm.hpp', 'w') as f:
    f.write(new_hpp)

