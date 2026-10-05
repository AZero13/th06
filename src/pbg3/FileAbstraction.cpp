#include "pbg3/FileAbstraction.hpp"

namespace th06
{
FileAbstraction::FileAbstraction()
{
    this->handle = INVALID_HANDLE_VALUE;
    this->access = 0;
}

FileAbstraction::~FileAbstraction()
{
    this->Close();
}

// DUMMY FUNCTIONS FOR IAT
struct MappedFileView
{
    HANDLE file;
    HANDLE mapping;
    void *data;
    DWORD size;
    BOOL writable;
};
BOOL CloseMappedFileView(MappedFileView *view)
{
    FlushViewOfFile(view->data, 0);
    UnmapViewOfFile(view->data);
    CloseHandle(view->mapping);
    CloseHandle(view->file);
    return TRUE;
}
BOOL OpenMappedFileView(const WCHAR *filename, BOOL writable, MappedFileView *view)
{
    GetFileAttributesW(filename);
    CreateFileW(filename, 0, 0, NULL, 0, 0, NULL);
    GetFileSize(view->file, NULL);
    CreateFileMappingA(view->file, NULL, 0, 0, 0, NULL);
    MapViewOfFile(view->mapping, 0, 0, 0, 0);
    return TRUE;
}
BOOL Exists_Dummy(const char *filename)
{
    GetFileAttributesA(filename);
    return TRUE;
}

// END DUMMY FUNCTIONS
BOOL FileAbstraction::Open(const char *filename, const char *mode)
{
    const char *curMode;
    BOOL isAppendMode = FALSE;
    u32 creationDisposition;

    this->Close();

    for (curMode = mode; *curMode != '\0'; curMode++)
    {
        if (*curMode == 'r')
        {
            this->access = GENERIC_READ;
            creationDisposition = OPEN_EXISTING;
            break;
        }
        else if (*curMode == 'w')
        {
            DeleteFile(filename);
            this->access = GENERIC_WRITE;
            creationDisposition = OPEN_ALWAYS;
            break;
        }
        else if (*curMode == 'a')
        {
            isAppendMode = TRUE;
            this->access = GENERIC_WRITE;
            creationDisposition = OPEN_ALWAYS;
            break;
        }
    }

    if (*curMode == '\0')
        return FALSE;

    this->handle = CreateFile(filename, this->access, FILE_SHARE_READ, NULL, creationDisposition,
                              FILE_ATTRIBUTE_NORMAL | FILE_FLAG_SEQUENTIAL_SCAN, NULL);

    if (INVALID_HANDLE_VALUE == this->handle)
        return FALSE;

    if (isAppendMode)
        this->Seek(0, FILE_END);

    return TRUE;
}

void FileAbstraction::Close()
{
    if (this->handle != INVALID_HANDLE_VALUE)
    {
        CloseHandle(this->handle);
        this->handle = INVALID_HANDLE_VALUE;
        this->access = 0;
    }
}

BOOL FileAbstraction::Read(void *data, u32 dataLen, DWORD *numBytesRead)
{
    if (GENERIC_READ != this->access)
        return FALSE;

    return ReadFile(this->handle, data, dataLen, numBytesRead, NULL);
}

BOOL FileAbstraction::Write(void *data, u32 dataLen, DWORD *outWritten)
{
    if (GENERIC_WRITE != this->access)
        return FALSE;

    return WriteFile(this->handle, data, dataLen, outWritten, NULL);
}

i32 FileAbstraction::ReadByte()
{
    u8 data;
    DWORD outBytesRead;

    if (FALSE == this->Read(&data, 1, &outBytesRead))
        return PBG_EOF;
    if (outBytesRead == 0)
        return PBG_EOF;
    else
        return data;
}

i32 FileAbstraction::WriteByte(i32 b)
{
    u8 outByte;
    DWORD outBytesWritten;

    outByte = b;
    if (FALSE == this->Write(&outByte, 1, &outBytesWritten))
        return PBG_EOF;
    if (outBytesWritten == 0)
        return PBG_EOF;
    else
        return b;
}

BOOL FileAbstraction::Seek(u32 amount, u32 seekFrom)
{
    if (INVALID_HANDLE_VALUE == this->handle)
        return FALSE;

    SetFilePointer(this->handle, amount, NULL, seekFrom);
    return TRUE;
}

u32 FileAbstraction::Tell()
{
    if (INVALID_HANDLE_VALUE == this->handle)
        return 0;

    return SetFilePointer(this->handle, 0, NULL, FILE_CURRENT);
}

u32 FileAbstraction::GetSize()
{
    if (INVALID_HANDLE_VALUE == this->handle)
        return 0;

    return GetFileSize(this->handle, NULL);
}

BOOL FileAbstraction::WriteString(void *buffer)
{
    DWORD Length;
    DWORD temp;

    if (GENERIC_WRITE != this->access)
        return FALSE;

    Length = strlen((char *)buffer);
    return this->Write(buffer, Length, &temp);
}

LPVOID FileAbstraction::ReadWholeFile(u32 maxSize)
{
    DWORD oldLocation, dataLen, outDataLen;
    LPVOID data;

    if (GENERIC_READ != this->access)
        return NULL;

    dataLen = this->GetSize();
    if (dataLen > maxSize)
        return NULL;

    data = (LPVOID)LocalAlloc(LPTR, dataLen);
    if (NULL == data)
        return NULL;

    oldLocation = this->Tell();

    // Pretty sure the plan here was to seek to 0, but woops the code
    // is buggy. And yes, this case leaks the data. Amazing, I know.
    if (FALSE == this->Seek(oldLocation, FILE_BEGIN))
        return NULL;

    if (FALSE == this->Read(data, dataLen, &outDataLen))
    {
        LocalFree(data);
        return NULL;
    }

    this->Seek(oldLocation, FILE_BEGIN);

    return data;
}

} // namespace th06
