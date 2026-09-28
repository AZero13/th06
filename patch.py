import re
data = open('src/TextHelper.cpp').read()
code = '''#include <string>

struct ZunFont {
    HFONT hFont;
    int width;
    int height;
    std::string name;
    int weight;

    ZunFont() {
        hFont = NULL;
        weight = FW_SEMIBOLD;
        height = 16;
        width = 0;
        name = "MS Gothic";
    }

    ~ZunFont() {
        ReleaseFont();
    }

    HFONT GetFont() {
        return hFont;
    }

    void SetFont() {
        ReleaseFont();
        hFont = CreateFontA(height, width, 0, 0, weight, FALSE, FALSE, FALSE, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, FF_MODERN, name.c_str());
    }

    void ReleaseFont() {
        if (hFont) {
            DeleteObject(hFont);
            hFont = NULL;
        }
    }
};

struct GdiManager {
    virtual ~GdiManager() {}
    virtual bool __FUN_00437380(int x, int y, HFONT font, D3DCOLOR param_5, D3DCOLOR param_6, const char* text) {
        return true;
    }
    virtual bool __FUN_004372a0(int x, int y, int height, D3DCOLOR param_5, D3DCOLOR param_6, const char* text) {
        ZunFont font;
        font.height = height;
        font.width = 0;
        font.SetFont();
        return __FUN_00437380(x, y, font.GetFont(), param_5, param_6, text);
    }
};

GdiManager g_GdiManager;

'''

data = re.sub(r'(struct THBITMAPINFO)', code + r'\1', data)
open('src/TextHelper.cpp', 'w').write(data)
