import sys
import re

def repl(file_path, find_str, repl_str):
    with open(file_path, 'r') as f:
        content = f.read()
    if find_str in content:
        content = content.replace(find_str, repl_str)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Patched {file_path}")
    else:
        print(f"Could not find target in {file_path}")

# AsciiManager.cpp
repl("src/AsciiManager.cpp",
"""DIFFABLE_STATIC(ChainElem, g_AsciiManagerOnDrawMenusChain)
DIFFABLE_STATIC(AsciiManager, g_AsciiManager)""",
"""DIFFABLE_STATIC(AsciiManager, g_AsciiManager)
DIFFABLE_STATIC(ChainElem, g_AsciiManagerCalcChain)
DIFFABLE_STATIC(ChainElem, g_AsciiManagerOnDrawMenusChain)
DIFFABLE_STATIC(ChainElem, g_AsciiManagerOnDrawPopupsChain)""")

# BulletManager.cpp
repl("src/BulletManager.cpp",
"""DIFFABLE_STATIC(BulletManager, g_BulletManager);
DIFFABLE_STATIC(ChainElem, g_BulletManagerCalcChain);
DIFFABLE_STATIC(ChainElem, g_BulletManagerDrawChain);""",
"""DIFFABLE_STATIC(ChainElem, g_BulletManagerCalcChain);
DIFFABLE_STATIC(ChainElem, g_BulletManagerDrawChain);
DIFFABLE_STATIC(BulletManager, g_BulletManager);""")

# EclManager.cpp
repl("src/EclManager.cpp",
"""DIFFABLE_STATIC(EclManager, g_EclManager);""",
"""DIFFABLE_STATIC(ChainElem, g_EclManagerCalcChain); // unused
DIFFABLE_STATIC(EclManager, g_EclManager);""")

# EclManager.hpp
repl("src/EclManager.hpp",
"""enum TimelineOpcode
{
    TIMELINE_OPCODE_CREATE_ENEMY = 0x0,
    TIMELINE_OPCODE_CREATE_ENEMY_OFFSET = 0x1,
    TIMELINE_OPCODE_JUMP = 0x2,
    TIMELINE_OPCODE_BOSS_WAIT = 0x3,
};""",
"""enum TimelineOpcode
{
    TIMELINE_OPCODE_CREATE_ENEMY = 0x0,
    TIMELINE_OPCODE_CREATE_ENEMY_OFFSET = 0x1,
    TIMELINE_OPCODE_JUMP = 0x2,
    TIMELINE_OPCODE_BOSS_WAIT = 0x3,
};

struct EclManagerExtraData
{
    unsigned char unknownA[0x80];
    f32 starAngleTable[6];
    unsigned char unknownB[0x68];
    D3DXVECTOR3 coords[8];
};""")

repl("src/EclManager.hpp",
"""    EclTimelineInstr *timeline;
};
ZUN_ASSERT_SIZE(EclManager, 0xc);""",
"""    EclTimelineInstr *timeline;
    EclManagerExtraData extra;
};
ZUN_ASSERT_SIZE(EclManager, 0x16c);""")

# EffectManager.cpp
repl("src/EffectManager.cpp",
"""EffectManager::EffectManager()
{
    this->Reset();
}

void EffectManager::Reset()""",
"""void EffectManager::Reset()""")

# EffectManager.hpp
repl("src/EffectManager.hpp",
"""    Effect effects[513];

    EffectManager();""",
"""    Effect effects[513];

    EffectManager()
    {
        this->Reset();
    }""")

# EnemyEclInstr.cpp
repl("src/EnemyEclInstr.cpp",
"""DIFFABLE_STATIC_ARRAY(f32, 6, g_StarAngleTable);
DIFFABLE_STATIC(D3DXVECTOR3, g_EnemyPosVector);
DIFFABLE_STATIC(D3DXVECTOR3, g_PlayerPosVector);""",
"""""")

