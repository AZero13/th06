#pragma once

#include "Supervisor.hpp"
#include "inttypes.hpp"
#include <Windows.h>

namespace th06
{
struct ZunTimer
{
    i32 previous;
    f32 subFrame;
    i32 current;

    ZunTimer()
    {
        this->Initialize();
    }

    ZunBool operator==(i32 time)
    {
        return this->current == time;
    }

    ZunBool operator>=(i32 time)
    {
        return this->current >= time;
    }

    ZunBool operator>(i32 time)
    {
        return this->current > time;
    }

    ZunBool operator<(i32 time)
    {
        return this->current < time;
    }

    ZunBool operator<=(i32 time)
    {
        return this->current <= time;
    }

    void Initialize()
    {
        this->current = 0;
        this->previous = -1;
        this->subFrame = 0;
    }
    void Increment(i32 value)
    {
        if (g_Supervisor.framerateMultiplier > 0.99f)
        {
            this->current = this->current + value;

            return;
        }

        if (value < 0)
        {
            Decrement(-value);

            return;
        }

        this->previous = this->current;
        this->subFrame = g_Supervisor.effectiveFramerateMultiplier * (float)value + this->subFrame;

        while (this->subFrame >= 1.0f)
        {
            this->current++;
            this->subFrame = this->subFrame - 1.0f;
        }
    }
    void Decrement(i32 value)
    {
        if (g_Supervisor.framerateMultiplier > 0.99f)
        {
            this->current = this->current - value;

            return;
        }

        if (value < 0)
        {
            Increment(-value);

            return;
        }

        this->previous = this->current;
        this->subFrame = this->subFrame - g_Supervisor.effectiveFramerateMultiplier * (float)value;

        while (this->subFrame < 0.0f)
        {
            this->current--;
            this->subFrame = this->subFrame + 1.0f;
        }
    }
    i32 NextTick()
    {
        this->Tick();
        return this->current;
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

    void Tick()
    {
        this->previous = this->current;
        g_Supervisor.TickTimer(&this->current, &this->subFrame);
    }

    f32 AsFramesFloat()
    {
        return this->current + this->subFrame;
    }

    i32 AsFrames()
    {
        return this->current;
    }

    ZunBool HasTicked()
    {
        return this->current != this->previous;
    }
};
ZUN_ASSERT_SIZE(ZunTimer, 0xc);
}; // namespace th06
