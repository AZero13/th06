with open('src/ResultScreen.hpp', 'r') as f:
    lines = f.readlines()

start_idx = -1
for i, l in enumerate(lines):
    if l.startswith('struct ResultScreen'):
        start_idx = i
        break

if start_idx != -1:
    end_idx = start_idx
    for i in range(start_idx, len(lines)):
        if lines[i].startswith('};'):
            end_idx = i
            break
            
    struct_code = lines[start_idx:end_idx+1]
    lines = lines[:start_idx] + lines[end_idx+1:]
    
    # insert at the end before }
    insert_idx = -1
    for i, l in enumerate(lines):
        if l.startswith('} // namespace th06'):
            insert_idx = i
            break
            
    if insert_idx != -1:
        lines = lines[:insert_idx] + struct_code + ["\n"] + lines[insert_idx:]
        
    with open('src/ResultScreen.hpp', 'w') as f:
        f.writelines(lines)
