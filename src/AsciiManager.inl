#pragma once

inline void AsciiManager::InitializeVms()
{
    memset(this, 0, sizeof(AsciiManager));

    this->color = COLOR_WHITE;
    this->scale.x = 1.0f;
    this->scale.y = 1.0f;

    this->vm1.flags.anchor = AnmVmAnchor_TopLeft;

    g_AnmManager->InitializeAndSetSprite(&this->vm1, 0);
    g_AnmManager->InitializeAndSetSprite(&this->vm0, 32);

    this->vm1.pos.z = 0.1f;
    this->isSelected = false;
}
