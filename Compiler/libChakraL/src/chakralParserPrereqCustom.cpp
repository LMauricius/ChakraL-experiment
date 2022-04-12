#include "chakralParserPrereqCustom.h"

#ifdef CHAKRAL_PARSER_TYPE_Custom

namespace ChakraL
{
    SemanticNode::~SemanticNode() {
    };
    void SemanticNode::process() {
    };
    std::string_view SemanticNode::name() const {
        return "UNDEFINED_NODE";
    };
    
    bool SemanticNodeVariable::trySet(SemanticNodePtr newPtr) {
        if (ptr == nullptr || newPtr->isSuccessful || !ptr->isSuccessful) {ptr = newPtr; return true;} else {return false;}
    }
    
    void SemanticNode::pullFrom(SemanticNode& other) {
        for (auto& varNodesPair : other.nodeLists) {
            const std::string &varName = varNodesPair.first;
            auto &otherList = varNodesPair.second;
            auto &myList = nodeLists[varName];
            myList.splice(otherList.begin(), otherList);
        }
        for (auto& varTokensPair : other.tokenLists) {
            const std::string &varName = varTokensPair.first;
            auto &otherList = varTokensPair.second;
            auto &myList = tokenLists[varName];
            otherList.splice(myList.begin(), myList);
        }
    };
    
    SemanticNodePtr getOrganized(SemanticNodePtr node, bool checkReplacement)
    {
        if (checkReplacement) {
            for (auto cNode = node; cNode != nullptr; cNode = cNode->continuationNode) {
                if (cNode->replacementNode) return getOrganized(cNode->replacementNode, true);
            }
        }
        for (auto& nameListPair : node->nodeLists) {
            for (auto& nodePtrRef : nameListPair.second) {
                if (nodePtrRef) nodePtrRef = getOrganized(nodePtrRef, true);
            }
        }
        if (node->continuationNode) {
            //auto contNodePtr = getOrganized(node->continuationNode, false);
            //node->pullFrom(*getOrganized(node->continuationNode, false));
            //node->continuationNode = nullptr;
            node->continuationNode = getOrganized(node->continuationNode, false);
        }
        return node;
    }

    void extractErrors(SemanticNodePtr node, std::list<ParserError>& outErrors)
    {
        for (auto& nameListPair : node->nodeLists) {
            for (auto& nodePtrRef : nameListPair.second) {
                if (nodePtrRef) extractErrors(nodePtrRef, outErrors);
            }
        }
        if (node->continuationNode) {
            extractErrors(node->continuationNode, outErrors);
        }
        if (node->replacementNode) {
            extractErrors(node->replacementNode, outErrors);
        }
        for (auto& e : node->errors) outErrors.push_back(e);
    }

}

#endif