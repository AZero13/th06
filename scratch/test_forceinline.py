import re

with open('src/AnmVm.hpp', 'r') as f:
    hpp = f.read()

# Add __forceinline constructor calling Initialize to AnmVm
hpp = re.sub(r'struct AnmVm\s*:\s*public\s*AnmVmBase\s*\{\s*(?:AnmVm\(\)\s*\{[^}]*\}\s*)?\}', """struct AnmVm : public AnmVmBase
{
    __forceinline AnmVm()
    {
        this->Initialize();
    }
}""", hpp)

with open('src/AnmVm.hpp', 'w') as f:
    f.write(hpp)

with open('src/AnmManager.cpp', 'r') as f:
    cpp = f.read()

cpp = re.sub(r'AnmVm::AnmVm\(\)\s*\{[^}]*\}\s*', '', cpp)

with open('src/AnmManager.cpp', 'w') as f:
    f.write(cpp)
