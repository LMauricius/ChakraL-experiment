#pragma once

#include "chakralBlock.h"
#include "chakralSourceFile.h"

namespace ChakraL {

    class Module {
    public:
        std::vector<std::shared_ptr<Module>> usedModules;
        Context context;

        std::vector<std::shared_ptr<SourceFile>> files;

    };
}