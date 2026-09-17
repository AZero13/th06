with open('src/ZunTimer.hpp', 'r') as f:
    content = f.read()

replacement = """struct ZunTimer
{
    i32 previous;
    f32 subFrame;
    i32 current;

    ZunBool operator==(i32 time)"""

content = content.replace("""struct ZunTimer
{
    i32 previous;
    f32 subFrame;
    i32 current;

    ZunTimer()
    {
        this->Initialize();
    }

    ZunBool operator==(i32 time)""", replacement)

with open('src/ZunTimer.hpp', 'w') as f:
    f.write(content)
