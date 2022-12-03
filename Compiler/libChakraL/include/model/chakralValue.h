#pragma once

#include "chakralContext.h"

#include <optional>
#include <memory.h>

namespace ChakraL {

    class Context;

    class Value {
    public:
        std::optional<ContextPtr> known_data;
        ContextPtr trait;

        bool spec_const : 1 = false;
        bool spec_mut : 1 = false;
        bool spec_static : 1 = false;
    };
}