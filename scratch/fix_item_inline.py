with open('src/ItemManager.hpp', 'r') as f:
    itemmgr_hpp = f.read()

# Replace Item constructor declaration with inline definition
item_ctor_decl = """    i8 state;
    Item();
};"""
item_ctor_def_inline = """    i8 state;
    Item()
    {
        this->timer.Initialize();
    }
};"""
itemmgr_hpp = itemmgr_hpp.replace(item_ctor_decl, item_ctor_def_inline)

with open('src/ItemManager.hpp', 'w') as f:
    f.write(itemmgr_hpp)

with open('src/ItemManager.cpp', 'r') as f:
    itemmgr_cpp = f.read()

# Remove Item constructor definition from cpp
item_ctor_def_cpp = """
Item::Item()
{
    this->timer.Initialize();
}

ItemManager::ItemManager()"""
itemmgr_cpp = itemmgr_cpp.replace(item_ctor_def_cpp, "ItemManager::ItemManager()")

with open('src/ItemManager.cpp', 'w') as f:
    f.write(itemmgr_cpp)
