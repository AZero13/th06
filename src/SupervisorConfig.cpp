#include "AnmManager.hpp"
#include "AsciiManager.hpp"
#include "Chain.hpp"
#include "ChainPriorities.hpp"
#include "Ending.hpp"
#include "GameManager.hpp"
#include "GameWindow.hpp"
#include "Global.hpp"
#include "MainMenu.hpp"
#include "MusicRoom.hpp"
#include "ReplayManager.hpp"
#include "ResultScreen.hpp"
#include "SoundPlayer.hpp"
#include "Supervisor.hpp"
#include "TextHelper.hpp"
#include "ZunTimer.hpp"
#include "i18n.hpp"
#include "inttypes.hpp"

#include <stdio.h>
#include <string.h>

namespace th06
{
#pragma var_order(data, wavFile, wavFile2)
ZunResult Supervisor::LoadConfig(const char *path)
{
    GameConfiguration *data;
    FILE *wavFile;
    FILE *wavFile2;

    memset(&g_Supervisor.cfg, 0, sizeof(GameConfiguration));
    g_Supervisor.cfg.opts.useSwTextureBlending = true;
    data = (GameConfiguration *)FileSystem::OpenPath(path, EXTERNAL_FILE);
    if (data == NULL)
    {
        g_Supervisor.cfg.lifeCount = 2;
        g_Supervisor.cfg.bombCount = 3;
        g_Supervisor.cfg.colorMode16bit = 0xff;
        g_Supervisor.cfg.version = GAME_VERSION;
        g_Supervisor.cfg.padXAxis = 600;
        g_Supervisor.cfg.padYAxis = 600;
        wavFile = fopen("bgm/th06_01.wav", "rb");
        if (wavFile != NULL)
        {
            g_Supervisor.cfg.musicMode = WAV;
            fclose(wavFile);
        }
        else
        {
            g_Supervisor.cfg.musicMode = MIDI;
            utils::DebugPrint(TH_ERR_NO_WAVE_FILE);
        }
        g_Supervisor.cfg.playSounds = true;
        g_Supervisor.cfg.defaultDifficulty = NORMAL;
        g_Supervisor.cfg.windowed = false;
        g_Supervisor.cfg.frameskipConfig = 0;
        g_Supervisor.cfg.controllerMapping = g_ControllerMapping;
        g_GameErrorContext.Log(TH_ERR_CONFIG_NOT_FOUND);
    }
    else
    {
        g_Supervisor.cfg = *data;
        if ((g_Supervisor.cfg.lifeCount >= 5) || (g_Supervisor.cfg.bombCount >= 4) ||
            (g_Supervisor.cfg.colorMode16bit >= 2) || (g_Supervisor.cfg.musicMode >= 3) ||
            (g_Supervisor.cfg.defaultDifficulty >= 5) || (g_Supervisor.cfg.playSounds >= 2) ||
            (g_Supervisor.cfg.windowed >= 2) || (g_Supervisor.cfg.frameskipConfig >= 3) ||
            (g_Supervisor.cfg.version != GAME_VERSION) || (g_LastFileSize != sizeof(GameConfiguration)))
        {
            g_Supervisor.cfg.lifeCount = 2;
            g_Supervisor.cfg.bombCount = 3;
            g_Supervisor.cfg.colorMode16bit = 0xff;
            g_Supervisor.cfg.version = GAME_VERSION;
            g_Supervisor.cfg.padXAxis = 600;
            g_Supervisor.cfg.padYAxis = 600;
            wavFile2 = fopen("bgm/th06_01.wav", "rb");
            if (wavFile2 != NULL)
            {
                g_Supervisor.cfg.musicMode = WAV;
                fclose(wavFile2);
            }
            else
            {
                g_Supervisor.cfg.musicMode = MIDI;
                utils::DebugPrint(TH_ERR_NO_WAVE_FILE);
            }
            g_Supervisor.cfg.playSounds = true;
            g_Supervisor.cfg.defaultDifficulty = NORMAL;
            g_Supervisor.cfg.windowed = false;
            g_Supervisor.cfg.frameskipConfig = 0;
            g_Supervisor.cfg.controllerMapping = g_ControllerMapping;
            memset(&g_Supervisor.cfg.opts, 0, sizeof(GameConfigOpts));
            g_Supervisor.cfg.opts.useSwTextureBlending = true;
            g_GameErrorContext.Log(TH_ERR_CONFIG_CORRUPTED);
        }
        g_ControllerMapping = g_Supervisor.cfg.controllerMapping;
        ZUN_FREE(data);
    }
    if (this->IsVertexBufferDisabled())
    {
        g_GameErrorContext.Log(TH_ERR_NO_VERTEX_BUFFER);
    }
    if (this->IsFogDisabled())
    {
        g_GameErrorContext.Log(TH_ERR_NO_FOG);
    }
    if (this->Is16bitColorMode())
    {
        g_GameErrorContext.Log(TH_ERR_USE_16BIT_TEXTURES);
    }
    if (this->ShouldForceBackbufferClear())
    {
        g_GameErrorContext.Log(TH_ERR_FORCE_BACKBUFFER_CLEAR);
    }
    if (this->IsMinimumGraphicsMode())
    {
        g_GameErrorContext.Log(TH_ERR_DONT_RENDER_ITEMS);
    }
    if (this->IsShadingDisabled())
    {
        g_GameErrorContext.Log(TH_ERR_NO_GOURAUD_SHADING);
    }
    if (this->IsDepthTestDisabled())
    {
        g_GameErrorContext.Log(TH_ERR_NO_DEPTH_TESTING);
    }
    if (this->IsForced60Fps())
    {
        g_GameErrorContext.Log(TH_ERR_FORCE_60FPS_MODE);
        this->vsyncEnabled = false;
    }
    if (this->IsColorCompositingDisabled())
    {
        g_GameErrorContext.Log(TH_ERR_NO_TEXTURE_COLOR_COMPOSITING);
    }
    if (this->IsColorCompositingDisabled())
    {
        g_GameErrorContext.Log(TH_ERR_LAUNCH_WINDOWED);
    }
    if (this->IsReferenceRasterizerMode())
    {
        g_GameErrorContext.Log(TH_ERR_FORCE_REFERENCE_RASTERIZER);
    }
    if (this->IsDInputDisabled())
    {
        g_GameErrorContext.Log(TH_ERR_DO_NOT_USE_DIRECTINPUT);
    }
    if (FileSystem::WriteDataToFile(path, &g_Supervisor.cfg, sizeof(GameConfiguration)) != 0)
    {
        g_GameErrorContext.Fatal(TH_ERR_FILE_CANNOT_BE_EXPORTED, path);
        g_GameErrorContext.Fatal(TH_ERR_FOLDER_HAS_WRITE_PROTECT_OR_DISK_FULL);
        return ZUN_ERROR;
    }

    return ZUN_SUCCESS;
}
} // namespace th06
