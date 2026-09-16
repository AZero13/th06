#include "BombData.hpp"
#include "EffectManager.hpp"
#include "Global.hpp"
#include "Gui.hpp"
#include "ScreenEffect.hpp"
#include "i18n.hpp"

namespace th06
{
#pragma var_order(i, starSprite, unused, starAngle)
void BombData::BombMarisaACalc(Player *player)
{

    f32 starAngle;
    i32 unused[3];
    AnmVm *starSprite;
    i32 i;

    if (player->bombInfo.timer >= player->bombInfo.duration)
    {
        g_Gui.EndPlayerSpellcard();
        player->bombInfo.isInUse = 0;
        return;
    }

    if (player->bombInfo.timer.HasTicked() && player->bombInfo.timer == 0)
    {
        g_ItemManager.RemoveAllItems();
        g_Gui.ShowBombNamePortrait(ANM_SCRIPT_FACE_ENEMY_SPELLCARD_PORTRAIT, TH_MARISA_A_BOMB_NAME);
        player->bombInfo.duration = 250;
        player->invulnerabilityTimer.SetCurrent(300);

        starSprite = player->bombInfo.sprites[0];
        for (i = 0; i < ARRAY_SIZE_SIGNED(player->bombInfo.sprites); i++, starSprite++)
        {
            g_AnmManager->ExecuteAnmIdx(starSprite, ANM_SCRIPT_PLAYER_MARISA_A_BLUE_STAR + i % 3);
            player->bombInfo.bombRegionPositions[i] = player->positionCenter;

            starAngle = i * ZUN_2PI / 8.0f;

            player->bombInfo.bombRegionVelocities[i].x = cosf(starAngle) * 2;

            player->bombInfo.bombRegionVelocities[i].y = sinf(starAngle) * 2;
            player->bombInfo.bombRegionVelocities[i].z = 0.0f;
        }
        g_SoundPlayer.PlaySoundByIdx(SOUND_BOMB_REIMARI, 0);
        ScreenEffect::RegisterChain(SCREEN_EFFECT_SHAKE, 120, 4, 1, 0);
    }
    else
    {
        for (i = 0; i < ARRAY_SIZE_SIGNED(player->bombInfo.sprites); i++)
        {
            player->bombInfo.bombRegionPositions[i] +=
                player->bombInfo.bombRegionVelocities[i] * g_Supervisor.effectiveFramerateMultiplier;

            if (player->bombInfo.timer.HasTicked() && player->bombInfo.timer.AsFrames() % 3 != 0)
            {
                player->bombProjectiles[i].posX = player->bombInfo.bombRegionPositions[i].x;
                player->bombProjectiles[i].posY = player->bombInfo.bombRegionPositions[i].y;
                player->bombProjectiles[i].sizeX = 128.0f;
                player->bombProjectiles[i].sizeY = 128.0f;
                player->bombRegionSizes[i].x = 128.0f;
                player->bombRegionSizes[i].y = 128.0f;

                player->bombRegionPositions[i] = player->bombInfo.bombRegionPositions[i];
                player->bombRegionDamages[i] = 8;
            }
            g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][i]);
        }
    }
    player->playerState = PLAYER_STATE_INVULNERABLE;
    player->bombInfo.timer.Tick();

    return;
}

#pragma var_order(bombSprite, idx)
void BombData::BombMarisaADraw(Player *player)
{

    AnmVm *bombSprite;
    i32 idx;

    BombData::DarkenViewport(player);
    bombSprite = &player->bombInfo.sprites[0][0];
    for (idx = 0; idx < ARRAY_SIZE_SIGNED(player->bombInfo.sprites); idx++)
    {

        bombSprite->pos = player->bombInfo.bombRegionPositions[idx];
        bombSprite->pos.x += g_GameManager.arcadeRegionTopLeftPos.x;
        bombSprite->pos.y += g_GameManager.arcadeRegionTopLeftPos.y;
        bombSprite->pos.z = 0.0f;
        bombSprite->scaleX = 3.2f;
        bombSprite->scaleY = 3.2f;
        g_AnmManager->Draw(bombSprite);

        bombSprite->pos -= player->bombInfo.bombRegionVelocities[idx] * 6.0f;
        bombSprite->pos.x += -32.0f;
        bombSprite->pos.y += -32.0f;
        bombSprite->pos.z = 0.0f;
        bombSprite->scaleX = 2.2f;
        bombSprite->scaleY = 2.2f;
        g_AnmManager->Draw(bombSprite);

        bombSprite->pos -= player->bombInfo.bombRegionVelocities[idx] * 2.0f;
        bombSprite->pos.x += 64.0f;
        bombSprite->pos.y += 64.0f;
        bombSprite->pos.z = 0.0f;

        bombSprite->pos -= player->bombInfo.bombRegionVelocities[idx] * 2.0f;
        bombSprite->pos.x += -32.0f;
        bombSprite->pos.y += -32.0f;
        bombSprite->pos.z = 0.0f;
        bombSprite->scaleX = 1.0f;
        bombSprite->scaleY = 1.0f;
        g_AnmManager->Draw(bombSprite);
        bombSprite++;
    }
}

}; // namespace th06
