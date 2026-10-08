#pragma once

// Everything every translation unit needs, precompiled through this header
// (/YXglobal.h). Headers do not include each other; the order here matters,
// since MSVC emits precompiled inline functions in definition order.
// clang-format off
#include "AnmIdx.hpp"
#include "dxutil.hpp"
#include "decomp.hpp"
#include "ZunColor.hpp"
#include <windows.h>
#include <d3dx8math.h>
#include "ZunMath.hpp"
#include "ZunResult.hpp"
#include "Chain.hpp"
#include "ZunBool.hpp"
#include "i18n.hpp"
#include "pbg3/Pbg3Archive.hpp"
#include <d3d8.h>
#include <d3dx8.h>
#include <stdarg.h>
#include <stdio.h>
#include "Global.hpp"
#include <dinput.h>
#include "Supervisor.hpp"
#include "ZunTimer.hpp"
#include "AnmVm.hpp"
#include "ReplayData.hpp"
#include "ResultScreen.hpp"
#include "GameManager.hpp"
#include "AnmManager.hpp"
#include "BulletManager.hpp"
#include <math.h>
#include "Player.hpp"
#include "BombData.hpp"
#include "BulletData.hpp"
#include "ChainPriorities.hpp"
#include "ItemManager.hpp"
#include <dsound.h>
#include <mmreg.h>
#include <mmsystem.h>
#include "zwave.hpp"
#include "SoundPlayer.hpp"
#include "EclManager.hpp"
#include "Effect.hpp"
#include "EffectManager.hpp"
#include "Ending.hpp"
#include <string.h>
#include "Enemy.hpp"
#include "EnemyEclInstr.hpp"
#include "EnemyManager.hpp"
#include "GameWindow.hpp"
#include "Gui.hpp"
#include "MainMenu.hpp"
#include "MusicRoom.hpp"
#include "ReplayManager.hpp"
#include <d3d8types.h>
#include "ScreenEffect.hpp"
#include "Stage.hpp"
#include "StageMenu.hpp"
#include "TextHelper.hpp"
// clang-format on
