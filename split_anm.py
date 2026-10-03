import re

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
            # backtrack to include comments
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
        # find end of namespace
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
lib_code = lines[:funcs[0][1]] # namespace start and stuff

for f, s, e in funcs:
    if f in anim_funcs:
        anim_code.extend(lines[s:e+1])
    elif f in disp_funcs:
        disp_code.extend(lines[s:e+1])
    else:
        lib_code.extend(lines[s:e+1])

lib_code.extend(lines[funcs[-1][2]:]) # namespace end

def write_file(filename, code):
    content = "".join(code)
    # Add includes if not present
    if '#include' not in content:
        content = '#include "th06.hpp"\n#include "AnmManager.hpp"\n\nnamespace th06\n{\n' + content + '}\n'
    with open(filename, 'w') as f:
        f.write(content)

write_file('src/sprtanim.cpp', ['#include "th06.hpp"\n#include "AnmManager.hpp"\n\nnamespace th06\n{\n'] + anim_code + ['}\n'])
write_file('src/sprtdisp.cpp', ['#include "th06.hpp"\n#include "AnmManager.hpp"\n#include "GameWindow.hpp"\n\nnamespace th06\n{\n'] + disp_code + ['}\n'])
write_file('src/AnmManager.cpp', lib_code)
print("AnmManager split done.")
