with open('src/ItemManager.cpp', 'r') as f:
    code = f.read()

new_code = code.replace("""ItemManager::ItemManager()
{
    i32 i = 0;
    for (; i < ARRAY_SIZE_SIGNED(this->items); i++)
    {
        this->items[i].sprite.__ctor();
    }
}""", """ItemManager::ItemManager()
{
}""")

with open('src/ItemManager.cpp', 'w') as f:
    f.write(new_code)
