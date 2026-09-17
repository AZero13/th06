with open('src/Gui.hpp', 'r') as f:
    text = f.read()

text = text.replace('struct GuiMsgVm\n{', 'struct GuiMsgVm\n{\n    GuiMsgVm() {}\n')

with open('src/Gui.hpp', 'w') as f:
    f.write(text)
