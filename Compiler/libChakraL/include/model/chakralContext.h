#pragma once

#include "chakralIdentifier.h"
#include "chakralRequirement.h"

#include <vector>
#include <map>
#include <memory>

namespace ChakraL {

    class Value;

    class Context;
    using ContextPtr = std::shared_ptr<Context>;// maybe turn to raw
    using MainContextPtr = std::shared_ptr<Context>;// maybe turn to unique

    class Context {
    public:
        std::map<Identifier, Value> declarations;
        std::vector<Requirement> requirements;
        std::vector<ContextPtr> inclusions;
    };
}