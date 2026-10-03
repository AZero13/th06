# 1. Move RELEASE to th06.hpp
with open('src/font.cpp', 'r') as f:
    font_lines = f.readlines()

new_font_lines = []
skip = False
for l in font_lines:
    if l.startswith('#define RELEASE(o)'):
        skip = True
        continue
    if skip and l.strip() == '}':
        skip = False
        continue
    if skip:
        continue
    new_font_lines.append(l)

with open('src/font.cpp', 'w') as f:
    f.writelines(new_font_lines)

with open('src/th06.hpp', 'r') as f:
    th06_lines = f.readlines()

for i, l in enumerate(th06_lines):
    if l.startswith('namespace th06'):
        th06_lines.insert(i, '#define RELEASE(o) \\\n    if (o) \\\n    { \\\n        (o)->Release(); \\\n        (o) = NULL; \\\n    }\n\n')
        break

with open('src/th06.hpp', 'w') as f:
    f.writelines(th06_lines)

# 2. Move g_CMyFont from Global.cpp to font.cpp
with open('src/Global.cpp', 'r') as f:
    global_lines = f.readlines()

new_global = []
g_font_line = ""
for l in global_lines:
    if 'CMyFont, g_CMyFont' in l:
        g_font_line = l
        continue
    if l.startswith('// CMyFont'):
        continue
    new_global.append(l)

with open('src/Global.cpp', 'w') as f:
    f.writelines(new_global)

with open('src/font.cpp', 'r') as f:
    font_lines = f.readlines()

for i, l in enumerate(font_lines):
    if l.startswith('CMyFont::CMyFont()'):
        font_lines.insert(i, g_font_line + '\n')
        break

with open('src/font.cpp', 'w') as f:
    f.writelines(font_lines)

