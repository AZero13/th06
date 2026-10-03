with open('src/font.cpp', 'r') as f:
    text = f.read()

text = text.replace('void CMyFont::Init(LPDIRECT3DDEVICE8 lpD3DDEV, int w, int h)\n{', 'void CMyFont::Init(LPDIRECT3DDEVICE8 lpD3DDEV, int w, int h)\n{\n    if (false) FakeMissingPiece();\n')
with open('src/font.cpp', 'w') as f:
    f.write(text)
