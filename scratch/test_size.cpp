#include <stdio.h>
struct PadEvilNoWhy
{
    PadEvilNoWhy() {}
};
struct GuiImpl {
    int stuff[1];
    char bossHealthBarState;
    PadEvilNoWhy ew;
};
int main() {
    printf("%lu\n", sizeof(GuiImpl));
}
