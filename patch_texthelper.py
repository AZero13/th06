import re
data = open('src/TextHelper.cpp', 'r').read()

# Remove strlen_dummy
data = re.sub(r'void strlen_dummy\(const char\* a\)\s*\{\s*strlen\(a\);\s*\}\s*#pragma intrinsic\(strlen\)\s*', '', data)

# Add ZunFont and unreferenced functions right before TryAllocateBuffer
zunfont_code = '''#include <string>

struct ZunFont
{
    HFONT hFont;
    int width;
    int height;
    std::string name;
    int weight;

    ZunFont()
    {
        this->hFont = NULL;
        this->weight = FW_SEMIBOLD;
        this->height = 16;
        this->width = 0;
        this->name = "MS Gothic";
    }

    ~ZunFont()
    {
        ReleaseFont();
    }

    HFONT GetFont()
    {
        return this->hFont;
    }

    void SetFontSize(int size)
    {
        this->width = 0;
        this->height = size;
    }

    void SetFontName(const char* name)
    {
        this->name = name;
    }

    void SetFont()
    {
        ReleaseFont();
        this->hFont = CreateFontA(this->height,       // cHeight
                                 this->width,         // cWidth
                                 0,                   // CEscapement
                                 0,                   // cOrientation
                                 this->weight,        // cWeight
                                 FALSE,               // bItalic
                                 FALSE,               // bUnderline
                                 FALSE,               // bStrikeOut
                                 DEFAULT_CHARSET,     // iCharSet
                                 OUT_DEFAULT_PRECIS,  // iOutPrecision
                                 CLIP_DEFAULT_PRECIS, // iClipPrecision
                                 DEFAULT_QUALITY,     // iQuality
                                 FF_MODERN,           // iPitchAndFamily
                                 this->name.c_str()); // pszFaceName
    }

    void ReleaseFont()
    {
        if (this->hFont != NULL)
        {
            DeleteObject(this->hFont);
            this->hFont = NULL;
        }
    }
};

ZunBool __FUN_00437380(TextHelper *this_, int x, int y, HFONT font, D3DCOLOR param_5, D3DCOLOR param_6, const char* text)
{
    return 1;
}

ZunBool __FUN_004372a0(TextHelper *this_, int x, int y, int height, D3DCOLOR param_5, D3DCOLOR param_6, const char* text)
{
    ZunFont font;
    this_->width = 0;
    this_->height = height;
    font.SetFont();
    return __FUN_00437380(this_, x, y, font.GetFont(), param_5, param_6, text);
}

'''

data = re.sub(r'(#pragma function\(memset\))', zunfont_code + r'\1', data)
open('src/TextHelper.cpp', 'w').write(data)
