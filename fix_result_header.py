with open('src/ResultScreen.cpp', 'r') as f:
    lines = f.readlines()

struct_start = -1
for i, line in enumerate(lines):
    if line.startswith('struct ResultScreen'):
        struct_start = i
        break

struct_end = -1
if struct_start != -1:
    for i in range(struct_start, len(lines)):
        if lines[i].startswith('};'):
            struct_end = i
            break

if struct_start != -1 and struct_end != -1:
    struct_code = lines[struct_start:struct_end+1]
    
    with open('src/ResultScreen.hpp', 'r') as f:
        hpp_lines = f.readlines()
        
    for i, line in enumerate(hpp_lines):
        if line.startswith('namespace th06'):
            # Insert after namespace th06 {
            hpp_lines = hpp_lines[:i+2] + struct_code + ["\n"] + hpp_lines[i+2:]
            break
            
    with open('src/ResultScreen.hpp', 'w') as f:
        f.writelines(hpp_lines)
        
    # Remove from cpp
    new_cpp = lines[:struct_start] + lines[struct_end+1:]
    with open('src/ResultScreen.cpp', 'w') as f:
        f.writelines(new_cpp)
