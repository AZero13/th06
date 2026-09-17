import re

with open('src/ZunTimer.hpp', 'r') as f:
    timer = f.read()

op_eq = """
    ZunTimer& operator=(i32 time)
    {
        this->current = time;
        this->subFrame = 0.0f;
        this->previous = -999;
        return *this;
    }
    
    ZunTimer& operator+=(i32 time)
    {
        this->current += time;
        return *this;
    }
"""

timer = timer.replace('ZunBool operator==(i32 time)', op_eq + 'ZunBool operator==(i32 time)')

with open('src/ZunTimer.hpp', 'w') as f:
    f.write(timer)

