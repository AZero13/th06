import os
import re

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.cpp') or file.endswith('.hpp'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            new_content = content.replace('FakePaddedAnmVm', 'AnmVm')
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)

with open('src/AnmVm.hpp', 'r') as f:
    hpp = f.read()

hpp = hpp.replace("""    AnmVm();""", """    AnmVm()
    {
        this->activeSpriteIndex = -1;
    }""")

hpp = re.sub(r'struct AnmVm : AnmVm\s*\{\s*AnmVm\(\)\s*\{\s*FAKE_INLINE_DWORD_STACK_PADDING<4>\(\);\s*\}\s*\};\s*', '', hpp)

with open('src/AnmVm.hpp', 'w') as f:
    f.write(hpp)

with open('src/AnmManager.cpp', 'r') as f:
    cpp = f.read()

cpp = re.sub(r'AnmVm::AnmVm\(\)\s*\{\s*this->activeSpriteIndex = -1;\s*\}\s*', '', cpp)

with open('src/AnmManager.cpp', 'w') as f:
    f.write(cpp)
