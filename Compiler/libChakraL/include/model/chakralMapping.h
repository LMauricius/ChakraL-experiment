#pragma once

#include "chakralContext.h"
#include "chakralScope.h"

namespace ChakraL {

    class Mapping : public Context {
    public:
        Scope code;
    };
}