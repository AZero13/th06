import re

with open('src/Gui.hpp', 'r') as f:
    hpp = f.read()

# Add GuiMsgVm constructor to Gui.hpp
hpp = hpp.replace("""struct GuiMsgVm
{
    i32 state;""", """struct GuiMsgVm
{
    GuiMsgVm()
    {
        this->timer.Initialize();
    }
    i32 state;""")

# Remove GuiFormattedText constructor from Gui.hpp
hpp = re.sub(r'\s*GuiFormattedText\(\) \{ this->timer\.Initialize\(\); \}', '', hpp)

with open('src/Gui.hpp', 'w') as f:
    f.write(hpp)

with open('src/Gui.cpp', 'r') as f:
    cpp = f.read()

# Remove GuiMsgVm constructor from Gui.cpp
cpp = re.sub(r'GuiMsgVm::GuiMsgVm\(\)\s*\{\s*this->timer\.Initialize\(\);\s*\}\s*', '', cpp)

# Add explicit timers to GuiImpl::GuiImpl()
cpp = cpp.replace("""GuiImpl::GuiImpl()
{
}""", """GuiImpl::GuiImpl()
{
    this->bonusScore.timer.Initialize();
    this->spellCardBonus.timer.Initialize();
    this->fullPowerMode.timer.Initialize();
}""")

with open('src/Gui.cpp', 'w') as f:
    f.write(cpp)
