with open('src/FileSystem.cpp', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('u8 *FileSystem::OpenPath'):
        lines.insert(i, '#pragma var_order(pbg3Idx, entryname, entryIdx, fsize, data, file)\n')
        break

with open('src/FileSystem.cpp', 'w') as f:
    f.writelines(lines)
