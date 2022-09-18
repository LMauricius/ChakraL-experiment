# How to read the documentation

## Documentation structure
The documentation is structured in several chapters:
* Introduction - introduction to the language, its goals, and stuff needed to start writing the code
* Basic concepts - helps understand the language and its terminology
* Language features - describes all the features of the language in detail
* Standard library - describes the modules included with the compiler
* Reference compiler - how to use the reference compiler
* Style guide - the recommended writing style for readability

## Syntax notation

Usually, a BNF notation is used to describe a programming language's syntax. For simplicity, this documentation doesn't use a BNF notation to describe the syntax. Parentheses, brackets, braces and other special characters that usually denote repeating or optional patterns won't have special meaning in the documentation. Instead we use the symbol `<...>` to say the patern continues, and describe the tiny details by words.

So if the BNF notation would be:
```
<ListLiteral> ::= LEFT_BRACKET [<Expression> (COMMA <Expression>)* [COMMA]] RIGHT_BRACKET
```

The documentation will describe it as:
```
🞱 🞥 • ⟦ ⟧ ⟨ ⟩ ⟪ ⟫ ⟮ ⟯ ⟬ ⟭ ⌈ ⌉ ⌊ ⌋ ⦇ ⦈ ⦉ ⦊ 【 】 ❪ ❫ ⁅ ⁆
[EXPRESSION1, EXPRESSION2 <...>]
```
and say empty lists and trailing commas are allowed.

## Formal syntax notation
To view the formal syntax in a BNF-like notation, look at the reference compiler's source code at `Compiler/libChakraL/syntaxdef/parser.txt` instead. Note that the compiler itself could in theory be buggy, so check the parser.txt specification file for reference.
The parser specification file would describe the syntax like this:
```
ListLiteral = '[' items::Expression (',' items::Expression)* [','] ']'
```
The meaning of special characters are described in the parser specification file itself.