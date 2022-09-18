from __future__ import annotations
import os
import re
from genUtil import *
from typing import Tuple

class Command:
    def __init__(self, name: str, arg: str):
        self.name = name
        self.arg = arg

class Rule:
    def __init__(self, regex: str):
        self.regex = regex
        self.commands: list[Command] = []

class Lexer:
    def __init__(self, macros: dict[str, str]):
        self.macros: dict[str, str] = macros
        self.regexNames: dict[str, str] = {}
        self.exactStringNames: dict[str, str] = {}
        self.stringTokenPairs: list[Tuple[str, str]] = []
        self.exactStrTokenPairs: list[Tuple[str, str]] = []
        self.tokenTypes: list[str] = ["END_OF_STR"]
        self.states: list[str] = []
        self.starting = ""
        self.rulesPerState: dict[str, list[Rule]] = {}

        self.macros["[:newl:]"] = "\\n"
        self.macros["[:alnum:]"] = "a-zA-Z0-9"
        self.macros["[:alpha:]"] = "a-zA-Z"
        self.macros["[:ascii:]"] = "\\x00-\\x7F"
        self.macros["[:blank:]"] = " \\t"
        self.macros["[:cntrl:]"] = "\\x00-\\x1F\\x7F"
        self.macros["[:digit:]"] = "0-9"
        self.macros["[:graph:]"] = "\\x21-\\x7E"
        self.macros["[:lower:]"] = "a-z"
        self.macros["[:print:]"] = "\\x20-\\x7E"
        self.macros["[:punct:]"] = "!\"\#$%&'()*+,\\-./:;<=>?@\\[\\\\\\]^_‘{|}~"
        self.macros["[:space:]"] = " \\t\\r\\n\\v\\f"
        self.macros["[:upper:]"] = "A-Z"
        self.macros["[:word:]"] = "A-Za-z0-9_"
        self.macros["[:xdigit:]"] = "A-Fa-f0-9"

def replaceMacros(regex: str, macros: dict[str, str]):
    ret = ""

    i = 0
    while i < len(regex):
        if regex[i:i+2] == '[:':
            ind = regex.find(']', i+1)
            if regex[ind-1] == ':':
                end = ind+1
                ret += macros[regex[i:end]]
                i = end
            else:
                ret += regex[i]
                i += 1
        else:
            ret += regex[i]
            i += 1


    return ret



def loadLexer(filename: str, macros: dict[str, str] ):
    print("Loading lexer ", filename)

    lines = meaningfulLines(filename)
    lexer = Lexer(macros)
    curState = ""

    try:
        lineInd = 0
        l, lineInd = next(lines, ("",-1))
        while len(l):
            #print("...Line ", l)

            if l[0] == '[':
                l2, lineInd = next(lines, ("",-1))
                lexer.macros[l] = replaceMacros(l2, lexer.macros)
            elif l[0] == '@':
                state = l[1:]
                #print("...Entered state ", state)
                if (len(lexer.states) == 0):
                    lexer.starting = state
                if not state in lexer.states:
                    lexer.states.append(state)
                lexer.rulesPerState[state] = []
                curState = state
            elif l[0] == '?' or l[0] == '=':
                if l[0] == '?':
                    # regex
                    regex = replaceMacros(l[2:], lexer.macros)
                    isExact = False
                else:# if l[0] == '='
                    # exact string
                    exactString = unescapeString(l[2:])
                    regex = exactString
                    special_chars_map = {
                        i: '\\' + chr(i) for i in b'()[]{}?*+-|^$\\.~ \t\n\r\v\f'
                    }
                    regex = exactString.translate(special_chars_map).replace('=', '[=]')
                    isExact = True

                if not regex in lexer.regexNames:
                    lexer.regexNames[regex] = "ruleRegex" + str(len(lexer.regexNames))

                # create rule
                rule = Rule(regex)
                #print("...Rule with regex ", regex)

                l, lineInd = next(lines, ("",-1))
                if l != '{':
                    raise FormatError("Expected a '{', got '"+l+"'", lineInd)
                
                # commands
                l, lineInd = next(lines, ("",-1))
                while l != '}':
                    spl = l.split()
                    if len(spl) > 1:
                        rule.commands.append(Command(spl[0], spl[1]))
                    else:
                        rule.commands.append(Command(spl[0], ""))
                    
                    if spl[0] == 'out':
                        if not spl[1] in lexer.tokenTypes:
                            lexer.tokenTypes.append(spl[1])
                        if isExact:
                            lexer.stringTokenPairs.append((exactString, spl[1]))

                    l, lineInd = next(lines, ("",-1))
                    if len(l) == 0:
                        raise FormatError("Expected a '}', got '"+l+"'", lineInd)


                # add rule
                lexer.rulesPerState[curState].append(rule)

            l, lineInd = next(lines, ("",-1))
    except FormatError as e:
        print("At line " + str(e.lineInd) + ": " + e.message)
        sys.exit(1)
    except StopIteration:
        pass
    
    return lexer




