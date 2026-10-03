import sys
from pathlib import Path
root = Path('.')
sys.path.insert(0, str(root / 'scripts'))
import pefile

p_target = pefile.PE(str(root / 'resources/th06.exe'), fast_load=True)
p_target.parse_data_directories()
p_build = pefile.PE(str(root / 'build/th06.exe'), fast_load=True)
p_build.parse_data_directories()

def get_iat(p):
    iat = {}
    for entry in p.DIRECTORY_ENTRY_IMPORT:
        dll_name = entry.dll.decode().lower()
        imports = []
        for imp in entry.imports:
            if imp.name:
                imports.append(imp.name.decode())
        iat[dll_name] = imports
    return iat

t_iat = get_iat(p_target)
b_iat = get_iat(p_build)

print("WINMM diff:")
for t, b in zip(t_iat['winmm.dll'], b_iat['winmm.dll']):
    if t != b:
        print(f"Target: {t} | Build: {b}")
