#include "chakralParserPrereqRecursive.h"

#ifdef CHAKRAL_PARSER_TYPE_Recursive

namespace ChakraL
{
    SemanticNode::~SemanticNode() {
    };

    void SemanticNode::extractErrors(std::list<ParserError>& outErrors) const
    {
        for (auto& node : getSubNodes()) {
            if (node) node->extractErrors(outErrors);
        }
        for (auto& e : errors) outErrors.push_back(e);
    }

}

#endif