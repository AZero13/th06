#include "BombData.hpp"

#include "EffectManager.hpp"
#include "Global.hpp"
#include "Gui.hpp"
#include "ScreenEffect.hpp"
#include "i18n.hpp"

namespace th06
{
#pragma var_order(angle, i, bombSprite, vecLength, bombPivot, bombIdx)
void BombData::BombReimuACalc(Player *player)
{
    i32 i;
    f32 vecLength;
    i32 bombIdx;
    D3DXVECTOR3 bombPivot;
    AnmVm *bombSprite;
    ZunVec2 angle;

    if (player->bombInfo.timer >= player->bombInfo.duration)
    {
        g_Gui.EndPlayerSpellcard();
        player->bombInfo.isInUse = false;
        return;
    }
    if (player->bombInfo.timer.HasTicked() && player->bombInfo.timer == 0)
    {
        g_Gui.ShowBombNamePortrait(ANM_SCRIPT_FACE_BOMB_PORTRAIT, TH_REIMU_A_BOMB_NAME);
        player->bombInfo.duration = 300;
        player->invulnerabilityTimer = 360;

        for (i = 0; i < 8; i++)
        {
            player->bombInfo.reimuABombProjectilesState[i] = 0;
        }
        g_ItemManager.RemoveAllItems();
        g_EffectManager.SpawnParticles(PARTICLE_EFFECT_UNK_12, &player->positionCenter, 1, COLOR_NEONBLUE);

        player->bombProjectiles[8].posX = (player->positionCenter).x;
        player->bombProjectiles[8].posY = (player->positionCenter).y;

        player->bombProjectiles[8].sizeX = 256.0f;
        player->bombProjectiles[8].sizeY = 256.0f;
    }
    if (player->bombInfo.timer >= 60 && player->bombInfo.timer < 180)
    {

        if (player->bombInfo.timer % 16 == 0 && (i = (player->bombInfo.timer - 60) / 16))
        {
            player->bombInfo.reimuABombProjectilesState[i] = 1;
            player->bombInfo.reimuABombProjectilesRelated[i] = 4.0f;
            player->bombInfo.bombRegionPositions[i] = player->positionCenter;

            angle.x = g_Rng.GetRandomF32ZeroToOne() * ZUN_2PI - ZUN_PI;

            player->bombInfo.bombRegionVelocities[i].x =
                cosf(angle.x) * player->bombInfo.reimuABombProjectilesRelated[i];

            player->bombInfo.bombRegionVelocities[i].y =
                sinf(angle.x) * player->bombInfo.reimuABombProjectilesRelated[i];
            player->unk_838[i] = 0;

            for (bombSprite = &player->bombInfo.sprites[0][i * 4], bombIdx = 0; bombIdx < 4; bombIdx++, bombSprite++)
            {
                g_AnmManager->ExecuteAnmIdx(bombSprite, ANM_SCRIPT_PLAYER_REIMU_A_BOMB_ARRAY + bombIdx);
            }
            g_SoundPlayer.PlaySoundByIdx(SOUND_BOMB_REIMU_A);
        }
    }
    player->playerState = PLAYER_STATE_INVULNERABLE;
    for (i = 0; i < ARRAY_SIZE_SIGNED(player->bombInfo.reimuABombProjectilesState); i++)
    {
        if (player->bombInfo.reimuABombProjectilesState[i] == 0)
        {
            continue;
        }
        if (player->bombInfo.reimuABombProjectilesState[i] == 1)
        {
            if (player->bombInfo.timer.HasTicked())
            {
                if (player->positionOfLastEnemyHit.x > -100.0f)
                {
                    bombPivot = player->positionOfLastEnemyHit;
                }
                else
                {
                    bombPivot = player->positionCenter;
                }
                angle.x = bombPivot.x - player->bombInfo.bombRegionPositions[i].x;
                angle.y = bombPivot.y - player->bombInfo.bombRegionPositions[i].y;

                vecLength = sqrtf(angle.x * angle.x + angle.y * angle.y) /
                            (player->bombInfo.reimuABombProjectilesRelated[i] / 8.0f);
                if (vecLength < 1.0f)
                {
                    vecLength = 1.0f;
                }
                angle.x = angle.x / vecLength + player->bombInfo.bombRegionVelocities[i].x;
                angle.y = angle.y / vecLength + player->bombInfo.bombRegionVelocities[i].y;
                vecLength = sqrtf(angle.x * angle.x + angle.y * angle.y);

                player->bombInfo.reimuABombProjectilesRelated[i] = ZUN_MIN(vecLength, 10.0f);

                if (player->bombInfo.reimuABombProjectilesRelated[i] < 1.0f)
                {
                    player->bombInfo.reimuABombProjectilesRelated[i] = 1.0f;
                }

                player->bombInfo.bombRegionVelocities[i].x =
                    (angle.x * player->bombInfo.reimuABombProjectilesRelated[i]) / vecLength;
                player->bombInfo.bombRegionVelocities[i].y =
                    (angle.y * player->bombInfo.reimuABombProjectilesRelated[i]) / vecLength;

                player->bombRegionSizes[i].x = 48.0f;
                player->bombRegionSizes[i].y = 48.0f;

                player->bombRegionPositions[i] = player->bombInfo.bombRegionPositions[i];
                player->bombRegionDamages[i] = 8;

                player->bombProjectiles[i].posX = player->bombInfo.bombRegionPositions[i].x;
                player->bombProjectiles[i].posY = player->bombInfo.bombRegionPositions[i].y;

                player->bombProjectiles[i].sizeX = 48.0f;
                player->bombProjectiles[i].sizeY = 48.0f;

                if (player->unk_838[i] >= 100 || player->bombInfo.timer >= player->bombInfo.duration - 30)
                {
                    g_EffectManager.SpawnParticles(PARTICLE_EFFECT_UNK_6, &player->bombInfo.bombRegionPositions[i], 8,
                                                   COLOR_WHITE);
                    g_EffectManager.SpawnParticles(PARTICLE_EFFECT_UNK_12, &player->bombInfo.bombRegionPositions[i], 1,
                                                   COLOR_NEONBLUE);
                    player->bombInfo.reimuABombProjectilesState[i] = 2;

                    player->bombInfo.sprites[0][i * 4].pendingInterrupt = 1;
                    player->bombInfo.sprites[0][i * 4 + 1].pendingInterrupt = 1;
                    player->bombInfo.sprites[0][i * 4 + 2].pendingInterrupt = 1;
                    player->bombInfo.sprites[0][i * 4 + 3].pendingInterrupt = 1;

                    player->bombRegionSizes[i].x = 256.0f;
                    player->bombRegionSizes[i].y = 256.0f;

                    player->bombRegionDamages[i] = 200;

                    player->bombProjectiles[i].sizeX = 256.0f;
                    player->bombProjectiles[i].sizeY = 256.0f;

                    player->bombInfo.bombRegionVelocities[i] / 8.0f; // ZUN moment

                    g_SoundPlayer.PlaySoundByIdx(SOUND_F);
                    ScreenEffect::RegisterChain(SCREEN_EFFECT_SHAKE, 16, 8, 0, 0);
                }
            }
        }
        else if (player->bombInfo.reimuABombProjectilesState[i] != 0 && player->bombInfo.timer.HasTicked())
        {
            player->bombInfo.reimuABombProjectilesState[i]++;
            if (player->bombInfo.reimuABombProjectilesState[i] >= 30)
            {
                player->bombInfo.reimuABombProjectilesState[i] = 0;
            }
        }
        player->bombInfo.bombRegionPositions[i].x +=
            g_Supervisor.effectiveFramerateMultiplier * player->bombInfo.bombRegionVelocities[i].x;
        player->bombInfo.bombRegionPositions[i].y +=
            g_Supervisor.effectiveFramerateMultiplier * player->bombInfo.bombRegionVelocities[i].y;

        g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][i * 4]);
        g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][i * 4 + 1]);
        g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][i * 4 + 2]);
        g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][i * 4 + 3]);
    }
    player->bombInfo.timer++;
}

