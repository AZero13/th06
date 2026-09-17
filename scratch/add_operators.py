with open('src/ZunTimer.hpp', 'r') as f:
    content = f.read()

replacement = """    void Initialize();
    void Increment(i32 value);
    void Decrement(i32 value);
    i32 NextTick();

    void operator+=(i32 value)
    {
        this->Increment(value);
    }
    void operator-=(i32 value)
    {
        this->Decrement(value);
    }
    void operator++(int)
    {
        this->Tick();
    }
    void operator--(int)
    {
        this->Decrement(1);
    }

    void IncrementInline(i32 value)
    {
        this->Increment(value);
    }

    void InitializeForPopup()
    {
        this->current = 0;
        this->subFrame = 0;
        this->previous = -999;
    }

    void SetCurrent(i32 value)
    {
        this->current = value;
        this->subFrame = 0;
        this->previous = -999;
    }

    void operator=(i32 value)
    {
        this->SetCurrent(value);
    }

    void Tick()
    {
        this->previous = this->current;
        g_Supervisor.TickTimer(&this->current, &this->subFrame);
    }"""

content = content.replace('    void Initialize();\n    void Increment(i32 value);\n    void Decrement(i32 value);\n    i32 NextTick();\n\n    void IncrementInline(i32 value)\n    {\n        this->Increment(value);\n    }\n\n    void InitializeForPopup()\n    {\n        this->current = 0;\n        this->subFrame = 0;\n        this->previous = -999;\n    }\n\n    void SetCurrent(i32 value)\n    {\n        this->current = value;\n        this->subFrame = 0;\n        this->previous = -999;\n    }\n\n    void Tick()\n    {\n        this->previous = this->current;\n        g_Supervisor.TickTimer(&this->current, &this->subFrame);\n    }', replacement)

with open('src/ZunTimer.hpp', 'w') as f:
    f.write(content)
