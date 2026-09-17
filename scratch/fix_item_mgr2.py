with open('src/ItemManager.hpp', 'r') as f:
    item_mgr = f.read()

item_mgr = item_mgr.replace("""    Item()
    {
        ZunTimer* pTimer = &this->timer;
        pTimer->Initialize();
    }""", """    Item()
    {
        this->timer.Initialize();
    }""")

with open('src/ItemManager.hpp', 'w') as f:
    f.write(item_mgr)
