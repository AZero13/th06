import re
with open('src/font.cpp', 'r') as f:
    text = f.read()
text = re.sub(r'void Fake_DrawTextA\(\)\n\{\n    DrawTextA\(NULL, NULL, 0, NULL, 0\);\n\}\n', '', text)
with open('src/font.cpp', 'w') as f:
    f.write(text)

with open('src/TextHelper.cpp', 'r') as f:
    text = f.read()
text = re.sub(r'void Fake_TextOutA_SetBkMode_SetTextColor_CxxThrowException\(\)\n\{\n    TextOutA\(NULL, 0, 0, NULL, 0\);\n    SetBkMode\(NULL, 0\);\n    SetTextColor\(NULL, 0\);\n    _CxxThrowException\(NULL, NULL\);\n\}\n', '', text)
with open('src/TextHelper.cpp', 'w') as f:
    f.write(text)