repl("src/EnemyEclInstr.cpp",
"""        g_EnemyPosVector = enemy->position;
        g_PlayerPosVector = g_Player.positionCenter;
        g_StarAngleTable[0] = g_Rng.GetRandomF32ZeroToOne() * (ZUN_PI * 2) - ZUN_PI;
        g_StarAngleTable[1] = utils::AddNormalizeAngle(g_StarAngleTable[0], 4 * ZUN_PI / 5);""",
"""        g_EclManager.extra.coords[0] = enemy->position;
        g_EclManager.extra.coords[1] = g_Player.positionCenter;
        g_EclManager.extra.starAngleTable[0] = g_Rng.GetRandomF32ZeroToOne() * (ZUN_PI * 2) - ZUN_PI;
        g_EclManager.extra.starAngleTable[1] = utils::AddNormalizeAngle(g_EclManager.extra.starAngleTable[0], 4 * ZUN_PI / 5);""")

repl("src/EnemyEclInstr.cpp",
"""        g_StarAngleTable[0] = g_StarAngleTable[1];
        g_StarAngleTable[1] = utils::AddNormalizeAngle(g_StarAngleTable[0], 4 * ZUN_PI / 5);
        g_StarAngleTable[2] = utils::AddNormalizeAngle(g_StarAngleTable[1], 4 * ZUN_PI / 5);
        g_StarAngleTable[3] = utils::AddNormalizeAngle(g_StarAngleTable[2], 4 * ZUN_PI / 5);
        g_StarAngleTable[4] = utils::AddNormalizeAngle(g_StarAngleTable[3], 4 * ZUN_PI / 5);
        g_StarAngleTable[5] = utils::AddNormalizeAngle(g_StarAngleTable[4], 4 * ZUN_PI / 5);""",
"""        g_EclManager.extra.starAngleTable[0] = g_EclManager.extra.starAngleTable[1];
        g_EclManager.extra.starAngleTable[1] = utils::AddNormalizeAngle(g_EclManager.extra.starAngleTable[0], 4 * ZUN_PI / 5);
        g_EclManager.extra.starAngleTable[2] = utils::AddNormalizeAngle(g_EclManager.extra.starAngleTable[1], 4 * ZUN_PI / 5);
        g_EclManager.extra.starAngleTable[3] = utils::AddNormalizeAngle(g_EclManager.extra.starAngleTable[2], 4 * ZUN_PI / 5);
        g_EclManager.extra.starAngleTable[4] = utils::AddNormalizeAngle(g_EclManager.extra.starAngleTable[3], 4 * ZUN_PI / 5);
        g_EclManager.extra.starAngleTable[5] = utils::AddNormalizeAngle(g_EclManager.extra.starAngleTable[4], 4 * ZUN_PI / 5);""")

repl("src/EnemyEclInstr.cpp",
"""        baseTargetPosition = (g_PlayerPosVector - g_EnemyPosVector) * targetDistance + g_EnemyPosVector;""",
"""        baseTargetPosition = (g_EclManager.extra.coords[1] - g_EclManager.extra.coords[0]) * targetDistance + g_EclManager.extra.coords[0];""")

repl("src/EnemyEclInstr.cpp",
"""            sincosmul(&starPatternTarget0, g_StarAngleTable[i], enemy->currentContext.float3);
            sincosmul(&starPatterTarget1, g_StarAngleTable[i + 1], enemy->currentContext.float3);""",
"""            sincosmul(&starPatternTarget0, g_EclManager.extra.starAngleTable[i], enemy->currentContext.float3);
            sincosmul(&starPatterTarget1, g_EclManager.extra.starAngleTable[i + 1], enemy->currentContext.float3);""")


# EnemyManager.cpp
repl("src/EnemyManager.cpp",
"""DIFFABLE_STATIC(EnemyManager, g_EnemyManager)
DIFFABLE_STATIC(ChainElem, g_EnemyManagerCalcChain)
DIFFABLE_STATIC(ChainElem, g_EnemyManagerDrawChain)""",
"""DIFFABLE_STATIC(ChainElem, g_EnemyManagerCalcChain)
DIFFABLE_STATIC(ChainElem, g_EnemyManagerDrawChain)
DIFFABLE_STATIC(EnemyManager, g_EnemyManager)""")

