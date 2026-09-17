struct GuiImpl {
    int vms[26];
    GuiImpl();
};
inline void DoNothingWithPointer(void* p) {
    // do nothing
}
#pragma optimize("s", on)
GuiImpl::GuiImpl() {
    int padding[26];
    DoNothingWithPointer(padding);
}
#pragma optimize("", on)
