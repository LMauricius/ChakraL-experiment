#include "server/TextLines.h"

namespace ChakraL
{
    TextLines::TextLines(std::wistream& in)
    {

    }

    TextLinesStreambuf::TextLinesStreambuf(const TextLines &file) : mSrc(file), mPos(0)
    {
        setg(nullptr, nullptr, nullptr);
    }
    
    std::wstreambuf::int_type TextLinesStreambuf::underflow()
    {
        if (mPos >= mSrc.lines().size())
        {
            return traits_type::eof();
        }

        const std::wstring &line = mSrc.lines()[mPos];
        setg(
            const_cast<wchar_t *>(line.c_str()),
            const_cast<wchar_t *>(line.c_str()),
            const_cast<wchar_t *>(line.c_str() + line.length())
        );

        mPos++;

        return traits_type::to_int_type(*gptr());
    }
}