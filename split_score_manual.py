with open('src/ResultScreen.cpp', 'r') as f:
    lines = f.readlines()

def get_range(start_str, end_str=None):
    start = -1
    for i, l in enumerate(lines):
        if l.startswith(start_str):
            start = i
            break
    while start > 0 and (lines[start-1].startswith('//') or lines[start-1].strip() == '' or lines[start-1].startswith('#pragma')):
        start -= 1
        
    if end_str:
        end = -1
        for i, l in enumerate(lines[start:]):
            if l.startswith(end_str):
                end = start + i
                break
        return list(range(start, end))
    else:
        # Find next function
        end = start
        while True:
            end += 1
            if lines[end].startswith('}'):
                break
        return list(range(start, end+1))

score_indices = set()
for r in [
    get_range('ScoreDat *OpenScore', 'i32 ResultScreen::LinkScore'),
    get_range('ZunResult ParseCatk', 'void ResultScreen::WriteScore')
]:
    for i in r:
        score_indices.add(i)

score_code = [l for i, l in enumerate(lines) if i in score_indices]
result_code = [l for i, l in enumerate(lines) if i not in score_indices]

with open('src/score.cpp', 'w') as f:
    f.write('#include "th06.hpp"\n#include "ResultScreen.hpp"\n\nnamespace th06\n{\n' + "".join(score_code) + '}\n')

with open('src/ResultScreen.cpp', 'w') as f:
    f.writelines(result_code)
