import sys
from pathlib import Path
root = Path('.')
sys.path.insert(0, str(root / 'scripts'))
import pefile
import hashlib

p_target = pefile.PE(str(root / 'resources/th06.exe'), fast_load=True)
s_target = next(s for s in p_target.sections if s.Name.startswith(b'.text'))
target_data = s_target.get_data()

p_build = pefile.PE(str(root / 'build/th06.exe'), fast_load=True)
s_build = next(s for s in p_build.sections if s.Name.startswith(b'.text'))
build_data = s_build.get_data()

print(f"Target .text size: {len(target_data)}")
print(f"Build .text size:  {len(build_data)}")
if len(target_data) == len(build_data):
    print(f"Sizes match!")
    
h_target = hashlib.sha256(target_data).hexdigest()
h_build = hashlib.sha256(build_data).hexdigest()
print(f"Target hash: {h_target}")
print(f"Build hash:  {h_build}")
if h_target == h_build:
    print(f"Hashes match!")
