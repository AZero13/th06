#include "th06.hpp"
#include "Global.hpp"
#include "GameWindow.hpp"

namespace th06
{
DIFFABLE_STATIC_SORTED(I4, Pbg3Archive **, g_Pbg3Archives);

#pragma var_order(pbg3Idx, entryname, entryIdx, fsize, data, file)
u8 *FileSystem::OpenPath(const char *filepath, ZunBool isExternalResource)
{
    u8 *data;
    FILE *file;
    size_t fsize;
    i32 entryIdx;
    const char *entryname;
    i32 pbg3Idx;

    entryIdx = -1;
    if (!isExternalResource)
    {
        entryname = strrchr(filepath, '\\');
        if (entryname == NULL)
        {
            entryname = filepath;
        }
        else
        {
            entryname++;
        }
        entryname = strrchr(entryname, '/');
        if (entryname == NULL)
        {
            entryname = filepath;
        }
        else
        {
            entryname++;
        }
        if (g_Pbg3Archives != NULL)
        {
            for (pbg3Idx = 0; pbg3Idx < 16; pbg3Idx++)
            {
                if (g_Pbg3Archives[pbg3Idx] != NULL)
                {
                    entryIdx = g_Pbg3Archives[pbg3Idx]->FindEntry(entryname);
                    if (entryIdx >= 0)
                    {
                        break;
                    }
                }
            }
        }
        if (entryIdx < 0)
        {
            return NULL;
        }
    }
    if (entryIdx >= 0)
    {
        utils::DebugPrint2("%s Decode ... \n", entryname);
        data = g_Pbg3Archives[pbg3Idx]->ReadDecompressEntry(entryIdx, entryname);
        g_LastFileSize = g_Pbg3Archives[pbg3Idx]->GetEntrySize(entryIdx);
    }
    else
    {
        utils::DebugPrint2("%s Load ... \n", filepath);
        file = fopen(filepath, "rb");
        if (file == NULL)
        {
            utils::DebugPrint2("error : %s is not found.\n", filepath);
            return NULL;
        }
        else
        {
            fseek(file, 0, SEEK_END);
            fsize = ftell(file);
            g_LastFileSize = fsize;
            fseek(file, 0, SEEK_SET);
            data = ZUN_ALLOC(fsize);
            fread(data, 1, fsize, file);
            fclose(file);
        }
    }
    return data;
}

int FileSystem::WriteDataToFile(const char *path, const void *data, size_t size)
{
    FILE *f;

    f = fopen(path, "wb");
    if (f == NULL)
    {
        return -1;
    }
    else
    {
        if (fwrite(data, 1, size, f) != size)
        {
            fclose(f);
            return -2;
        }
        else
        {
            fclose(f);
            return 0;
        }
    }
}
}
