import re
import os

with open('src/ItemManager.cpp', 'r') as f:
    content = f.read()

content = content.replace('(i32)(60 > curItem->timer.current)', 'curItem->timer < 60')
content = content.replace('(i32)(curItem->timer.current == 60)', 'curItem->timer == 60')

with open('src/ItemManager.cpp', 'w') as f:
    f.write(content)

with open('src/Gui.cpp', 'r') as f:
    content = f.read()

content = content.replace('(i32)(this->msg.timer.current >= this->msg.currentInstr->time)', 'this->msg.timer >= this->msg.currentInstr->time')
content = content.replace('(i32)(this->msg.timer.current < 60)', 'this->msg.timer < 60')
content = content.replace('(i32)(this->impl->bonusScore.timer.current < 30)', 'this->impl->bonusScore.timer < 30')
content = content.replace('(i32)(250 <= this->impl->bonusScore.timer.current)', 'this->impl->bonusScore.timer >= 250')
content = content.replace('(i32)(this->impl->fullPowerMode.timer.current < 30)', 'this->impl->fullPowerMode.timer < 30')
content = content.replace('(i32)(180 <= this->impl->fullPowerMode.timer.current)', 'this->impl->fullPowerMode.timer >= 180')
content = content.replace('(i32)(280 <= this->impl->spellCardBonus.timer.current)', 'this->impl->spellCardBonus.timer >= 280')

with open('src/Gui.cpp', 'w') as f:
    f.write(content)
