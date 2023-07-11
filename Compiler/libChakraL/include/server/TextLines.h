#include <vector>
#include <istream>
#include <streambuf>
#include <filesystem>
#include <memory>

namespace ChakraL
{

    struct TextPosition
    {
        std::size_t line;
        std::size_t character;
    };

    /**
     * @brief Text separated into lines for easier file editing work
     *
     */
    class TextLines
    {
        std::vector<std::wstring> mTextLines;

    public:
        TextLines(std::wistream &in);
        TextLines(const std::wstring &str);

        void replace(TextPosition begin, TextPosition end, const TextLines &lines);

        inline const std::vector<std::wstring> &lines() const { return mTextLines; };
    };

    /**
     * @brief streambuf for reading from TextLines
     *
     */
    class TextLinesStreambuf : public std::wstreambuf
    {
    public:
        TextLinesStreambuf(const TextLines &file);

    protected:
        int_type underflow() override;

    private:
        const TextLines &mSrc;
        std::vector<std::wstring>::size_type mPos;
    };
}