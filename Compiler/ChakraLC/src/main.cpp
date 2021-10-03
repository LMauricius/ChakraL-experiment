#include "chakralLexer.h"
#include "chakralParser.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include <chrono>

void printTabs(int tabs)
{
    for (int i=0; i < tabs; i++) std::cout << "  ";
}
void printNode(ChakraL::SemanticNodePtr nodePtr, int tabs)
{
    for (auto& nameListPair : nodePtr->nodeLists)
    {
        //printTabs(tabs); std::cout << "'" << nameListPair.first << "'" << "(nodes): ";
        for (auto np : nameListPair.second)
        {
            if (np)
            {
                printTabs(tabs); std::cout << "'" << nameListPair.first << "': " << np->name() << " {" << std::endl;
                printNode(np, tabs + 1);
                printTabs(tabs); std::cout << "}";
                std::cout << std::endl;
            }
            else
            {
                printTabs(tabs); std::cout << "'" << nameListPair.first << "': ERROR-nullptr" << std::endl;
            }
        }
    }
    for (auto& nameListPair : nodePtr->tokenLists)
    {
        //printTabs(tabs); std::cout << "'" << nameListPair.first << "'" << "(tokens): ";
        for (auto& t : nameListPair.second)
        {
            printTabs(tabs);
            std::cout << "'" << nameListPair.first << "': " << ChakraL::TokenNames[(int)t.type] << "-" << t.line << "," << t.character << ": ";
            std::wcout << t.str;
            std::cout << std::endl;
        }
    }
    if (nodePtr->continuationNode)
    {
        printNode(nodePtr->continuationNode, tabs);
    }
}

int main(int argc, char** argv)
{
    /*std::wstring s = L"2021/9/12";
    auto result = ctre::starts_with<L"(?<year>\\d{4})/(?<month>\\d{1,2})/(?<day>\\d{1,2})">(s);
    //std::string y1 = result.get<"year">().to_string();
    std::wstring y2 = result.get<"year">().to_string();

    //std::cout << result.get<"year">() << " " << result.get<"month">() << " " << result.get<"day">() << std::endl;
    //std::cout << y1 << std::endl;
    std::wcout << result.to_view() << std::endl;
    std::wcout << result.get<"year">().to_view() << " " << result.get<"month">().to_view() << " " << result.get<"day">().to_view() << std::endl;
    //std::wcout << result.get<"year">().to_string() << std::endl;
    std::wcout << result.to_view().length() << std::endl;
    std::wcout << std::endl;*/

    using namespace std::chrono;

    if (argc >= 2)
    {
        std::wifstream file;
        std::wstring text;
        std::wstringstream ss;
        file.open(argv[1]);

        ss << file.rdbuf();
        text = ss.str();

        //text = std::wstring(std::istream_iterator<wchar_t, wchar_t>(file), std::istream_iterator<wchar_t, wchar_t>());

        std::list<ChakraL::LexerError> lerrors;
        auto startLexTime = high_resolution_clock::now();
        std::list<ChakraL::Token> tokens = ChakraL::tokenize(text, lerrors);
        auto endLexTime = high_resolution_clock::now();
        std::cout << "Lexer finished in " << duration<double>(endLexTime - startLexTime).count() << "s" << std::endl;

        for (auto& t : tokens)
        {
            std::cout << ChakraL::TokenNames[(int)t.type] << "-" << t.line << "," << t.character << ": ";
            std::wcout << t.str << std::endl;
        }
        for (auto& e : lerrors)
        {
            std::cout << "Error at line " << e.line << ", position " << e.character << ": ";
            std::wcout << e.msg << std::endl;
        }
        
        std::list<ChakraL::ParserError> perrors;
        auto startParsTime = high_resolution_clock::now();
        ChakraL::SemanticNodePtr node = ChakraL::parse(tokens, perrors);
        auto endParsTime = high_resolution_clock::now();
        std::cout << "Parser finished in " << duration<double>(endParsTime - startParsTime).count() << "s" << std::endl;
        printNode(node, 1);

        /*for (auto& t : tokens)
        {
            std::cout << ChakraL::TokenNames[(int)t.type] << "-" << t.line << "," << t.character << ": ";
            std::wcout << t.str << std::endl;
        }*/
        for (auto& e : perrors)
        {
            std::wcout << L"Error at line " << e.token.line << L", position " << e.token.character << L", token " << e.token.str << L": ";
            std::wcout << e.msg << std::endl;
        }

        file.close();
    }
}