import sys
from pathlib import Path
root = Path('.')
sys.path.insert(0, str(root / 'scripts'))
import pefile

p_target = pefile.PE(str(root / 'resources/th06.exe'), fast_load=True)
p_target.parse_data_directories()

found = False
for entry in p_target.DIRECTORY_ENTRY_IMPORT:
    if entry.dll.decode().lower() == 'kernel32.dll':
        for imp in entry.imports:
            if imp.name and imp.name.decode() == 'MapViewOfFile':
                found = True
print("MapViewOfFile in target:", found)
