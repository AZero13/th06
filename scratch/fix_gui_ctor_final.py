import re

with open('src/Gui.hpp', 'r') as f:
    gui_hpp = f.read()

# Add inline constructor to GuiFormattedText
gui_hpp = gui_hpp.replace("""struct GuiFormattedText
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
    f.write(gui_hpp)

with open('src/Gui.cpp', 'r') as f:
    gui_cpp = f.read()

# Remove explicit timer initializations from GuiImpl::GuiImpl
gui_cpp = gui_cpp.replace("""GuiImpl::GuiImpl()
{
    this->bonusScore.timer.Initialize();
    this->spellCardBonus.timer.Initialize();
    this->fullPowerMode.timer.Initialize();
}""", """GuiImpl::GuiImpl()
{
}""")

with open('src/Gui.cpp', 'w') as f:
    f.write(gui_cpp)
