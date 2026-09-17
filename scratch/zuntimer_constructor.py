import re

with open('src/ZunTimer.hpp', 'r') as f:
    hpp = f.read()

hpp = hpp.replace("""struct ZunTimer
{""", """struct ZunTimer
{
    ZunTimer()
    {
        this->Initialize();
    }""")

with open('src/ZunTimer.hpp', 'w') as f:
    f.write(hpp)

with open('src/Gui.hpp', 'r') as f:
    gui_hpp = f.read()

gui_hpp = re.sub(r'GuiMsgVm\(\)\s*\{\s*this->timer\.Initialize\(\);\s*\}', 'GuiMsgVm() = default;', gui_hpp)
gui_hpp = re.sub(r'GuiFormattedText\(\)\s*\{\s*this->timer\.Initialize\(\);\s*\}', 'GuiFormattedText() = default;', gui_hpp)

with open('src/Gui.hpp', 'w') as f:
    f.write(gui_hpp)
