with open('src/font.cpp', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "Fake_DrawTextA" in line:
        if any("Fake_DrawTextA" in l for l in new_lines):
            skip = True
            continue
    if skip and "}" in line:
        skip = False
        continue
    if skip:
        continue
    if "g_Pbg3Archives" in line:
        continue
    if "var_order" in line:
        continue
    new_lines.append(line)

has_release = any("RELEASE(o)" in l for l in new_lines)
if not has_release:
    release_macro = """
#define RELEASE(o) \\
    if (o) \\
    { \\
        o->Release(); \\
        o = NULL; \\
    }
"""
    for i, line in enumerate(new_lines):
        if "void CMyFont::Init" in line:
            new_lines.insert(i, release_macro)
            break

with open('src/font.cpp', 'w') as f:
    f.writelines(new_lines)
