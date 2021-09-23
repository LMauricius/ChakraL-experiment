#include "chakralLexer.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include <chrono>

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

        std::list<ChakraL::LexerError> errors;
        auto startLexTime = high_resolution_clock::now();
        std::list<ChakraL::Token> tokens = ChakraL::tokenize(text, errors);
        auto endLexTime = high_resolution_clock::now();
        std::cout << "Lexer finished in " << duration<double>(endLexTime - startLexTime).count() << "s" << std::endl;

        for (auto& t : tokens)
        {
            std::cout << ChakraL::TokenNames[(int)t.type] << "-" << t.line << "," << t.character << ": ";
            std::wcout << t.str << std::endl;
        }
        for (auto& e : errors)
        {
            std::cout << "Error at line " << e.line << ", position " << e.character << ": ";
            std::wcout << e.msg << std::endl;
        }

        file.close();
    }
}