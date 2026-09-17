import re

# Remove ZunTimer constructor
with open('src/ZunTimer.hpp', 'r') as f:
    text = f.read()
text = re.sub(r'\n    ZunTimer\(\)\n    \{\n        this->Initialize\(\);\n    \}\n', '', text)
with open('src/ZunTimer.hpp', 'w') as f:
    f.write(text)

# Remove GuiMsgVm and GuiFormattedText constructors
with open('src/Gui.hpp', 'r') as f:
    text = f.read()
text = text.replace('GuiMsgVm() {}', '')
text = text.replace('GuiFormattedText() {}', '')
with open('src/Gui.hpp', 'w') as f:
    f.write(text)

# Remove FakePaddedAnmVm
with open('src/AnmVm.hpp', 'r') as f:
    text = f.read()
text = re.sub(r'struct FakePaddedAnmVm : AnmVm\n\{\n    FakePaddedAnmVm\(\)\n    \{\n        FAKE_INLINE_DWORD_STACK_PADDING<4>\(\);\n    \}\n\};\n', '', text)
with open('src/AnmVm.hpp', 'w') as f:
    f.write(text)
