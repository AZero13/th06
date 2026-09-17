#include <stdio.h>

void NonInlineFunc();

__forceinline void InlineFunc() {
    NonInlineFunc();
}

void TestFunc() {
    for (int i = 0; i < 10; i++) {
        InlineFunc();
    }
}
