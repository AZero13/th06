#pragma once
#include <d3d8.h>
#include <d3dx8.h>

namespace th06 {
class CMyFont
{
  private:
    LPD3DXFONT m_lpFont;

  public:
    CMyFont()
    {
        m_lpFont = NULL;
    }
    virtual void Init(LPDIRECT3DDEVICE8 lpD3DDEV, int w, int h);
    virtual void Print(char *str, int x, int y, D3DCOLOR color = 0xFFFFFFFF);
    virtual void Clean();
};
}
