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
ZunBool Supervisor::ReadMidiFile(u32 midiFileIdx, const char *path)
{
    // Return conventions seem opposite of normal? But they're never used anyway
    if (g_Supervisor.cfg.musicMode == MIDI)
    {
        if (g_Supervisor.midiOutput != NULL)
        {
            g_Supervisor.midiOutput->ReadFileData(midiFileIdx, path);
        }

        return FALSE;
    }

    return TRUE;
}

i32 Supervisor::PlayMidiFile(i32 midiFileIdx)
{
    MidiOutput *globalMidiController;

    if (g_Supervisor.cfg.musicMode == MIDI)
    {
        if (g_Supervisor.midiOutput != NULL)
        {
            globalMidiController = g_Supervisor.midiOutput;
            globalMidiController->StopPlayback();
            globalMidiController->ParseFile(midiFileIdx);
            globalMidiController->Play();
        }

        return FALSE;
    }

    return TRUE;
}

ZunResult Supervisor::SetupMidiPlayback(const char *path)
{
    if (g_Supervisor.cfg.musicMode == MIDI)
    {
    }
    else if (g_Supervisor.cfg.musicMode == WAV)
    {
    }
    else
    {
        return ZUN_ERROR;
    }
    return ZUN_SUCCESS;
}

ZunResult Supervisor::PlayAudio(const char *path)
{
    char wavName[256];
    char wavPos[256];
    char *pathExtension;

    if (g_Supervisor.cfg.musicMode == MIDI)
    {
        if (g_Supervisor.midiOutput != NULL)
        {
            MidiOutput *midiOutput = g_Supervisor.midiOutput;
            midiOutput->StopPlayback();
            midiOutput->LoadFile(path);
            midiOutput->Play();
        }
    }
    else if (g_Supervisor.cfg.musicMode == WAV)
    {
        strcpy(wavName, path);
        strcpy(wavPos, path);
        pathExtension = strrchr(wavName, L'.');
        pathExtension[1] = 'w';
        pathExtension[2] = 'a';
        pathExtension[3] = 'v';
        pathExtension = strrchr(wavPos, L'.');
        pathExtension[1] = 'p';
        pathExtension[2] = 'o';
        pathExtension[3] = 's';
        g_SoundPlayer.LoadWav(wavName);
        if (g_SoundPlayer.LoadPos(wavPos) < ZUN_SUCCESS)
        {
            g_SoundPlayer.PlayBGM(FALSE);
        }
        else
        {
            g_SoundPlayer.PlayBGM(TRUE);
        }
    }
    else
    {
        return ZUN_ERROR;
    }
    return ZUN_SUCCESS;
}

ZunResult Supervisor::StopAudio()
{
    if (g_Supervisor.cfg.musicMode == MIDI)
    {
        if (g_Supervisor.midiOutput != NULL)
        {
            g_Supervisor.midiOutput->StopPlayback();
        }
    }
    else
    {
        if (g_Supervisor.cfg.musicMode == WAV)
        {
            g_SoundPlayer.StopBGM();
        }
        else
        {
            return ZUN_ERROR;
        }
    }

    return ZUN_SUCCESS;
}

ZunResult Supervisor::FadeOutMusic(f32 fadeOutSeconds)
{
    if (g_Supervisor.cfg.musicMode == MIDI)
    {
        if (g_Supervisor.midiOutput != NULL)
        {
            g_Supervisor.midiOutput->SetFadeOut(1000.0f * fadeOutSeconds);
        }
    }
    else
    {
        if (g_Supervisor.cfg.musicMode == WAV)
        {
            if (this->effectiveFramerateMultiplier == 0.0f)
            {
                g_SoundPlayer.FadeOut(fadeOutSeconds);
            }
            else
            {
                if (this->effectiveFramerateMultiplier > 1.0f)
                {
                    g_SoundPlayer.FadeOut(fadeOutSeconds);
                }
                else
                {
                    g_SoundPlayer.FadeOut(fadeOutSeconds / this->effectiveFramerateMultiplier);
                }
            }
        }
        else
        {
            return ZUN_ERROR;
        }
    }

    return ZUN_SUCCESS;
}
} // namespace th06
