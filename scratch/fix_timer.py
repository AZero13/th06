import re

with open('src/ZunTimer.hpp', 'r') as f:
    code = f.read()

# Nuke SetCurrent and InitializeForPopup
code = re.sub(r'\s*void SetCurrent\(i32 value\)\s*\{[^}]*\}', '', code)
code = re.sub(r'\s*void InitializeForPopup\(\)\s*\{[^}]*\}', '', code)

# Update Tick() to return i32
code = code.replace("void Tick()", "i32 Tick()")
code = code.replace("g_Supervisor.TickTimer(&this->current, &this->subFrame);", "g_Supervisor.TickTimer(&this->current, &this->subFrame);\n        return this->current;")

# Update operator= to include SetCurrent's body
code = code.replace("""    void operator=(i32 value)
    {
        this->SetCurrent(value);
    }""", """    void operator=(i32 value)
    {
        this->current = value;
        this->subFrame = 0.0f;
        this->previous = -999;
    }""")

# Update operator++ to return i32
code = code.replace("""    void operator++(int)
    {
        this->Tick();
    }""", """    i32 operator++(int)
    {
        return this->Tick();
    }""")

# Add friend comparison operators
friend_ops = """
    friend ZunBool operator==(i32 time, ZunTimer& timer)
    {
        return time == timer.current;
    }
    friend ZunBool operator!=(i32 time, ZunTimer& timer)
    {
        return time != timer.current;
    }
    friend ZunBool operator<(i32 time, ZunTimer& timer)
    {
        return time < timer.current;
    }
    friend ZunBool operator<=(i32 time, ZunTimer& timer)
    {
        return time <= timer.current;
    }
    friend ZunBool operator>(i32 time, ZunTimer& timer)
    {
        return time > timer.current;
    }
    friend ZunBool operator>=(i32 time, ZunTimer& timer)
    {
        return time >= timer.current;
    }
"""

code = code.replace("    void Initialize();", friend_ops + "\n    void Initialize();")

with open('src/ZunTimer.hpp', 'w') as f:
    f.write(code)
