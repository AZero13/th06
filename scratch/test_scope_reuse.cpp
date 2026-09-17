#include <stdio.h>

void CallMe();

void ScopeReuseNoCall() {
    { int a[4]; }
    { int b[4]; }
    { int c[4]; }
}

void ScopeReuseWithCall() {
    { int a[4]; }
    { int b[4]; }
    CallMe();
    { int c[4]; }
}

void ScopeReuseWithCallInside() {
    { int a[4]; }
    { int b[4]; CallMe(); }
    { int c[4]; }
}
