# Somewhat bafflingly, link.exe does not provide a (documented) way to
# override the PE header timestamp. So this script does exactly that.

import sys

exe_path = sys.argv[1]
timestamp_value = int(sys.argv[2])

exe = open(exe_path, "r+b")
# Offset for pointer to PE header
exe.seek(0x3c, 0)
pe_offset = int.from_bytes(exe.read(4), byteorder='little')
# TimeDataStamp is +0x8 from base of PE header
timestamp_offset = pe_offset + 0x8
exe.seek(timestamp_offset, 0)
exe.write(timestamp_value.to_bytes(4, byteorder='little'))
exe.close();
