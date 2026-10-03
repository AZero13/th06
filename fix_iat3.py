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

text = text.replace('} // namespace th06', new_func + '\n} // namespace th06')
with open('src/Global.hpp', 'w') as f:
    f.write(text)
