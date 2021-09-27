from __future__ import annotations
import sys
from lexerGen import *
from parserGen import *
from parserExprGen import *

class ArgumentError(Exception):
    def __init__(self, name: str):
        self.message = "Command requires " + name + " as an argument."

def main():
    # arg1 = definition folder
    # arg2 = header folder
    # arg3 = cpp folder
    argMap: dict[str, str] = {}
    curArg = ""

    def argget(*names):
        for n in names:
            if n in argMap:
                return argMap[n]
        
        errname = ""
        if len(names) > 1:
            errname = "either "
            for i in range(0, len(names)):
                if i == len(names)-1:
                    errname += " or "
                else:
                    errname += ", "
                errname += names[i]
        else:
            errname = names[0]
        
        raise ArgumentError(errname)

    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg[0:2] == "--":
            curArg = arg
            argMap[curArg] = ""
        else:
            argMap[curArg] = arg
    
    try:
        if "--outoperators" in argMap:
            outputExprProductions(argget("--inoperators"), argget("--outoperators"))
            print("Generated operator productions file: " + argget("--outoperators"))
        if "--inlexer" in argMap:
            lex = loadLexer(argget("--inlexer"))
        if "--inparser" in argMap:
            argget("--inlexer")
            pars = loadParser(lex, argget("--inparser"))
        if "--outlexerh" in argMap:
            argget("--inlexer")
            writeLexerH(lex, argget("--outlexerh"))
            print("Generated lexer header file: " + argget("--outlexerh"))
        if "--outlexercpp" in argMap:
            argget("--inlexer")
            writeLexerCPP(lex, argget("--outlexercpp"), argget("--inlexerh", "--outlexerh"), ("--useSingleDFA" in argMap))
            print("Generated lexer source file: " + argget("--outlexercpp"))
        if "--outparserh" in argMap:
            argget("--inparser")
            writeParserH(pars, argget("--outparserh"), argget("--inlexerh", "--outlexerh"))
            print("Generated parser header file: " + argget("--outparserh"))
        if "--outparsercpp" in argMap:
            argget("--inparser")
            writeParserCPP(pars, argget("--outparsercpp"), argget("--inparserh", "--outparserh"))
            print("Generated parser source file: " + argget("--outparsercpp"))
        if "--outparserprocesscpp" in argMap:
            argget("--inparser")
            writeParserProcessCPP(pars, argget("--outparserprocesscpp"), argget("--inparserh", "--outparserh"))
            print("Generated parser process definitions source file: " + argget("--outparserprocesscpp"))
    except ArgumentError as e:
        print("Error: " + e.message)
        return 1
        

    '''
    outputExprProductions(sys.argv[1]+"operatorTable.txt", sys.argv[1]+"autogeneratedParserExpressions.txt")

    lex = loadLexer(sys.argv[1]+"lexer.txt")
    pars = loadParser(lex, sys.argv[1]+"parser.txt")

    writeLexerH(lex, sys.argv[2]+"chakralLexer.h")
    writeLexerCPP(lex, sys.argv[3]+"chakralLexer.cpp", sys.argv[2]+"chakralLexer.h")
    writeParserH(pars, sys.argv[2]+"chakralParser.h", sys.argv[2]+"chakralLexer.h")
    writeParserCPP(pars, sys.argv[3]+"chakralParser.cpp", sys.argv[2]+"chakralParser.h")
    '''

main()