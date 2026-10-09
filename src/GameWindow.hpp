#pragma once
#include "ZunBool.hpp"
#include "decomp.hpp"
#include <windows.h>

#define GAME_WINDOW_WIDTH 640
#define GAME_WINDOW_HEIGHT 480

namespace th06
{
enum RenderResult
{
    RENDER_RESULT_KEEP_RUNNING,
    RENDER_RESULT_EXIT_SUCCESS,
    RENDER_RESULT_EXIT_ERROR,
};

struct GameWindow
{
    RenderResult Render();

    HWND window;
    ZunBool isAppClosing;
    ZunBool isAppActive;
    ZunBool showCursor;
    u8 curFrame;
    alignment_padding(0x3);
    BOOL screenSaveActive;
    BOOL lowPowerActive;
    BOOL powerOffActive;
};

ZUN_ASSERT_TYPE(GameWindow, 0x20, 4);

extern GameWindow g_GameWindow;

extern i32 g_TickCountToEffectiveFramerate;
extern double g_LastFrameTime;
} // namespace th06
