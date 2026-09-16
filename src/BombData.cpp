#include "BombData.hpp"

#include "EffectManager.hpp"
#include "Global.hpp"
#include "Gui.hpp"
#include "ScreenEffect.hpp"
#include "i18n.hpp"

namespace th06
{
DIFFABLE_STATIC_ARRAY_ASSIGN(BombData, 4, g_BombData) = {
    /* ReimuA  */ {BombData::BombReimuACalc, BombData::BombReimuADraw},
    /* ReimuB  */ {BombData::BombReimuBCalc, BombData::BombReimuBDraw},
    /* MarisaA */ {BombData::BombMarisaACalc, BombData::BombMarisaADraw},
    /* MarisaB */ {BombData::BombMarisaBCalc, BombData::BombMarisaBDraw},
};

}; // namespace th06
