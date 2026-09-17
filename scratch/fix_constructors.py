with open('src/AnmVm.hpp', 'r') as f:
    anmvm_hpp = f.read()

# Replace inline constructor with declaration
replacement_anmvm = """    AnmVm();
"""
anmvm_hpp = anmvm_hpp.replace("""    AnmVm()
    {
        this->activeSpriteIndex = -1;
    }""", replacement_anmvm)

with open('src/AnmVm.hpp', 'w') as f:
    f.write(anmvm_hpp)

with open('src/AnmManager.cpp', 'r') as f:
    anmmgr_cpp = f.read()

# Add AnmVm constructor
anmvm_ctor = """
AnmVm::AnmVm()
{
    this->activeSpriteIndex = -1;
}
"""
anmmgr_cpp = anmmgr_cpp.replace("namespace th06\n{", "namespace th06\n{" + anmvm_ctor)

with open('src/AnmManager.cpp', 'w') as f:
    f.write(anmmgr_cpp)

with open('src/ItemManager.hpp', 'r') as f:
    itemmgr_hpp = f.read()

# Add Item constructor declaration
item_ctor_decl = """    i8 state;
    Item();
};"""
itemmgr_hpp = itemmgr_hpp.replace("""    i8 state;
};""", item_ctor_decl)

with open('src/ItemManager.hpp', 'w') as f:
    f.write(itemmgr_hpp)

with open('src/ItemManager.cpp', 'r') as f:
    itemmgr_cpp = f.read()

# Add Item constructor definition
item_ctor_def = """
Item::Item()
{
    this->timer.Initialize();
}

ItemManager::ItemManager()"""
itemmgr_cpp = itemmgr_cpp.replace("ItemManager::ItemManager()", item_ctor_def)

with open('src/ItemManager.cpp', 'w') as f:
    f.write(itemmgr_cpp)
