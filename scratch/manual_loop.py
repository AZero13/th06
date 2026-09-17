import re

with open('src/ItemManager.cpp', 'r') as f:
    cpp = f.read()

cpp = re.sub(r'ItemManager::ItemManager\(\)\s*\{[^}]*\}', """ItemManager::ItemManager()
{
    for (int i = 0; i < 513; i++)
    {
        this->items[i].anm.AnmVm::AnmVm();
        this->items[i].timer.Initialize();
    }
}""", cpp)

with open('src/ItemManager.cpp', 'w') as f:
    f.write(cpp)
