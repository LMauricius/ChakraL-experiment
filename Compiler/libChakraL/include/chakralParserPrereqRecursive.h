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
        virtual void print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const = 0;
        virtual std::vector<const SemanticNode*> getSubNodes() const = 0;
	    void extractErrors(std::list<ParserError>& outErrors) const;
        
        std::list<ParserError> errors;
    };
	
}