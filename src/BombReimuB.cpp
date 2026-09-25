#include "BombData.hpp"

#include "EffectManager.hpp"
#include "Global.hpp"
#include "Gui.hpp"
#include "ScreenEffect.hpp"
#include "i18n.hpp"

namespace th06
{
#pragma var_order(i, bombSprite, unusedVector)
void BombData::BombReimuBCalc(Player *player)
{
    AnmVm *bombSprite;
    i32 i;
    D3DXVECTOR3 unusedVector;

    if (player->bombInfo.timer >= player->bombInfo.duration)
    {
        g_Gui.EndPlayerSpellcard();
        player->bombInfo.isInUse = false;
        return;
    }

    if (player->bombInfo.timer.HasTicked() && player->bombInfo.timer == 0)
    {
        g_ItemManager.RemoveAllItems();
        g_Gui.ShowBombNamePortrait(ANM_SCRIPT_FACE_ENEMY_SPELLCARD_PORTRAIT, TH_REIMU_B_BOMB_NAME);
        player->bombInfo.duration = 140;
        player->invulnerabilityTimer = 200;
        bombSprite = player->bombInfo.sprites[0];

        for (i = 0; i < 4; i++, bombSprite++)
        {
            g_AnmManager->ExecuteAnmIdx(bombSprite, ANM_SCRIPT_PLAYER_REIMU_B_BOMB_ARRAY + i);
        }

        g_SoundPlayer.PlaySoundByIdx(SOUND_BOMB_REIMARI);
        player->bombInfo.bombRegionPositions[0].x = player->positionCenter.x;
        player->bombInfo.bombRegionPositions[0].y = 224.0f;
        player->bombInfo.bombRegionPositions[0].z = 0.42f;
        player->bombInfo.bombRegionPositions[1].x = 192.0f;
        player->bombInfo.bombRegionPositions[1].y = player->positionCenter.y;
        player->bombInfo.bombRegionPositions[1].z = 0.415f;
        player->bombInfo.bombRegionPositions[2].x = player->positionCenter.x;
        player->bombInfo.bombRegionPositions[2].y = 224.0f;
        player->bombInfo.bombRegionPositions[2].z = 0.41f;
        player->bombInfo.bombRegionPositions[3].x = 192.0f;
        player->bombInfo.bombRegionPositions[3].y = player->positionCenter.y;
        player->bombInfo.bombRegionPositions[3].z = 0.405f;
        ScreenEffect::RegisterChain(SCREEN_EFFECT_SHAKE, 60, 2, 6, 0);
    }
    else
    {
        if (player->bombInfo.timer == 60)
        {
            ScreenEffect::RegisterChain(SCREEN_EFFECT_SHAKE, 80, 20, 0, 0);
        }

        player->bombProjectiles[0].sizeX = 62.0f;
        player->bombProjectiles[0].sizeY = 448.0f;
        player->bombProjectiles[1].sizeX = 384.0f;
        player->bombProjectiles[1].sizeY = 62.0f;
        player->bombProjectiles[2].sizeX = 62.0f;
        player->bombProjectiles[2].sizeY = 448.0f;
        player->bombProjectiles[3].sizeX = 384.0f;
        player->bombProjectiles[3].sizeY = 62.0f;

        for (i = 0; i < 4; i++)
        {
            g_AnmManager->ExecuteScript(&player->bombInfo.sprites[0][i]);
            if (player->bombInfo.timer.HasTicked() && player->bombInfo.timer % 2 != 0)
            {
                player->bombProjectiles[i].posX =
                    player->bombInfo.bombRegionPositions[i].x + player->bombInfo.sprites[0][i].posOffset.x;
                player->bombProjectiles[i].posY =
                    player->bombInfo.bombRegionPositions[i].y + player->bombInfo.sprites[0][i].posOffset.y;
                player->bombRegionSizes[i].x = player->bombProjectiles[i].sizeX;
                player->bombRegionSizes[i].y = player->bombProjectiles[i].sizeY;
                player->bombRegionPositions[i] =
                    player->bombInfo.bombRegionPositions[i] + player->bombInfo.sprites[0][i].posOffset;
                player->bombRegionDamages[i] = 8;
            }
        }
    }

    player->playerState = PLAYER_STATE_INVULNERABLE;
    player->bombInfo.timer++;
}

#pragma var_order(bombSprite, i)
void BombData::BombReimuBDraw(Player *player)
{
    AnmVm *bombSprite;
    i32 i;

    BombData::DarkenViewport(player);
    bombSprite = player->bombInfo.sprites[0];
    for (i = 0; i < 4; i++, bombSprite++)
    {
        bombSprite->pos = player->bombInfo.bombRegionPositions[i] + bombSprite->posOffset;
        bombSprite->pos.x += g_GameManager.arcadeRegionTopLeftPos.x;
        bombSprite->pos.y += g_GameManager.arcadeRegionTopLeftPos.y;
        bombSprite->pos.z = 0.0f;
        g_AnmManager->Draw(bombSprite);
    }
}
} // namespace th06
