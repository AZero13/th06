import re
with open('src/font.cpp', 'r') as f:
    text = f.read()
text = text.replace('DIFFABLE_STATIC_SORTED(J6, LPDIRECT3DSURFACE8, g_TextBufferSurface);', 'DIFFABLE_STATIC_SORTED(J6, LPDIRECT3DSURFACE8, g_TextBufferSurface);\nDIFFABLE_STATIC_SORTED(J3, CMyFont, g_CMyFont);')
with open('src/font.cpp', 'w') as f:
    f.write(text)
