#pragma once

#include "chakralContext.h"

#include <memory>

namespace ChakraL {

    class Scope;
    using ScopePtr = std::shared_ptr<Scope>;// maybe turn to raw
    using MainScopePtr = std::shared_ptr<Scope>;// maybe turn to unique

    class Scope {
    public:
        Scope(Scope &parentScope);
        
        Value& getMember(const Identifier& identifier);

        Scope *const parentScope;
        ContextPtr base;
    };
}