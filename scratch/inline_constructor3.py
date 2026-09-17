import re

with open('src/Gui.hpp', 'r') as f:
    hpp = f.read()

# Make sure GuiMsgVm and GuiFormattedText have inline constructors
hpp = re.sub(r'struct GuiMsgVm\s*\{(?:\s*GuiMsgVm\(\)\s*\{\s*this->timer\.Initialize\(\);\s*\})?\s*i32 state;', """struct GuiMsgVm
{
    GuiMsgVm() { this->timer.Initialize(); }
    i32 state;""", hpp)

hpp = re.sub(r'struct GuiFormattedText\s*\{[^}]*ZunTimer timer;\s*(?:GuiFormattedText\(\) \{ this->timer\.Initialize\(\); \}\s*)?\};', """struct GuiFormattedText
{
    D3DXVECTOR3 pos;
    i32 fmtArg;
    i32 isShown;
    ZunTimer timer;
    GuiFormattedText() { this->timer.Initialize(); }
};""", hpp)

with open('src/Gui.hpp', 'w') as f:
    f.write(hpp)

with open('src/Gui.cpp', 'r') as f:
    cpp = f.read()

cpp = re.sub(r'GuiImpl::GuiImpl\(\)\s*\{[^}]*\}', """GuiImpl::GuiImpl()
{
}""", cpp)

with open('src/Gui.cpp', 'w') as f:
    f.write(cpp)
