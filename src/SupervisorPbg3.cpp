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
void Supervisor::ReleasePbg3(i32 pbg3FileIdx)
{
    if (this->pbg3Archives[pbg3FileIdx] == NULL)
    {
        return;
    }

    // Double free! Release is called internally by the Pbg3Archive destructor,
    // and as such should not be called directly. By calling it directly here,
    // it ends up being called twice, which will cause the resources owned by
    // Pbg3Archive to be freed multiple times, which can result in crashes.
    //
    // For some reason, this double-free doesn't cause crashes in the original
    // game. However, this can cause problems in dllbuilds of the game. Maybe
    // some accuracy improvements in the PBG3 handling will remove this
    // difference.
    this->pbg3Archives[pbg3FileIdx]->Release();
    ZUN_DELETE(this->pbg3Archives[pbg3FileIdx]);
}

i32 Supervisor::LoadPbg3(i32 pbg3FileIdx, const char *filename)
{
    if (this->pbg3Archives[pbg3FileIdx] == NULL || strcmp(filename, this->pbg3ArchiveNames[pbg3FileIdx]) != 0)
    {
        this->ReleasePbg3(pbg3FileIdx);
        this->pbg3Archives[pbg3FileIdx] = ZUN_NEW(Pbg3Archive);
        utils::DebugPrint("%s open ...\n", filename);
        if (this->pbg3Archives[pbg3FileIdx]->Load(filename) != 0)
        {
            strcpy(this->pbg3ArchiveNames[pbg3FileIdx], filename);

            char verPath[128];
            sprintf(verPath, "ver%.4x.dat", GAME_VERSION);
            i32 res = this->pbg3Archives[pbg3FileIdx]->FindEntry(verPath);
            if (res < 0)
            {
                g_GameErrorContext.Fatal(TH_ERR_WRONG_DATA_VERSION);
                return 1;
            }
        }
        else
        {
            // Let's really make sure this is null by nulling twice. I assume
            // there's some kind of inline function here, like it's actually
            // calling this->pbg3Archives.delete(pbg3FileIdx), followed by a
            // manual nulling?
            ZUN_DELETE(this->pbg3Archives[pbg3FileIdx]);
            this->pbg3Archives[pbg3FileIdx] = NULL;
        }
    }
    return 0;
}
} // namespace th06