# Gui.cpp
repl("src/Gui.cpp",
"""DIFFABLE_STATIC(Gui, g_Gui);
DIFFABLE_STATIC(ChainElem, g_GuiDrawChain);
DIFFABLE_STATIC(ChainElem, g_GuiCalcChain);""",
"""DIFFABLE_STATIC(Gui, g_Gui);
DIFFABLE_STATIC(ChainElem, g_GuiCalcChain);
DIFFABLE_STATIC(ChainElem, g_GuiDrawChain);""")

# ItemManager.cpp
repl("src/ItemManager.cpp",
"""DIFFABLE_STATIC(ItemManager, g_ItemManager);""",
"""DIFFABLE_STATIC(ItemManager, g_ItemManager);
DIFFABLE_STATIC(ChainElem, g_ItemManagerCalcChain); // unused
DIFFABLE_STATIC(ChainElem, g_ItemManagerDrawChain); // unused""")


# MainMenu.cpp
repl("src/MainMenu.cpp",
"""MainMenu::MainMenu()
{
}""",
"""""")

# MainMenu.hpp
repl("src/MainMenu.hpp",
"""struct MainMenu
{
    MainMenu();
    ZunResult BeginStartup();""",
"""struct MainMenu
{
    ZunResult BeginStartup();""")

# SoundPlayer.cpp
repl("src/SoundPlayer.cpp",
"""SoundPlayer::SoundPlayer()
{
    memset(this, 0, sizeof(SoundPlayer));
    for (i32 i = 0; i < ARRAY_SIZE_SIGNED(this->unk408); i++)
    {
        this->unk408[i] = -1;
    }
}""",
"""""")

# SoundPlayer.hpp
repl("src/SoundPlayer.hpp",
"""struct SoundPlayer
{
    SoundPlayer();""",
"""struct SoundPlayer
{
    SoundPlayer()
    {
        memset(this, 0, sizeof(SoundPlayer));
        for (i32 i = 0; i < ARRAY_SIZE_SIGNED(this->unk408); i++)
        {
            this->unk408[i] = -1;
        }
    }""")

# Stage.cpp
repl("src/Stage.cpp",
"""DIFFABLE_STATIC_ARRAY_ASSIGN(StageFile, 8, g_StageFiles) = {
    {"data/stg0bg.anm", "data/stage0.std"},
    {"data/stg1bg.anm", "data/stage1.std"},
    {"data/stg2bg.anm", "data/stage2.std"},
    {"data/stg3bg.anm", "data/stage3.std"},
    {"data/stg4bg.anm", "data/stage4.std"},
    {"data/stg5bg.anm", "data/stage5.std"},
    {"data/stg6bg.anm", "data/stage6.std"},
    {"data/stg7bg.anm", "data/stage7.std"},
};
DIFFABLE_STATIC(ChainElem, g_AsciiManagerCalcChain)
DIFFABLE_STATIC(ChainElem, g_AsciiManagerOnDrawPopupsChain)
DIFFABLE_STATIC(ChainElem, g_StageOnDrawHighPrioChain)
DIFFABLE_STATIC(Stage, g_Stage)
DIFFABLE_STATIC(ChainElem, g_StageOnDrawLowPrioChain)
DIFFABLE_STATIC(ChainElem, g_StageCalcChain)""",
"""DIFFABLE_STATIC_ARRAY_ASSIGN(StageFile, 8, g_StageFiles) = {
    {"data/stg0bg.anm", "data/stage0.std"},
    {"data/stg1bg.anm", "data/stage1.std"},
    {"data/stg2bg.anm", "data/stage2.std"},
    {"data/stg3bg.anm", "data/stage3.std"},
    {"data/stg4bg.anm", "data/stage4.std"},
    {"data/stg5bg.anm", "data/stage5.std"},
    {"data/stg6bg.anm", "data/stage6.std"},
    {"data/stg7bg.anm", "data/stage7.std"},
};
DIFFABLE_STATIC(Stage, g_Stage)
DIFFABLE_STATIC(ChainElem, g_StageCalcChain)
DIFFABLE_STATIC(ChainElem, g_StageOnDrawHighPrioChain)
DIFFABLE_STATIC(ChainElem, g_StageOnDrawLowPrioChain)""")

