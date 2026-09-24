#pragma once

#include "inttypes.hpp"
#include "pbg3/FileAbstraction.hpp"
#include "pbg3/IPbg3Parser.hpp"

namespace th06
{
class Pbg3Parser : public IPbg3Parser, public FileAbstraction
{
  public:
    Pbg3Parser();
    i32 OpenArchive(const char *path);
    void Close();
    virtual i32 ReadBit();
    virtual u32 ReadInt(u32 numBitsAsPowersOf2);
    virtual i32 ReadByte();
    virtual i32 SeekToOffset(u32 fileOffset);
    virtual i32 SeekToNextByte();
    virtual i32 ReadByteAlignedData(u8 *data, u32 bytesToRead);
    virtual i32 GetLastWriteTime(LPFILETIME lastWriteTime);

    ~Pbg3Parser();
};
ZUN_ASSERT_SIZE(Pbg3Parser, 0x24);
}; // namespace th06
