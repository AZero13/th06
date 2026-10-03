with open('src/FileSystem.cpp', 'r') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if l.startswith('#pragma var_order'):
        lines.insert(i, 'DIFFABLE_STATIC_SORTED(I4, Pbg3Archive **, g_Pbg3Archives);\n\n')
        break

with open('src/FileSystem.cpp', 'w') as f:
    f.writelines(lines)
