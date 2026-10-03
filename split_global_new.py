import os
import re

with open('src/Global.cpp', 'r') as f:
    lines = f.readlines()

def find_lines(pattern):
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            return i
    return -1

font_init_start = find_lines(r'void CMyFont::Init')
fs_start = find_lines(r'u8 \*FileSystem::OpenPath')
err_start = find_lines(r'const char \*GameErrorContext::Log')

font_init_end = fs_start - 1
while not lines[font_init_end].strip() or lines[font_init_end].startswith('//') or "DIFFABLE" in lines[font_init_end] or "Fake_DrawTextA" in lines[font_init_end] or lines[font_init_end].startswith('}'):
    font_init_end -= 1
font_init_end += 1

fs_end = err_start - 1
while not lines[fs_end].strip() or lines[fs_end].startswith('//') or "DIFFABLE" in lines[fs_end]:
    fs_end -= 1
fs_end += 1

font_class_start = find_lines(r'class CMyFont')
font_class_end = font_class_start
while not lines[font_class_end].strip().startswith('};'):
    font_class_end += 1
font_class_end += 1

release_macro = []
fake_draw = []
controller_end = font_init_start - 1
while not lines[controller_end].strip() or lines[controller_end].startswith('//') or "DIFFABLE" in lines[controller_end] or "Fake_DrawTextA" in lines[controller_end] or lines[controller_end].startswith('#define RELEASE'):
    controller_end -= 1
controller_end += 1

for i in range(controller_end, fs_start):
    if lines[i].startswith('#define RELEASE'):
        release_macro = lines[i:i+7]
    if lines[i].startswith('void Fake_DrawTextA'):
        fake_draw = lines[i:i+4]

font_code = lines[font_class_start:font_class_end] + ["\n"] + release_macro + ["\n"] + fake_draw + ["\n"] + lines[font_init_start:font_init_end]

fs_code = []
if lines[fs_start-1].startswith('#pragma var_order'):
    fs_code.append(lines[fs_start-1])
fs_code += lines[fs_start:fs_end]

def write_file(filename, code_lines):
    content = '#include "th06.hpp"\n#include "Global.hpp"\n#include "GameWindow.hpp"\n\nnamespace th06\n{\n'
    content += "".join(code_lines)
    if not content.endswith('\n'):
        content += '\n'
    content += '}\n'
    with open(filename, 'w') as f:
        f.write(content)

write_file('src/grpfont.cpp', font_code)
write_file('src/File.cpp', fs_code)

remove_indices = set()
for i in range(font_class_start, font_class_end): remove_indices.add(i)
for i in range(font_init_start, font_init_end): remove_indices.add(i)
for i in range(fs_start-1, fs_end): 
    if lines[i].startswith('#pragma var_order') or i >= fs_start:
        remove_indices.add(i)
for i, line in enumerate(lines):
    if line.startswith('#define RELEASE'):
        for j in range(i, i+7): remove_indices.add(j)
    if line.startswith('void Fake_DrawTextA'):
        for j in range(i, i+4): remove_indices.add(j)

new_global_lines = [line for i, line in enumerate(lines) if i not in remove_indices]

with open('src/Global.cpp', 'w') as f:
    f.writelines(new_global_lines)

print("Global split done.")
