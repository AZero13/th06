with open('src/Global.cpp', 'r') as f:
    text = f.read()

text = text.replace('void CMyFont::Init', 'void CMyFont::Init(LPDIRECT3DDEVICE8 lpD3DDEV, int w, int h) { if (false) FakeMissingPiece(); }\nvoid CMyFont::Init_old')
with open('src/Global.cpp', 'w') as f:
    f.write(text)
