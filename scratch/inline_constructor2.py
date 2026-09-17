import re

with open('src/Gui.hpp', 'r') as f:
    hpp = f.read()

# Add GuiFormattedText constructor to Gui.hpp
hpp = hpp.replace("""struct GuiFormattedText
{
    D3DXVECTOR3 pos;
    i32 fmtArg;
    i32 isShown;
    ZunTimer timer;
};""", """struct GuiFormattedText
{
    D3DXVECTOR3 pos;
    i32 fmtArg;
    i32 isShown;
    ZunTimer timer;
    GuiFormattedText() { this->timer.Initialize(); }
};""")

with open('src/Gui.hpp', 'w') as f:
    f.write(hpp)

with open('src/Gui.cpp', 'r') as f:
    cpp = f.read()

# Remove explicit timers from GuiImpl::GuiImpl()
cpp = cpp.replace("""GuiImpl::GuiImpl()
{
    this->bonusScore.timer.Initialize();
    this->spellCardBonus.timer.Initialize();
    this->fullPowerMode.timer.Initialize();
}""", """GuiImpl::GuiImpl()
{
}""")

with open('src/Gui.cpp', 'w') as f:
    f.write(cpp)
