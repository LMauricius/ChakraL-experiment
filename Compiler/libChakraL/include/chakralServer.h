#pragma once

#include "chakralModel.h"
#include "../autoinclude/chakralSemanticNodesAutogen.h"

#include <filesystem>
#include <optional>

namespace ChakraL {

    class Server {
    public:
        void addIncludeDirectory(std::filesystem::path &&path);
        void addInput(std::filesystem::path &&path);
        
        void setBuildDirectory(std::filesystem::path &&path);
        void setOutputPrefix(std::filesystem::path &&path);
        void setOutputExecutablePrefix(std::filesystem::path &&path);
        void setOutputLibraryPrefix(std::filesystem::path &&path);
        void setOutputInterfacePrefix(std::filesystem::path &&path);

        std::optional<std::string> processLSPQuery(const std::string& query);

    };
}