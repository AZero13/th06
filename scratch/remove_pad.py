with open('src/Gui.hpp', 'r') as f:
    gui_hpp = f.read()

gui_hpp = gui_hpp.replace("""    u8 bossHealthBarState;
    PadEvilNoWhy ew;""", """    u8 bossHealthBarState;""")

with open('src/Gui.hpp', 'w') as f:
    f.write(gui_hpp)
