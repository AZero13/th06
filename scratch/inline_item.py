import re

with open('src/ItemManager.hpp', 'r') as f:
    hpp = f.read()

hpp = hpp.replace("""struct Item
{
    Item() = default;
    AnmVm anm;""", """struct Item
{
    Item() {
        ZunTimer* timer = &this->timer;
        timer->Initialize();
    }
    AnmVm anm;""")

with open('src/ItemManager.hpp', 'w') as f:
    f.write(hpp)
