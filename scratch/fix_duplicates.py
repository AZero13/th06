import re

with open('src/ZunTimer.hpp', 'r') as f:
    timer = f.read()

# Remove one of the ZunTimer constructors
timer = timer.replace("""    ZunTimer()
    {
        this->Initialize();
    }""", "", 1)

with open('src/ZunTimer.hpp', 'w') as f:
    f.write(timer)

with open('src/AnmVm.hpp', 'r') as f:
    hpp = f.read()

# Remove AnmVm() from AnmVmBase
hpp = re.sub(r'\s*AnmVm\(\)\s*\{\s*this->activeSpriteIndex = -1;\s*\}', '', hpp)

with open('src/AnmVm.hpp', 'w') as f:
    f.write(hpp)
