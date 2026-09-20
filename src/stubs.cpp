#include "th06.hpp"
#include <stdio.h>

using namespace th06;

// Force the linker to include virtual function tables that would otherwise be
// dropped by /OPT:REF. These vtables reference scalar_deleting_destructors as
// COMDAT associatives, so including the vtable transitively pulls in the
// destructor code — matching the original binary without adding any function
// bodies.
#pragma comment(linker, "/INCLUDE:??_7CSound@th06@@6B@")
#pragma comment(linker, "/INCLUDE:??_7CStreamingSound@th06@@6B@")
#pragma comment(linker, "/INCLUDE:??_7IPbg3Parser@th06@@6B@")
#pragma comment(linker, "/INCLUDE:??_7Pbg3Parser@th06@@6BIPbg3Parser@1@@")
#pragma comment(linker, "/INCLUDE:??_7Pbg3Parser@th06@@6BFileAbstraction@1@@")