#pragma var_order(bombSprite, idx)
void BombData::BombReimuADraw(Player *player)
{
    i32 idx;
    AnmVm *bombSprite;

    BombData::DarkenViewport(player);
    bombSprite = &player->bombInfo.sprites[0][0];
    for (idx = 0; idx < ARRAY_SIZE_SIGNED(player->bombInfo.sprites); idx++)
    {
        if (player->bombInfo.reimuABombProjectilesState[idx] == 0)
        {
            bombSprite = &bombSprite[4];
            continue;
        }

        bombSprite->pos = player->bombInfo.bombRegionPositions[idx] + bombSprite->posOffset;
        player->SetToTopLeftPos(bombSprite);
        g_AnmManager->DrawNoRotation(bombSprite);
        bombSprite++;

        bombSprite->pos = player->bombInfo.bombRegionPositions[idx] + bombSprite->posOffset;
        player->SetToTopLeftPos(bombSprite);
        g_AnmManager->DrawNoRotation(bombSprite);
        bombSprite++;

        bombSprite->pos = player->bombInfo.bombRegionPositions[idx] + bombSprite->posOffset;
        player->SetToTopLeftPos(bombSprite);
        g_AnmManager->DrawNoRotation(bombSprite);
        bombSprite++;

        bombSprite->pos = player->bombInfo.bombRegionPositions[idx] + bombSprite->posOffset;
        player->SetToTopLeftPos(bombSprite);
        g_AnmManager->DrawNoRotation(bombSprite);
        bombSprite++;
    }
}

#pragma var_order(local8, viewport, darkeningTimeLeft)
void BombData::DarkenViewport(Player *player)
{
    ZunRect viewport;
    f32 darkeningTimeLeft;
    i32 darknessLevel; // Controls alpha level of black rectangle drawn over view

    viewport.left = 32.0f;
    viewport.top = 16.0f;
    viewport.right = 416.0f;
    viewport.bottom = 464.0f;

    if (player->bombInfo.timer < 60)
    {
        darkeningTimeLeft = (player->bombInfo.timer.AsFramesFloat() * 176.0f) / 60.0f;
        darknessLevel = darkeningTimeLeft >= 176.0f ? 176 : (i32)darkeningTimeLeft;
    }
    else if (player->bombInfo.timer >= player->bombInfo.duration + -60)
    {
        darkeningTimeLeft = ((player->bombInfo.duration - player->bombInfo.timer.AsFramesFloat()) * 176.0f) / 60.0f;
        darknessLevel = darkeningTimeLeft < 0.0f ? 0 : (i32)darkeningTimeLeft;
    }
    else
    {
        darknessLevel = 176;
    }

    ScreenEffect::DrawSquare(&viewport, darknessLevel << 24);
}
} // namespace th06
