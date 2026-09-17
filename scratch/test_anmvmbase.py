import re

with open('src/AnmVm.hpp', 'r') as f:
    hpp = f.read()

# Make sure AnmVmBase has a constructor calling Initialize
hpp = re.sub(r'struct AnmVmBase\s*\{(?:\s*AnmVmBase\(\)\s*\{\s*\})?', """struct AnmVmBase
{
    AnmVmBase()
    {
        this->Initialize();
    }""", hpp)

with open('src/AnmVm.hpp', 'w') as f:
    f.write(hpp)

with open('src/ZunTimer.hpp', 'r') as f:
    timer_hpp = f.read()

# Undo friend operators
timer_hpp = re.sub(r'\s*ZunBool operator==\(i32 time\)\s*\{\s*return this->current == time;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*ZunBool operator>=\(i32 time\)\s*\{\s*return this->current >= time;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*ZunBool operator>\(i32 time\)\s*\{\s*return this->current > time;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*ZunBool operator<\(i32 time\)\s*\{\s*return this->current < time;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*ZunBool operator<=\(i32 time\)\s*\{\s*return this->current <= time;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*ZunBool operator!=\(i32 time\)\s*\{\s*return this->current != time;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*friend ZunBool operator==\(i32 time, const ZunTimer& timer\)\s*\{\s*return time == timer\.current;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*friend ZunBool operator>=\(i32 time, const ZunTimer& timer\)\s*\{\s*return time >= timer\.current;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*friend ZunBool operator>\(i32 time, const ZunTimer& timer\)\s*\{\s*return time > timer\.current;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*friend ZunBool operator<\(i32 time, const ZunTimer& timer\)\s*\{\s*return time < timer\.current;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*friend ZunBool operator<=\(i32 time, const ZunTimer& timer\)\s*\{\s*return time <= timer\.current;\s*\}', '', timer_hpp)
timer_hpp = re.sub(r'\s*friend ZunBool operator!=\(i32 time, const ZunTimer& timer\)\s*\{\s*return time != timer\.current;\s*\}', '', timer_hpp)

with open('src/ZunTimer.hpp', 'w') as f:
    f.write(timer_hpp)
