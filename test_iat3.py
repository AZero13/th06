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

print("KERNEL32 diff:")
t_set = set(t_iat['kernel32.dll'])
b_set = set(b_iat['kernel32.dll'])
print("Extra in build:", b_set - t_set)
print("Missing in build:", t_set - b_set)
