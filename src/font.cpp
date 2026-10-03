#include "th06.hpp"
#include "Global.hpp"
#include "font.hpp"
#include "GameWindow.hpp"

namespace th06
{



void CMyFont::Init(LPDIRECT3DDEVICE8 lpD3DDEV, int w, int h)
{

    HDC hTextDC = NULL;
    HFONT hFont = NULL, hOldFont = NULL;

    hTextDC = CreateCompatibleDC(NULL);
    hFont = CreateFont(h, w, 0, 0, FW_REGULAR, FALSE, FALSE, FALSE, SHIFTJIS_CHARSET, OUT_DEFAULT_PRECIS,
                       CLIP_DEFAULT_PRECIS, DEFAULT_QUALITY, DEFAULT_PITCH, TH_FONT_NAME);
    if (!hFont)
        return;
    hOldFont = (HFONT)SelectObject(hTextDC, hFont);

    if (FAILED(D3DXCreateFont(lpD3DDEV, hFont, &m_lpFont)))
    {
        MessageBox(NULL, "D3DXCreateFontIndirect FALSE", "ok", MB_OK);
        return;
    }
    SelectObject(hTextDC, hOldFont);
    DeleteObject(hFont);
}

DIFFABLE_STATIC_SORTED(J6, LPDIRECT3DSURFACE8, g_TextBufferSurface);
DIFFABLE_STATIC_SORTED(J3, CMyFont, g_CMyFont);


// ----------------------------------------------------------------------------
void CMyFont::Print(char *str, int x, int y, D3DCOLOR color)
{
    RECT rect;
    rect.left = x;
    rect.right = GAME_WINDOW_WIDTH;
    rect.top = y;
    rect.bottom = GAME_WINDOW_HEIGHT;

    m_lpFont->DrawText(str, -1, &rect, DT_LEFT | DT_EXPANDTABS, color);
}
// ----------------------------------------------------------------------------
void CMyFont::Clean()
{
    RELEASE(m_lpFont);
}


}
