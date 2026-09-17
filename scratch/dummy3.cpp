struct AnmVm {
    AnmVm() {}
    ~AnmVm() {}
};
struct GuiImpl {
    AnmVm vms[26];
    GuiImpl();
};
#pragma optimize("s", on)
GuiImpl::GuiImpl() {}
#pragma optimize("", on)
