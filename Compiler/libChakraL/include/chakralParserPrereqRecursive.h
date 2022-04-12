#pragma once
    
#include <list>
#include <string>
#include <map>
#include <set>
#include <memory>
#include "chakralParserPrereqShared.h"

namespace ChakraL {
    
    class SemanticNode {
    public:
        virtual ~SemanticNode();
        virtual std::string_view name() const = 0;
        
        std::map<std::string, std::list<SemanticNodePtr>> nodeLists;
        std::map<std::string, std::list<Token>> tokenLists;
        
        std::list<ParserError> errors;
    };
	
	void extractErrors(SemanticNodePtr node, std::list<ParserError>& outErrors);
}