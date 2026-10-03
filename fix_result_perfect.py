with open('src/ResultScreen.cpp', 'r') as f:
    cpp_lines = f.readlines()

# Extract struct ResultScreen
struct_start = -1
for i, line in enumerate(cpp_lines):
    if line.startswith('struct ResultScreen'):
        struct_start = i
        break

struct_end = -1
if struct_start != -1:
    for i in range(struct_start, len(cpp_lines)):
        if cpp_lines[i].startswith('};'):
            struct_end = i
            break

struct_code = cpp_lines[struct_start:struct_end+1]

# Delete struct ResultScreen from cpp
new_cpp = cpp_lines[:struct_start] + cpp_lines[struct_end+1:]

# Insert struct ResultScreen into hpp before } // namespace th06
with open('src/ResultScreen.hpp', 'r') as f:
    hpp_lines = f.readlines()

insert_idx = -1
for i, line in enumerate(hpp_lines):
    if line.startswith('} // namespace th06'):
        insert_idx = i
        break

hpp_lines = hpp_lines[:insert_idx] + struct_code + ["\n"] + hpp_lines[insert_idx:]

# Also add #include "MainMenu.hpp" to hpp
for i, line in enumerate(hpp_lines):
    if line.startswith('#include "Global.hpp"'):
        hpp_lines.insert(i+1, '#include "MainMenu.hpp"\n')
        break

# Forward declare struct ResultScreen at the top of hpp?
# Actually, the struct is now at the bottom of hpp, after ScoreListNode etc.
# Some methods take ResultScreen*, so maybe we need a forward declaration at the top?
# Let's add `struct ResultScreen;` right after `namespace th06 {`
for i, line in enumerate(hpp_lines):
    if line.startswith('namespace th06'):
        hpp_lines.insert(i+2, 'struct ResultScreen;\n')
        break

with open('src/ResultScreen.hpp', 'w') as f:
    f.writelines(hpp_lines)

with open('src/ResultScreen.cpp', 'w') as f:
    f.writelines(new_cpp)
