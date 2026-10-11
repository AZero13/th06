# Somewhat bafflingly, link.exe does not provide a (documented) way to
# override the PE header timestamp. So this script does exactly that.

import sys

def patch_timestamp(exe_path, timestamp_value):
    with open(exe_path, "r+b") as exe:
        # Offset for pointer to PE header.
        exe.seek(0x3C)
        pe_offset = int.from_bytes(exe.read(4), byteorder="little")
        exe.seek(pe_offset)
        if exe.read(4) != b"PE\0\0":
            raise ValueError("Not a PE executable: " + str(exe_path))
        # TimeDateStamp is +0x8 from the base of the PE header.
        exe.seek(pe_offset + 0x8)
        exe.write(timestamp_value.to_bytes(4, byteorder="little"))


if __name__ == "__main__":
    patch_timestamp(sys.argv[1], int(sys.argv[2]))