def writeLexerH(lexer: Lexer, filename: str):
    print("Writing lexer ", filename)
    f = open(filename, "wt")

    def TB():
        f.write('    ')
    def LN(s: str):
        f.write(s)
        f.write('\n')

    LN("// This file is autogenerated. Do not edit!")
    LN("")
    LN('#pragma once')
    LN("")
    LN('#include <list>')
    LN('#include <string>')
    LN('#include <vector>')
    LN('#include <array>')
    LN("")
    LN("namespace ChakraL {")
    LN("")
    TB();LN("enum class TokenType {")
    for t in lexer.tokenTypes:
        TB();TB();LN(t+',')
    TB();LN("};")
    LN("")
    TB();LN("extern const std::array<std::string, "+str(len(lexer.tokenTypes))+"> TokenNames;")
    TB();LN("extern const std::array<std::wstring, "+str(len(lexer.tokenTypes))+"> WTokenNames;")
    LN("")
    TB();LN("enum class LexerState {")
    for t in lexer.states:
        TB();TB();LN(t+',')
    TB();LN("};")
    LN("")
    TB();LN("class Token {")
    TB();LN('public:')
    TB();TB();LN('Token() = default;')
    TB();TB();LN('inline Token(TokenType type, int line, int character): type(type), line(line), character(character) {}')
    TB();TB();LN('inline Token(TokenType type, std::wstring str, int line, int character): type(type), str(str), line(line), character(character) {}')
    TB();TB();LN('Token(const Token&) = default;')
    TB();TB();LN('Token(Token&&) = default;')
    TB();TB();LN('Token& operator=(const Token&) = default;')
    TB();TB();LN('Token& operator=(Token&&) = default;')
    TB();TB();LN('TokenType type;')
    TB();TB();LN('std::wstring str;')
    TB();TB();LN('int line;')
    TB();TB();LN('int character;')
    TB();LN("};")
    LN("")
    TB();LN("class LexerError {")
    TB();LN('public:')
    TB();TB();LN('inline LexerError(int line, int character, std::wstring msg): line(line), character(character), msg(msg) {{}}')
    TB();TB();LN('std::wstring msg;')
    TB();TB();LN('int line;')
    TB();TB();LN('int character;')
    TB();LN("};")
    LN("")
    TB();LN("std::list<Token> tokenize(std::wstring &input, std::list<LexerError>& outErrors);")
    LN("")
    LN("}")

    f.close()


