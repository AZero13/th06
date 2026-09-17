struct AnmVm {
    void Initialize() {}
    AnmVm() { Initialize(); }
    int data[68];
};
struct GuiMsgVm {
    int stuff[6];
    AnmVm portraits[2];
    AnmVm dialogueLines[2];
    AnmVm introLines[2];
    int more_stuff[10];
};
struct GuiImpl {
    GuiImpl();
    AnmVm vms[26];
    int stuff2[2];
    AnmVm stageNameSprite;
    AnmVm songNameSprite;
    AnmVm playerSpellcardPortrait;
    AnmVm enemySpellcardPortrait;
    AnmVm bombSpellcardName;
    AnmVm enemySpellcardName;
    AnmVm bombSpellcardBackground;
    AnmVm enemySpellcardBackground;
    AnmVm loadingScreenSprite;
    GuiMsgVm msg;
    int stuff3[10];
};

GuiImpl::GuiImpl() {
    int dummy[26];
}
