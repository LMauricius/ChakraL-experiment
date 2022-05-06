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

    template<class Node_T>
    class Ptr : public std::shared_ptr<SemanticNode>
    {
    public:
        using std::shared_ptr<SemanticNode>::shared_ptr;

        Node_T *get() {
            return (Node_T*)std::shared_ptr<SemanticNode>::get();
        }

        Node_T& operator*() {
            return *get();
        }

        Node_T* operator->() {
            return get();
        }

        template<class T>
        T& operator->*(T Node_T::*v) {
            return get()->*v;
        }

        const Node_T *get() const {
            return (Node_T*)std::shared_ptr<SemanticNode>::get();
        }

        const Node_T& operator*() const {
            return *get();
        }

        const Node_T* operator->() const {
            return get();
        }

        template<class T>
        const T& operator->*(T Node_T::*v) const {
            return get()->*v;
        }
    };
    
    class ParserError {
    public:
        inline ParserError(Token token, std::wstring msg): token(token), msg(msg) {}
        std::wstring msg;
        Token token;
    };

}