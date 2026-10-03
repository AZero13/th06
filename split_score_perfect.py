import re

with open('src/ResultScreen.cpp', 'r') as f:
    lines = f.readlines()

def find_func_boundaries():
    funcs = []
    current_func = None
    start = -1
    for i, line in enumerate(lines):
        # Match function definitions like "ZunResult ParseCatk(" or "ScoreDat *OpenScore(" or "u32 GetHighScore("
        m = re.match(r'^([a-zA-Z_0-9]+[ \t\*]+)+([a-zA-Z_0-9:]+)\(', line)
        if m and not line.startswith('return') and not line.startswith('if') and not line.startswith('while') and not line.startswith('for'):
            if current_func:
                funcs.append((current_func, start, i-1))
            current_func = m.group(2)
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

score_funcs = ['OpenScore', 'GetHighScore', 'ParseCatk', 'ParseClrd', 'ParsePscr', 'ReleaseScoreDat']

score_code = []
result_code = lines[:funcs[0][1]]

for f, s, e in funcs:
    if f in score_funcs:
        score_code.extend(lines[s:e+1])
    else:
        result_code.extend(lines[s:e+1])

result_code.extend(lines[funcs[-1][2]:])

with open('src/score.cpp', 'w') as f:
    content = '#include "th06.hpp"\n#include "ResultScreen.hpp"\n\nnamespace th06\n{\n' + "".join(score_code) + '}\n'
    f.write(content)

with open('src/ResultScreen.cpp', 'w') as f:
    f.writelines(result_code)
