import re
with open('src/pbg3/FileAbstraction.cpp', 'r') as f:
    text = f.read()
text = re.sub(r'u8\* FileAbstraction::MapWholeFile\(\) \{\n.*?\}\n', '', text, flags=re.DOTALL)
with open('src/pbg3/FileAbstraction.cpp', 'w') as f:
    f.write(text)

with open('src/pbg3/FileAbstraction.hpp', 'r') as f:
    text = f.read()
text = text.replace('    u8 *MapWholeFile();\n', '')
with open('src/pbg3/FileAbstraction.hpp', 'w') as f:
    f.write(text)
