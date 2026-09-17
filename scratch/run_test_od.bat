@echo off
set WINEPREFIX=Z:\Users\main\Untitled\scripts\prefix
wine cmd /c "Z:\Users\main\Untitled\scripts\prefix\bin\cl.exe /nologo /c /Od /Os /Gy /GF /Op scratch\test_od.cpp /Foscratch\test_od.obj"
wine cmd /c "Z:\Users\main\Untitled\scripts\prefix\bin\dumpbin.exe /DISASM scratch\test_od.obj > scratch\test_od.asm"
