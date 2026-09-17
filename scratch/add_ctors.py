import re

# Item
with open('src/ItemManager.hpp', 'r') as f:
    text = f.read()
text = text.replace('struct Item\n{', 'struct Item\n{\n    Item()\n    {\n        this->timer.Initialize();\n    }\n')
with open('src/ItemManager.hpp', 'w') as f:
    f.write(text)

# PlayerBullet
with open('src/Player.hpp', 'r') as f:
    text = f.read()
text = text.replace('struct PlayerBullet\n{', 'struct PlayerBullet\n{\n    PlayerBullet()\n    {\n        this->unk_140.Initialize();\n    }\n')
with open('src/Player.hpp', 'w') as f:
    f.write(text)

# GuiMsgVm and GuiFormattedText
with open('src/Gui.hpp', 'r') as f:
    text = f.read()
text = text.replace('struct GuiMsgVm\n{', 'struct GuiMsgVm\n{\n    GuiMsgVm()\n    {\n        this->timer.Initialize();\n    }\n')
text = text.replace('struct GuiFormattedText\n{', 'struct GuiFormattedText\n{\n    GuiFormattedText()\n    {\n        this->timer.Initialize();\n    }\n')
with open('src/Gui.hpp', 'w') as f:
    f.write(text)

# AsciiManagerPopup
with open('src/AsciiManager.hpp', 'r') as f:
    text = f.read()
text = text.replace('struct AsciiManagerPopup\n{', 'struct AsciiManagerPopup\n{\n    AsciiManagerPopup()\n    {\n        this->timer.Initialize();\n    }\n')
with open('src/AsciiManager.hpp', 'w') as f:
    f.write(text)
