import re

with open('src/Gui.hpp', 'r') as f:
    text = f.read()

text = re.sub(r'\n    GuiFormattedText\(\)\n    \{\n        this->timer\.Initialize\(\);\n    \}\n', '', text)
with open('src/Gui.hpp', 'w') as f:
    f.write(text)

with open('src/Gui.cpp', 'r') as f:
    text = f.read()

# find GuiImpl::GuiImpl() and insert this->bonusScore.timer.Initialize();
text = text.replace('GuiImpl::GuiImpl()\n{', 'GuiImpl::GuiImpl()\n{\n    this->bonusScore.timer.Initialize();\n    this->fullPowerMode.timer.Initialize();\n    this->spellCardBonus.timer.Initialize();\n')
with open('src/Gui.cpp', 'w') as f:
    f.write(text)
