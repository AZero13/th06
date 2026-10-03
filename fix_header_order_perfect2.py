with open('src/ResultScreen.hpp', 'r') as f:
    lines = f.readlines()

def extract_struct(name, lines):
    start = -1
    for i, line in enumerate(lines):
        if line.startswith(f'struct {name}\n'):
            start = i
            break
    if start == -1:
        return []
    end = start
    for i in range(start, len(lines)):
        if lines[i].startswith('ZUN_ASSERT_TYPE(' + name) or (name == 'ResultScreen' and lines[i].startswith('};')):
            if lines[i].startswith('};'):
                if i+1 < len(lines) and lines[i+1].startswith('ZUN_ASSERT_TYPE(' + name):
                    end = i+1
                else:
                    end = i
            else:
                end = i
            break
    
    code = lines[start:end+1]
    code.append('\n')
    for i in range(start, end+1):
        lines[i] = ''
    return code

git_lines = open('git_result.hpp', 'r').readlines()
lines = git_lines

structs = []
for name in ['Th6k', 'Catk', 'Clrd', 'Pscr', 'Hscr', 'ScoreListNode', 'ScoreDat']:
    structs.extend(extract_struct(name, lines))

# ResultScreen is currently at bottom of git_result.hpp? NO! In git_result.hpp it is NOT THERE!
# ResultScreen is in the modified ResultScreen.hpp (which I will grab from the current one)
cur_lines = open('src/ResultScreen.hpp', 'r').readlines()
rs_code = extract_struct('ResultScreen', cur_lines)
structs.extend(rs_code)

# Insert after enums
insert_idx = -1
for i, line in enumerate(lines):
    if line.startswith('enum ResultScreenMainMenuCursor'):
        for j in range(i, len(lines)):
            if lines[j].startswith('};'):
                insert_idx = j + 2
                break
        break

if insert_idx != -1:
    lines = lines[:insert_idx] + structs + lines[insert_idx:]

final_lines = [l for l in lines if l != '']
# add #include "MainMenu.hpp"
for i, l in enumerate(final_lines):
    if '#include "Global.hpp"' in l:
        final_lines.insert(i+1, '#include "MainMenu.hpp"\n')
        break

with open('src/ResultScreen.hpp', 'w') as f:
    f.writelines(final_lines)
