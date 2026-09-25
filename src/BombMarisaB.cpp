#include "BombData.hpp"

#include "EffectManager.hpp"
#include "Global.hpp"
#include "Gui.hpp"
#include "ScreenEffect.hpp"
#include "i18n.hpp"

namespace th06
{
#pragma var_order(i, bombSprite, unusedVector)
void BombData::BombMarisaBCalc(Player *player)
{
    AnmVm *bombSprite;
    i32 i;
    D3DXVECTOR3 unusedVector;

    if (player->bombInfo.timer >= player->bombInfo.duration)
    {
        g_Gui.EndPlayerSpellcard();
        player->bombInfo.isInUse = false;
        player->verticalMovementSpeedMultiplierDuringBomb = 1.0f;
        player->horizontalMovementSpeedMultiplierDuringBomb = 1.0f;
        return;
    }

    if (player->bombInfo.timer.HasTicked() && player->bombInfo.timer == 0)
    {
        g_ItemManager.RemoveAllItems();
        g_Gui.ShowBombNamePortrait(ANM_SCRIPT_FACE_BOMB_PORTRAIT, TH_MARISA_B_BOMB_NAME);
        player->bombInfo.duration = 300;
        player->invulnerabilityTimer = 360;
        bombSprite = player->bombInfo.sprites[0];
        for (i = 0; i < 4; i++, bombSprite++)
        {
            g_AnmManager->ExecuteAnmIdx(bombSprite, ANM_SCRIPT_PLAYER_MARISA_B_MASTER_SPARK + i);
            player->bombInfo.bombRegionPositions[i] = player->positionCenter;
        }
        g_SoundPlayer.PlaySoundByIdx(SOUND_BOMB_MARISA_B);
        player->verticalMovementSpeedMultiplierDuringBomb = 0.3f;
        player->horizontalMovementSpeedMultiplierDuringBomb = 0.3f;
    }
    else
    {
        if (player->bombInfo.timer == 60)
        {
            ScreenEffect::RegisterChain(SCREEN_EFFECT_SHAKE, 60, 1, 7, 0);
        }
        else if (player->bombInfo.timer == 120)
        {
            ScreenEffect::RegisterChain(SCREEN_EFFECT_SHAKE, 200, 24, 0, 0);
        }

        if (player->bombInfo.timer.HasTicked() && player->bombInfo.timer % 4 != 0)
        {
            player->bombProjectiles[0].posX = 192.0f;
            player->bombProjectiles[0].posY = player->positionCenter.y / 2.0f;
            player->bombProjectiles[0].sizeX = 384.0f;
            player->bombProjectiles[0].sizeY = player->positionCenter.y;
            player->bombRegionSizes[0].x = 384.0f;
            player->bombRegionSizes[0].y = player->positionCenter.y;
            player->bombRegionPositions[0].x = player->bombProjectiles[0].posX;
            player->bombRegionPositions[0].y = player->bombProjectiles[0].posY;
            player->bombRegionDamages[0] = 12;
        }

        g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][0]);
        g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][1]);
        g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][2]);
        g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][3]);
    }

    player->playerState = PLAYER_STATE_INVULNERABLE;
    player->bombInfo.timer++;
}

#pragma var_order(bombSprite, i, spriteAngle)
void BombData::BombMarisaBDraw(Player *player)
{
    AnmVm *bombSprite;
    i32 i;
    f32 spriteAngle;

    BombData::DarkenViewport(player);
    bombSprite = player->bombInfo.sprites[0];
    for (i = 0; i < 4; i++)
    {
        spriteAngle = (((ZUN_PI / 5.0f) * i) / 3.0f - ZUN_PI) + (ZUN_2PI / 5.0f);
        bombSprite->pos = player->positionCenter;
        bombSprite->pos.x += (cosf(spriteAngle) * bombSprite->sprite->heightPx * bombSprite->scaleY) / 2.0f;
        bombSprite->pos.y += (sinf(spriteAngle) * bombSprite->sprite->heightPx * bombSprite->scaleY) / 2.0f;
        spriteAngle = ZUN_HALF_PI - spriteAngle;
        bombSprite->rotation.z = utils::AddNormalizeAngle(spriteAngle, ZUN_PI);
        bombSprite->pos.x += g_GameManager.arcadeRegionTopLeftPos.x;
        bombSprite->pos.y += g_GameManager.arcadeRegionTopLeftPos.y;
        bombSprite->pos.z = 0.0f;
        g_AnmManager->Draw(bombSprite);
        bombSprite++;
    }
}
} // namespace th06
