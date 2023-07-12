#include "server/TextLines.h"

namespace ChakraL
{
    TextLines::TextLines(std::wistream &in)
    {
        std::wstring line;

        while (std::getline(in, line))
        {
            if (line.back() != L'\n')
            {
                line += L'\n';
            }
            mLineList.emplace_back(std::move(line));
        }
    }

    TextLines::TextLines(const std::wstring &str)
    {
        std::size_t lnstart = 0, lnend = 0;

        while ((lnend = str.find_first_of(L'\n', lnend + 1)) != std::wstring::npos)
        {
            mLineList.emplace_back(str.substr(lnstart, lnend + 1));
        }

        if (lnend + 1 != str.size())
        {
            mLineList.emplace_back(str.substr(lnstart, lnend + 1));
        }
    }

    void TextLines::replace(TextPosition begin, TextPosition end, const TextLines &other)
    {
        // save partial lines that we preserve
        std::wstring beginPrefix, endSuffix;
        beginPrefix = mLineList[begin.line].substr(0, begin.character);
        endSuffix = mLineList[end.line].substr(end.character, std::wstring::npos);

        // replace whole lines
        if (end.line - begin.line + 1 < other.mLineList.size())
        {
            std::copy(
                other.mLineList.begin(),
                other.mLineList.begin() + end.line - begin.line + 1,
                mLineList.begin() + begin.line);
            mLineList.insert(
                mLineList.begin() + end.line,
                other.mLineList.begin() + end.line - begin.line + 1,
                other.mLineList.end());
        }
        else
        {
            std::copy(
                other.mLineList.begin(),
                other.mLineList.end(),
                mLineList.begin() + begin.line);
            mLineList.erase(
                mLineList.begin() + begin.line + other.mLineList.size(),
                mLineList.begin() + end.line);
        }

        // restore partial lines that shouldn't be replaced
        mLineList[begin.line].insert(0, beginPrefix);
        mLineList[begin.line + other.mLineList.size() - 1] += endSuffix;
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
            const_cast<wchar_t *>(line.c_str() + line.length()));

        mPos++;

        return traits_type::to_int_type(*gptr());
    }
}