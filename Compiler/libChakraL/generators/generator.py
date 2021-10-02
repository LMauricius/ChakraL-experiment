from __future__ import annotations
import sys
from lexerGen import *
from parserGen import *
from parserExprGen import *
import time

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
            startTime = time.time()
            outputExprProductions(argget("--inoperators"), argget("--outoperators"))
            print("Generated operator productions file in " + str(time.time()-startTime) + "s: " + argget("--outoperators"))
        if "--inlexer" in argMap:
            startTime = time.time()
            lex = loadLexer(argget("--inlexer"))
            print("Loaded lexer in " + str(time.time()-startTime) + "s: " + argget("--inlexer"))
        if "--inparser" in argMap:
            startTime = time.time()
            argget("--inlexer")
            pars = loadParser(lex, argget("--inparser"))
            print("Loaded parser in " + str(time.time()-startTime) + "s: " + argget("--inparser"))
        if "--outlexerh" in argMap:
            startTime = time.time()
            argget("--inlexer")
            writeLexerH(lex, argget("--outlexerh"))
            print("Generated lexer header file in " + str(time.time()-startTime) + "s: " + argget("--outlexerh"))
        if "--outlexercpp" in argMap:
            startTime = time.time()
            argget("--inlexer")
            writeLexerCPP(lex, argget("--outlexercpp"), argget("--inlexerh", "--outlexerh"), ("--useSingleDFA" in argMap))
            print("Generated lexer source file in " + str(time.time()-startTime) + "s: " + argget("--outlexercpp"))
        if "--outparserh" in argMap:
            startTime = time.time()
            argget("--inparser")
            writeParserH(pars, argget("--outparserh"), argget("--inlexerh", "--outlexerh"))
            print("Generated parser header file in " + str(time.time()-startTime) + "s: " + argget("--outparserh"))
        if "--outparsercpp" in argMap:
            startTime = time.time()
            argget("--inparser")
            writeParserCPP(pars, argget("--outparsercpp"), argget("--inparserh", "--outparserh"))
            print("Generated parser source file in " + str(time.time()-startTime) + "s: " + argget("--outparsercpp"))
        if "--outparserprocesscpp" in argMap:
            startTime = time.time()
            argget("--inparser")
            writeParserProcessCPP(pars, argget("--outparserprocesscpp"), argget("--inparserh", "--outparserh"))
            print("Generated parser process definitions source file in " + str(time.time()-startTime) + "s: " + argget("--outparserprocesscpp"))
    except ArgumentError as e:
        print("Error: " + e.message)
        return 1

main()