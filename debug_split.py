import re
with open('src/AnmManager.cpp', 'r') as f:
    lines = f.readlines()
funcs = []
current_func = None
start = -1
for i, line in enumerate(lines):
    m = re.match(r'^[a-zA-Z_0-9]+.* AnmManager::([a-zA-Z_0-9]+)\(', line)
    if not m and (line.startswith('ZunResult ') or line.startswith('void ') or line.startswith('i32 ')):
        m = re.match(r'^[a-zA-Z_0-9]+ AnmManager::([a-zA-Z_0-9]+)\(', line)
    
    if m and (line.startswith('return') or line.strip().startswith('if') or line.strip().startswith('while') or line.strip().startswith('for') or line.strip().startswith('=')):
        m = None
        
    if m:
        func_name = m.group(1)
        temp_start = i
        while temp_start > 0 and (lines[temp_start-1].startswith('//') or lines[temp_start-1].strip() == '' or lines[temp_start-1].startswith('#pragma')):
            temp_start -= 1
        
        if current_func:
            funcs.append((current_func, start, temp_start - 1))
        
        current_func = func_name
        start = temp_start

if current_func:
    end = len(lines) - 1
    while not lines[end].startswith('} // namespace th06'):
        end -= 1
    funcs.append((current_func, start, end))

for f, s, e in funcs:
    print(f, s, e)
