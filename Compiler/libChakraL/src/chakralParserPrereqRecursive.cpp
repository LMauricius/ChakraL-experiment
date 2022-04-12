#include "chakralParserPrereqRecursive.h"

#ifdef CHAKRAL_PARSER_TYPE_Recursive

namespace ChakraL
{
    SemanticNode::~SemanticNode() {
    };

    void extractErrors(SemanticNodePtr node, std::list<ParserError>& outErrors)
    {
        for (auto& nameListPair : node->nodeLists) {
            for (auto& nodePtrRef : nameListPair.second) {
                if (nodePtrRef) extractErrors(nodePtrRef, outErrors);
            }
        }
        for (auto& e : node->errors) outErrors.push_back(e);
    }

}

#endif