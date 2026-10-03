import re
import json

# 1 & 2: Global.cpp -> FileSystem.cpp & font.cpp
with open('src/Global.cpp', 'r') as f:
    lines = f.readlines()

def find_lines(lines_list, pattern):
    for i, line in enumerate(lines_list):
        if re.search(pattern, line):
            return i
    return -1

font_init_start = find_lines(lines, r'void CMyFont::Init')
fs_start = find_lines(lines, r'u8 \*FileSystem::OpenPath')
err_start = find_lines(lines, r'const char \*GameErrorContext::Log')

font_init_end = fs_start - 1
while not lines[font_init_end].strip() or lines[font_init_end].startswith('//') or "DIFFABLE" in lines[font_init_end] or "Fake_DrawTextA" in lines[font_init_end] or lines[font_init_end].startswith('}'):
    font_init_end -= 1
font_init_end += 1

fs_end = err_start - 1
while not lines[fs_end].strip() or lines[fs_end].startswith('//') or "DIFFABLE" in lines[fs_end]:
    fs_end -= 1
fs_end += 1

font_class_start = find_lines(lines, r'class CMyFont')
font_class_end = font_class_start
while not lines[font_class_end].strip().startswith('};'):
    font_class_end += 1
font_class_end += 1

controller_end = font_init_start - 1
while not lines[controller_end].strip() or lines[controller_end].startswith('//') or "DIFFABLE" in lines[controller_end] or "Fake_DrawTextA" in lines[controller_end] or lines[controller_end].startswith('#define RELEASE'):
    controller_end -= 1
controller_end += 1

release_macro = []
fake_draw = []
for i in range(controller_end, fs_start):
    if lines[i].startswith('#define RELEASE'):
        release_macro = lines[i:i+7]
    if lines[i].startswith('void Fake_DrawTextA'):
        fake_draw = lines[i:i+4]

font_code = lines[font_class_start:font_class_end] + ["\n"] + release_macro + ["\n"] + fake_draw + ["\n"] + lines[font_init_start:font_init_end]

fs_code = []
start_idx = fs_start
if lines[fs_start-1].startswith('#pragma var_order'):
    start_idx = fs_start # skip pragma
fs_code = lines[start_idx:fs_end]

remove_indices = set()
for i in range(font_class_start, font_class_end): remove_indices.add(i)
for i in range(font_init_start, font_init_end): remove_indices.add(i)
for i in range(start_idx, fs_end): remove_indices.add(i)
if lines[fs_start-1].startswith('#pragma var_order'):
    remove_indices.add(fs_start-1) # remove the pragma completely from Global.cpp
for i, line in enumerate(lines):
    if line.startswith('#define RELEASE'):
        for j in range(i, i+7): remove_indices.add(j)
    if line.startswith('void Fake_DrawTextA'):
        for j in range(i, i+4): remove_indices.add(j)

new_global_lines = [line for i, line in enumerate(lines) if i not in remove_indices]

# Fix font duplicates
new_font_lines = []
skip = False
for line in font_code:
    if "Fake_DrawTextA" in line:
        if any("Fake_DrawTextA" in l for l in new_font_lines):
            skip = True
            continue
    if skip and "}" in line:
        skip = False
        continue
    if skip: continue
    if "g_Pbg3Archives" in line: continue
    if "var_order" in line: continue
    new_font_lines.append(line)

has_release = any("RELEASE(o)" in l for l in new_font_lines)
if not has_release:
    release_macro = "#define RELEASE(o) \\\n    if (o) \\\n    { \\\n        o->Release(); \\\n        o = NULL; \\\n    }\n"
    for i, line in enumerate(new_font_lines):
        if "void CMyFont::Init" in line:
            new_font_lines.insert(i, release_macro)
            break

def write_file(filename, code_lines, extra_includes=""):
    content = '#include "th06.hpp"\n#include "Global.hpp"\n#include "GameWindow.hpp"\n' + extra_includes + '\nnamespace th06\n{\n'
    content += "".join(code_lines)
    if not content.endswith('\n'):
        content += '\n'
    content += '}\n'
    with open(filename, 'w') as f:
        f.write(content)

write_file('src/font.cpp', new_font_lines)
write_file('src/FileSystem.cpp', fs_code)
with open('src/Global.cpp', 'w') as f:
    f.writelines(new_global_lines)


# 3. ResultScreen.cpp -> score.cpp
with open('src/ResultScreen.cpp', 'r') as f:
    lines = f.readlines()

score_start = find_lines(lines, r'ScoreDat \*OpenScore')
score_end = find_lines(lines, r'ZunResult ResultScreen_RegisterChain')

score_code = lines[score_start:score_end]
new_result = lines[:score_start] + lines[score_end:]

content = '#include "th06.hpp"\n#include "ResultScreen.hpp"\n\nnamespace th06\n{\n'
content += "".join(score_code)
content += '}\n'
with open('src/score.cpp', 'w') as f:
    f.write(content)
with open('src/ResultScreen.cpp', 'w') as f:
    f.writelines(new_result)


# 4 & 5. AnmManager.cpp -> AnmVm.cpp & AnmDisp.cpp
with open('src/AnmManager.cpp', 'r') as f:
    lines = f.readlines()

