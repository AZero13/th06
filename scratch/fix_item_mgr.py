import re

with open('src/ItemManager.hpp', 'r') as f:
    item_mgr = f.read()

item_mgr = item_mgr.replace("""    Item()
    {
        this->timer.Initialize();
    }""", """    Item()
    {
        ZunTimer* pTimer = &this->timer;
        pTimer->Initialize();
    }""")

with open('src/ItemManager.hpp', 'w') as f:
    f.write(item_mgr)
