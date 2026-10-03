with open('src/AnmVm.cpp', 'r') as f:
    lines = f.readlines()

macros = """
#define GET_ARG(type, num) ((type *)curInstr->args)[num]
#define GET_INT_ARG(num) GET_ARG(i32, num)
#define GET_FLOAT_ARG(num) GET_ARG(float, num)
"""

for i, l in enumerate(lines):
    if l.startswith('namespace th06'):
        lines.insert(i+2, macros)
        break

with open('src/AnmVm.cpp', 'w') as f:
    f.writelines(lines)
