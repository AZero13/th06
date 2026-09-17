import re

with open('src/ZunTimer.hpp', 'r') as f:
    timer = f.read()

op_eq = """
    ZunTimer& operator++(int)
    {
        this->current++;
        return *this;
    }
    
    ZunTimer& operator--(int)
    {
        this->current--;
        return *this;
    }
"""

timer = timer.replace('ZunTimer& operator=(i32 time)', op_eq + 'ZunTimer& operator=(i32 time)')

with open('src/ZunTimer.hpp', 'w') as f:
    f.write(timer)

