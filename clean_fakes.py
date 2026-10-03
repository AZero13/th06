with open('src/font.cpp', 'r') as f:
    text = f.read()
text = text.replace('    if (false) FakeMissingPiece();\n', '')
text = text.replace('void Fake_DrawTextA()\n{\n    void *fake = (void *)&DrawText;\n}\n', '')
with open('src/font.cpp', 'w') as f:
    f.write(text)

with open('src/Global.hpp', 'r') as f:
    text = f.read()
import re
text = re.sub(r'inline void FakeMissingPiece\(\) \{.*?\n\}\n', '', text, flags=re.DOTALL)
with open('src/Global.hpp', 'w') as f:
    f.write(text)
