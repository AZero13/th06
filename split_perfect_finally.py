import re

def process_file(filename, score_funcs, class_name, out_file1, out_file2, out_funcs1, out_funcs2):
    with open(filename, 'r') as f:
        lines = f.readlines()

    funcs = []
    current_func = None
    start = -1
    for i, line in enumerate(lines):
        if class_name:
            # For AnmManager: match "AnmManager::FunctionName("
            m = re.match(r'^[a-zA-Z_0-9]+.* ' + class_name + r'::([a-zA-Z_0-9]+)\(', line)
            if not m and (line.startswith('ZunResult ') or line.startswith('void ') or line.startswith('i32 ')):
                m = re.match(r'^[a-zA-Z_0-9]+ ' + class_name + r'::([a-zA-Z_0-9]+)\(', line)
        else:
            # For ResultScreen (global score functions and ResultScreen:: functions)
            m = re.match(r'^([a-zA-Z_0-9]+[ \t\*]+)+([a-zA-Z_0-9:]+)\(', line)
            if m and (line.startswith('return') or line.startswith('if') or line.startswith('while') or line.startswith('for')):
                m = None
        
        if m:
            func_name = m.group(1) if class_name else m.group(2)
            temp_start = i
            while temp_start > 0 and (lines[temp_start-1].startswith('//') or lines[temp_start-1].strip() == '' or lines[temp_start-1].startswith('#pragma')):
                temp_start -= 1
            
            if current_func:
                funcs.append((current_func, start, temp_start - 1)) # FIXED! temp_start - 1 instead of i - 1
            
            current_func = func_name
            start = temp_start
            
    if current_func:
        end = len(lines) - 1
        while not lines[end].startswith('} // namespace th06'):
            end -= 1
        funcs.append((current_func, start, end))

    lib_code = lines[:funcs[0][1]]
    code1 = []
    code2 = []

    for f, s, e in funcs:
        if f in out_funcs1:
            code1.extend(lines[s:e+1])
        elif f in out_funcs2:
            code2.extend(lines[s:e+1])
        else:
            lib_code.extend(lines[s:e+1])

    lib_code.extend(lines[funcs[-1][2]:])

    if out_file1:
        with open(out_file1, 'w') as f:
            if 'score' in out_file1:
                f.write('#include "th06.hpp"\n#include "ResultScreen.hpp"\n\nnamespace th06\n{\n' + "".join(code1) + '}\n')
            else:
                f.write('#include "th06.hpp"\n#include "AnmManager.hpp"\n\nnamespace th06\n{\n' + "".join(code1) + '}\n')
    
    if out_file2:
        with open(out_file2, 'w') as f:
            f.write('#include "th06.hpp"\n#include "AnmManager.hpp"\n#include "GameWindow.hpp"\n\nnamespace th06\n{\n' + "".join(code2) + '}\n')
            
    with open(filename, 'w') as f:
        f.writelines(lib_code)

process_file('src/ResultScreen.cpp', None, None, 'src/score.cpp', None, ['OpenScore', 'GetHighScore', 'ParseCatk', 'ParseClrd', 'ParsePscr', 'ReleaseScoreDat'], [])

anim_funcs = ['SetActiveSprite', 'SetAndExecuteScript', 'ExecuteScript']
disp_funcs = ['SetRenderStateForVm', 'DrawInner', 'DrawNoRotation', 'TranslateRotation', 'Draw', 'DrawFacingCamera', 'Draw3', 'Draw2', 'DrawTextToSprite', 'DrawVmTextFmt', 'DrawStringFormat', 'DrawStringFormat2']
process_file('src/AnmManager.cpp', None, 'AnmManager', 'src/AnmVm.cpp', 'src/AnmDisp.cpp', anim_funcs, disp_funcs)
