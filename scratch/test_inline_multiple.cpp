#include <stdio.h>

void CallMe();

__forceinline void InlineWithVar() {
    int x[4];
    CallMe();
}

void TestFuncMultiple() {
    InlineWithVar();
    InlineWithVar();
    InlineWithVar();
}