def find_func_boundaries():
    funcs = []
    current_func = None
    start = -1
    for i, line in enumerate(lines):
        m = re.match(r'^[a-zA-Z_0-9]+.* AnmManager::([a-zA-Z_0-9]+)\(', line)
        if m:
            if current_func:
                funcs.append((current_func, start, i-1))
            current_func = m.group(1)
            start = i
            while start > 0 and (lines[start-1].startswith('//') or lines[start-1].strip() == '' or lines[start-1].startswith('#pragma')):
                start -= 1
        elif line.startswith('ZunResult AnmManager::') or line.startswith('void AnmManager::') or line.startswith('i32 AnmManager::'):
            m = re.match(r'^[a-zA-Z_0-9]+ AnmManager::([a-zA-Z_0-9]+)\(', line)
            if m:
                if current_func:
                    funcs.append((current_func, start, i-1))
                current_func = m.group(1)
                start = i
                while start > 0 and (lines[start-1].startswith('//') or lines[start-1].strip() == '' or lines[start-1].startswith('#pragma')):
                    start -= 1
                    
    if current_func:
        end = len(lines) - 1
        while not lines[end].startswith('} // namespace th06'):
            end -= 1
        funcs.append((current_func, start, end))
    return funcs

funcs = find_func_boundaries()

anim_funcs = ['SetActiveSprite', 'SetAndExecuteScript', 'ExecuteScript']
disp_funcs = ['SetRenderStateForVm', 'DrawInner', 'DrawNoRotation', 'TranslateRotation', 'Draw', 'DrawFacingCamera', 'Draw3', 'Draw2', 'DrawTextToSprite', 'DrawVmTextFmt', 'DrawStringFormat', 'DrawStringFormat2']

anim_code = []
disp_code = []
lib_code = lines[:funcs[0][1]]

for f, s, e in funcs:
    if f in anim_funcs:
        anim_code.extend(lines[s:e+1])
    elif f in disp_funcs:
        disp_code.extend(lines[s:e+1])
    else:
        lib_code.extend(lines[s:e+1])

lib_code.extend(lines[funcs[-1][2]:])

def write_anm_file(filename, code):
    content = "".join(code)
    if '#include' not in content:
        content = '#include "th06.hpp"\n#include "AnmManager.hpp"\n#include "GameWindow.hpp"\n\nnamespace th06\n{\n' + content + '}\n'
    with open(filename, 'w') as f:
        f.write(content)

write_anm_file('src/AnmVm.cpp', ['#include "th06.hpp"\n#include "AnmManager.hpp"\n\nnamespace th06\n{\n'] + anim_code + ['}\n'])
write_anm_file('src/AnmDisp.cpp', ['#include "th06.hpp"\n#include "AnmManager.hpp"\n#include "GameWindow.hpp"\n\nnamespace th06\n{\n'] + disp_code + ['}\n'])
with open('src/AnmManager.cpp', 'w') as f:
    f.writelines(lib_code)


# 6. Update configs
with open('objdiff.json', 'r') as f:
    objdiff = json.load(f)

new_objects = [
    {"name": "FileSystem", "target_path": "build/objdiff/orig/FileSystem.obj", "base_path": "build/objdiff/reimpl/FileSystem.obj", "reverse_fn_order": False},
    {"name": "font", "target_path": "build/objdiff/orig/font.obj", "base_path": "build/objdiff/reimpl/font.obj", "reverse_fn_order": False},
    {"name": "score", "target_path": "build/objdiff/orig/score.obj", "base_path": "build/objdiff/reimpl/score.obj", "reverse_fn_order": False},
    {"name": "AnmVm", "target_path": "build/objdiff/orig/AnmVm.obj", "base_path": "build/objdiff/reimpl/AnmVm.obj", "reverse_fn_order": False},
    {"name": "AnmDisp", "target_path": "build/objdiff/orig/AnmDisp.obj", "base_path": "build/objdiff/reimpl/AnmDisp.obj", "reverse_fn_order": False},
]

objects = [obj for obj in objdiff['objects'] if obj['name'] not in ('FileSystem', 'font', 'score', 'AnmVm', 'AnmDisp')]
global_idx = next(i for i, obj in enumerate(objects) if obj['name'] == 'Global')
objects[global_idx+1:global_idx+1] = new_objects
objdiff['objects'] = objects

with open('objdiff.json', 'w') as f:
    json.dump(objdiff, f, indent=4)

with open('config/ghidra_ns_to_obj.csv', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('Global,'):
        new_lines.append('Global,th06::Chain,th06::ChainElem,th06::Controller,th06::GameErrorContext,th06::Rng,th06::utils\n')
        new_lines.append('font,th06::CMyFont\n')
        new_lines.append('FileSystem,th06::FileSystem\n')
    elif line.startswith('ResultScreen,'):
        new_lines.append('ResultScreen,th06::ResultScreen\n')
        new_lines.append('score,th06::OpenScore,th06::ParseCatk\n')
    elif line.startswith('AnmManager,'):
        new_lines.append('AnmManager,th06::AnmManager\n')
        new_lines.append('AnmVm,th06::AnmVm\n')
        new_lines.append('AnmDisp,th06::AnmDisp\n')
    elif line.startswith('FileSystem,') or line.startswith('font,') or line.startswith('score,') or line.startswith('AnmVm,') or line.startswith('AnmDisp,'):
        continue
    else:
        new_lines.append(line)

new_lines.sort()

with open('config/ghidra_ns_to_obj.csv', 'w') as f:
    f.writelines(new_lines)

with open('scripts/configure.py', 'r') as f:
    content = f.read()

import re
content = re.sub(r'"FileSystem",\s*', '', content)
content = re.sub(r'"font",\s*', '', content)
content = re.sub(r'"score",\s*', '', content)
content = re.sub(r'"AnmVm",\s*', '', content)
content = re.sub(r'"AnmDisp",\s*', '', content)

new_sources = '"FileSystem",\n            "font",\n            "score",\n            "AnmVm",\n            "AnmDisp",'
content = content.replace('"Global",', '"Global",\n            ' + new_sources)

with open('scripts/configure.py', 'w') as f:
    f.write(content)

print("Master split done.")
