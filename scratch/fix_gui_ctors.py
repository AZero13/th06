with open('src/Gui.hpp', 'r') as f:
    gui_hpp = f.read()

# Add constructor for GuiMsgVm
gui_hpp = gui_hpp.replace("""struct GuiMsgVm
{
    AnmVm unk_0;""", """struct GuiMsgVm
{
    GuiMsgVm();
    AnmVm unk_0;""")

# GuiFormattedText DOES NOT have a constructor!

# Add constructor for GuiImpl
gui_hpp = gui_hpp.replace("""struct GuiImpl
{
    GuiMsgVm msg;""", """struct GuiImpl
{
    GuiImpl();
    GuiMsgVm msg;""")

with open('src/Gui.hpp', 'w') as f:
    f.write(gui_hpp)

with open('src/Gui.cpp', 'r') as f:
    gui_cpp = f.read()

ctors = """
GuiMsgVm::GuiMsgVm()
{
    this->timer.Initialize();
}

GuiImpl::GuiImpl()
{
    this->bonusScore.timer.Initialize();
    this->spellcardBonus.timer.Initialize();
    this->fullPowerMode.timer.Initialize();
}
"""

gui_cpp = gui_cpp.replace("""GuiImpl::GuiImpl() {

};""", ctors)

with open('src/Gui.cpp', 'w') as f:
    f.write(gui_cpp)
