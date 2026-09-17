with open('src/Gui.hpp', 'r') as f:
    gui_hpp = f.read()

gui_hpp = gui_hpp.replace("""struct PadEvilNoWhy
{
    PadEvilNoWhy()
    {
        FAKE_INLINE_DWORD_STACK_PADDING<16>();
    }
};""", """struct __declspec(align(8)) PadEvilNoWhy
{
    PadEvilNoWhy()
    {
        FAKE_INLINE_DWORD_STACK_PADDING<16>();
    }
};""")

with open('src/Gui.hpp', 'w') as f:
    f.write(gui_hpp)
