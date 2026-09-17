import re

with open('src/ItemManager.hpp', 'r') as f:
    hpp = f.read()

hpp = re.sub(r'struct Item\s*\{(?:\s*Item\(\)\s*\{\s*ZunTimer\* timer = &this->timer;\s*timer->Initialize\(\);\s*\})?', """struct Item
{
    Item()
    {
        this->timer.Initialize();
    }""", hpp)

with open('src/ItemManager.hpp', 'w') as f:
    f.write(hpp)

with open('src/ItemManager.cpp', 'r') as f:
    cpp = f.read()

cpp = re.sub(r'ItemManager::ItemManager\(\)\s*\{[^}]*\}', """ItemManager::ItemManager()
{
}""", cpp)

with open('src/ItemManager.cpp', 'w') as f:
    f.write(cpp)
