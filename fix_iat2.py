import re
with open('src/Global.hpp', 'r') as f:
    text = f.read()

# Extract FakeMissingPiece
func = re.search(r'    inline void FakeMissingPiece\(\) \{.*?\}\n', text, re.DOTALL)
if func:
    text = text.replace(func.group(0), '')
    text = text + '\n' + func.group(0).replace('    inline void', 'inline void')
    with open('src/Global.hpp', 'w') as f:
        f.write(text)
