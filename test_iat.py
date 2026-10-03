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

for dll in t_iat:
    if dll in b_iat:
        t_list = t_iat[dll]
        b_list = b_iat[dll]
        if t_list == b_list:
            print(f"{dll}: Match! ({len(t_list)} imports)")
        else:
            print(f"{dll}: Mismatch!")
            diff = sum(1 for i, (t, b) in enumerate(zip(t_list, b_list)) if t != b)
            if len(t_list) != len(b_list):
                print(f"  Length difference: Target={len(t_list)}, Build={len(b_list)}")
            else:
                print(f"  Slot differences: {diff}")
    else:
        print(f"{dll}: Missing in build!")
