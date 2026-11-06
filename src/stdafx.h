#pragma once

// Portable compatibility header.
// Keep this file minimal: project modules should include their own direct
// dependencies, while the Windows-specific SDK headers remain guarded so the
// portable branch can still compile on non-Windows platforms without requiring a
// fixed include ordering or a precompiled-header setup.

#include "BuildVersion.hpp"

#if defined(_WIN32) || defined(_WIN64)
#ifndef _WIN32_WINNT
#define _WIN32_WINNT 0x0500
#endif
#ifndef DIRECTINPUT_VERSION
#define DIRECTINPUT_VERSION 0x0800
#endif

#include <windows.h>
#include <d3d8.h>
#include <d3dx8.h>
#include <dinput.h>
#include <dsound.h>
#include <mmsystem.h>
#endif

#include <cstdio>
#include <cstddef>

// Avoid pulling project-level headers here: they often depend on each other and
// can create circular or platform-specific include chains. Include the specific
// dependencies from the source files that need them instead.
