import re

with open('src/ItemManager.hpp', 'r') as f:
    hpp = f.read()

hpp = re.sub(r'struct Item\s*\{(?:\s*Item\(\)\s*\{[^}]*\}\s*)?', """struct Item
{
    Item()
    {
        this->timer = ZunTimer();
    }""", hpp)

with open('src/ItemManager.hpp', 'w') as f:
    f.write(hpp)

