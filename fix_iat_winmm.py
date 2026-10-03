with open('src/Global.hpp', 'r') as f:
    text = f.read()

text = text.replace('void *map4 = (void *)&CloseHandle;', 'void *map4 = (void *)&CloseHandle;\n    void *m1 = (void *)&mmioGetInfo;\n    void *m2 = (void *)&mmioAdvance;')
with open('src/Global.hpp', 'w') as f:
    f.write(text)
