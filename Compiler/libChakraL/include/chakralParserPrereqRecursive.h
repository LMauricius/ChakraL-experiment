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
        virtual std::string_view className() const = 0;
        virtual void print(std::ostream& out, size_t tabs) const = 0;
        
        std::map<std::string, std::list<SemanticNodePtr>> nodeLists;
        std::map<std::string, std::list<Token>> tokenLists;
        
        std::list<ParserError> errors;
    };
	
	void extractErrors(SemanticNodePtr node, std::list<ParserError>& outErrors);
}