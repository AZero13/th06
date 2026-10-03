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
    if m:
        func_name = m.group(1)
        if current_func:
            funcs.append((current_func))
        current_func = func_name
        start = i
if current_func:
    funcs.append(current_func)
print(funcs)
