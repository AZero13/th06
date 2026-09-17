inline void InlineFunc() {
}
void NormalFunc() {
}
void* get_inline() { return (void*)InlineFunc; }
void* get_normal() { return (void*)NormalFunc; }
