#pragma once
    
#include <list>
#include <string>
#include <map>
#include <set>
#include <memory>
#include "../autoinclude/chakralLexerAutogen.h"

namespace ChakraL {

    class SemanticNode;
    using SemanticNodePtr = std::shared_ptr<SemanticNode>;
    
    class ParserError {
    public:
        inline ParserError(Token token, std::wstring msg): token(token), msg(msg) {}
        std::wstring msg;
        Token token;
    };

}