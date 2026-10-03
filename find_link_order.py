import sys
from pathlib import Path
root = Path('.')
sys.path.insert(0, str(root / 'scripts'))
import pefile

p_build = pefile.PE(str(root / 'build/th06.exe'), fast_load=True)
p_target = pefile.PE(str(root / 'resources/th06.exe'), fast_load=True)

# Get target .text
s_target = next(s for s in p_target.sections if s.Name.startswith(b'.text'))
target_data = s_target.get_data()
target_base = p_target.OPTIONAL_HEADER.ImageBase + s_target.VirtualAddress

# Parse build map to get one function per obj
obj_funcs = {}
with open('build/th06.map', 'r') as f:
    in_publics = False
    for line in f:
        if 'Publics by Value' in line:
            in_publics = True
            continue
        if in_publics and line.strip() == '':
            continue
        if in_publics:
            parts = line.split()
            if len(parts) >= 4:
                addr = int(parts[0].split(':')[1], 16) + p_build.OPTIONAL_HEADER.ImageBase + 0x1000
                sym = parts[1]
                obj = parts[-1]
                if ':' in obj: obj = obj.split(':')[1]
                
                # Exclude library objs
                if not obj.endswith('.obj') or obj in ['libcpmt.obj', 'LIBCMT.obj', 'OLDNAMES.obj', 'uuid.obj']:
                    continue
                    
                if obj not in obj_funcs:
                    # try to find a nice big function
                    obj_funcs[obj] = []
                obj_funcs[obj].append((sym, addr))

# For each obj, we need its target address
obj_target_addrs = {}

# We'll just look at the map file from BEFORE the split (header_inline.map or something) or just use the current build
# But wait, we can't easily find the functions in the target by bytes unless we use the exact bytes.
# Since we just want the obj file order, let's just use the `ghidra_ns_to_obj.csv` or similar mapping!
