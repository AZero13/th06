import re
with open('src/Global.hpp', 'r') as f:
    text = f.read()

new_func = """
    inline void FakeMissingPiece() {
        void *painA = (void *)&TextOut;
        void *painB = (void *)&SetBkMode;
        void *painC = (void *)&SetTextColor;
        void *fake = (void *)&DrawText;
        void *map1 = (void *)&MapViewOfFile;
        void *map2 = (void *)&CreateFileMappingA;
        void *map3 = (void *)&UnmapViewOfFile;
        void *map4 = (void *)&CloseHandle;
        
        memmove(NULL, NULL, 0);
        strlen("test_string_literal_for_icf_12345");
        throw "error";
    }
"""

if 'FakeMissingPiece' not in text:
    text = text.replace('struct CMyFont\n{', 'struct CMyFont\n{\n' + new_func)
    with open('src/Global.hpp', 'w') as f:
        f.write(text)