def writeLexerCPP(lexer: Lexer, filename: str, headerfile: str, useSingleDFA: bool):
    print("Writing lexer ", filename)
    f = open(filename, "wt")

    def TB():
        f.write('    ')
    def LN(s: str):
        f.write(s)
        f.write('\n')

    LN("// This file is autogenerated. Do not edit!")
    LN("")
    LN('#include "ctre-unicode.hpp"')
    LN('#include "../autoinclude/' + os.path.basename(headerfile) + '"')
    #LN('#include "ctre.hpp"')
    LN('#include <vector>')
    LN('#include <string_view>')
    #LN('#include <regex>') # obsolete
    LN('#include <sstream>')
    #LN('#include "ctre-unicode.hpp"')
    LN('#include <iostream>')
    LN("")
    LN("namespace")
    LN("{")
    #for reg in lexer.regexNames:
    #    TB();LN("const std::wregex " + lexer.regexNames[reg] + "(L\"" + escapeRegexToC(reg) + "\", std::wregex::extended);")
    LN("}")
    LN("namespace ChakraL")
    LN("{")
    TB();LN("const std::array<std::string, "+str(len(lexer.tokenTypes))+"> TokenNames {")
    for t in lexer.tokenTypes:
        TB();TB();LN('"'+t+'",')
    TB();LN("};")
    TB();LN("const std::array<std::wstring, "+str(len(lexer.tokenTypes))+"> WTokenNames {")
    for t in lexer.tokenTypes:
        TB();TB();LN('L"'+t+'",')
    TB();LN("};")
    LN("")
    TB();LN("std::list<Token> tokenize(std::wstring &input, std::list<LexerError>& outErrors)")
    TB();LN("{")
    TB();TB();LN("int line = 1, character = 1;")
    TB();TB();LN("int start = 0, maxEnd = -1;")
    TB();TB();LN("std::vector<LexerState> states = {{LexerState::" + lexer.starting + "}};")
    TB();TB();LN("std::list<Token> ret;")
    TB();TB();LN("")
    TB();TB();LN("while (start < input.size())")
    TB();TB();LN("{")
    TB();TB();TB();LN("int choosenRuleInd = -1;")
    TB();TB();TB();LN("bool movePtr = true;")
    '''
    TB();TB();TB();LN("std::wsmatch match;")
    '''
    TB();TB();TB();LN("std::wstring_view matchStr;")
    TB();TB();TB();LN("")
    TB();TB();TB();LN("switch (states.back())")
    TB();TB();TB();LN("{")
    for s in lexer.states:
        TB();TB();TB();LN("case LexerState::"+s+":")

        TB();TB();TB();TB();LN("")
        TB();TB();TB();TB();LN("// *** choose rule ***")

        if useSingleDFA:
            TB();TB();TB();TB();LN("if (auto res = ctre::starts_with<")
            i = 0
            for r in lexer.rulesPerState[s]:
                i += 1
                if i == 1:
                    TB();TB();TB();TB();TB();TB();LN("L\"(" + escapeRegexToC(r.regex) + ")\"")
                else:
                    TB();TB();TB();TB();TB();TB();LN("L\"|(" + escapeRegexToC(r.regex) + ")\"")

            TB();TB();TB();TB();TB();LN(">(std::wstring_view(input.begin()+start, input.end())); res && (int)res.size() > (maxEnd-start))")
            TB();TB();TB();TB();LN("{")
            TB();TB();TB();TB();TB();LN("maxEnd = start + res.size();")
            i = 0
            for r in lexer.rulesPerState[s]:
                i += 1
                TB();TB();TB();TB();TB();LN("if (const auto& subRes = res.get<" + str(i) + ">(); subRes && subRes.size() == res.size()) "+"choosenRuleInd = " + str(i) + ";")
            TB();TB();TB();TB();LN("}")

        else:
            i = 0
            for r in lexer.rulesPerState[s]:
                i += 1
                TB();TB();TB();TB();LN("if (auto res = ctre::starts_with<L\"(" + escapeRegexToC(r.regex) + ")\">(")
                TB();TB();TB();TB();TB();TB();LN("std::wstring_view(input).substr(start, input.size()-start)")
                TB();TB();TB();TB();TB();LN(");")
                TB();TB();TB();TB();TB();LN("res && (int)res.size() > (maxEnd-start)")
                TB();TB();TB();TB();LN(") {")
                TB();TB();TB();TB();TB();LN("choosenRuleInd = " + str(i) + ";")
                TB();TB();TB();TB();TB();LN("maxEnd = start + res.size();")
                TB();TB();TB();TB();LN("}")
             
        
        TB();TB();TB();TB();LN("")
        TB();TB();TB();TB();LN("// *** execute rule commands ***")
        TB();TB();TB();TB();LN("switch (choosenRuleInd)")
        TB();TB();TB();TB();LN("{")
        i = 0
        for r in lexer.rulesPerState[s]:
            i += 1
            TB();TB();TB();TB();LN("case " + str(i) + ":// " + escapeRegexToCComment(r.regex))
            hasOut = False
            hasStorestr = False
            for c in r.commands:
                if c.name == "out":
                    hasOut = True
                if c.name == "storeString":
                    hasStorestr = True
            for c in r.commands:
                if c.name == "out":
                    if hasStorestr:
                        TB();TB();TB();TB();TB();LN("ret.push_back(Token(TokenType::" + c.arg + ", input.substr(start, maxEnd-start), line, character));")
                    else:
                        TB();TB();TB();TB();TB();LN("ret.push_back(Token(TokenType::" + c.arg + ", line, character));")
                    #TB();TB();TB();TB();TB();LN("std::cout << \"token: " + c.arg + "\" << std::endl;")
                elif c.name == "push":
                    TB();TB();TB();TB();TB();LN("states.push_back(LexerState::" + c.arg + ");")
                elif c.name == "pop":
                    TB();TB();TB();TB();TB();LN("states.pop_back();")
                elif c.name == "swap":
                    TB();TB();TB();TB();TB();LN("states.pop_back();")
                elif c.name == "throw":
                    TB();TB();TB();TB();TB();LN("movePtr = false;")
            TB();TB();TB();TB();TB();LN("break;")
        TB();TB();TB();TB();LN("default:")
        TB();TB();TB();TB();LN("{")
        TB();TB();TB();TB();TB();LN("maxEnd = start+1;")
        TB();TB();TB();TB();TB();LN("movePtr = true;")
        TB();TB();TB();TB();TB();LN("std::wstringstream ss;")
        TB();TB();TB();TB();TB();LN("ss << \"Unexpected character '\" << input[start] << \"'\";")
        TB();TB();TB();TB();TB();LN("outErrors.emplace_back(line, character, ss.str());")
        TB();TB();TB();TB();LN("}")
        TB();TB();TB();TB();LN("}")
        TB();TB();TB();TB();LN("break;")
    TB();TB();TB();LN("}")
    
        
    TB();TB();TB();LN("")
    TB();TB();TB();LN("// *** count lines/positions ***")
    TB();TB();TB();LN("for (int i=start; i<maxEnd; i++)")
    TB();TB();TB();LN("{")
    TB();TB();TB();TB();LN("if (input[i] == '\\n')")
    TB();TB();TB();TB();LN("{")
    TB();TB();TB();TB();TB();LN("line++;")
    TB();TB();TB();TB();TB();LN("character = 0;")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();TB();LN("character++;")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("")
    TB();TB();TB();LN("// *** move pointer ***")
    TB();TB();TB();LN("if (movePtr) {")
    TB();TB();TB();TB();LN("start = maxEnd;")
    TB();TB();TB();TB();LN("maxEnd = -1;")
    TB();TB();TB();LN("}")
    TB();TB();LN("}")
    TB();TB();LN("")
    TB();TB();LN("ret.push_back(Token(TokenType::END_OF_STR, line, character));")
    TB();TB();LN("return ret;")
    TB();LN("}")
    LN("")
    LN("}")

    f.close()