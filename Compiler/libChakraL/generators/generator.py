from __future__ import annotations
import sys
from lexerGen import *
from parserGenShared import *
from semanticMethodGen import *
from parserGenCustom import *
from parserGenRecursive import *
from operatorProdGen import *
import time

class ArgumentError(Exception):
    def __init__(self, name: str):
        self.message = "Command requires " + name + " as an argument."

def main():
    # --inoperators <txt file> ... Operator table file
    # --outoperators <txt file> ... File to write operator expression productions to
    # --inlexer <txt file> ... Lexer definitions file
    # --inparser <txt file> ... Parser productions file
    # --outlexerh <h file> ... Lexer header file to write to
    # --outlexercpp <cpp file> ... Lexer c++ file to write to
    # --outparserh <h file> ... Parser header file to write to
    # --outparsercpp <cpp file> ... Parser c++ file to write to
    # --outsemanticnodescpp <cpp file> ... C++ file to write semantic node processor methods to
    # --extraparserheaders <file1> <file2> ... Header files to be included with the parser header file
    # --extrasemanticnodesheaders <file1> <file2> ... Header files to be included with the semantic node processor methods header file

    argMap: dict[str, list[str]] = {}
    curArg = ""

    parserTypeHeaderGens = {
        "custom": writeCustomParserH,
        "recursive": writeRecursiveParserH
    }
    parserTypeCPPGens = {
        "custom": writeCustomParserCPP,
        "recursive": writeRecursiveParserCPP
    }

    def argsgetopt(*names):
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
        
        return []

    def argsget(*names):
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

    def argget(*names):
        return argsget(*names)[0]

    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg[0:2] == "--":
            curArg = arg
            argMap[curArg] = []
        else:
            argMap[curArg].append(arg)
    
    try:
        semNodes : OrderedDict[str, SemanticNode] = OrderedDict()

        if "--outoperators" in argMap:
            startTime = time.time()
            outputOperatorProductions(argget("--inoperators"), argget("--outoperators"))
            print("Generated operator productions file in " + str(time.time()-startTime) + "s: " + argget("--outoperators"))
        if "--inlexer" in argMap:
            startTime = time.time()
            lex = loadLexer(argget("--inlexer"))
            print("Loaded lexer in " + str(time.time()-startTime) + "s: " + argget("--inlexer"))
        if "--inparser" in argMap:
            startTime = time.time()
            argget("--inlexer")
            pars = loadParser(lex, argget("--inparser"))
            semNodes.update(pars.semNodes)
            print("Loaded parser in " + str(time.time()-startTime) + "s: " + argget("--inparser"))
        if "--insemanticnodes" in argMap:
            startTime = time.time()
            semNodes.update(loadSemanticNodes(argget("--insemanticnodes")))
            print("Loaded sematic nodes in " + str(time.time()-startTime) + "s: " + argget("--insemanticnodes"))
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

            parsertype = argget("--parsertype")
            writeFuncH = parserTypeHeaderGens[parsertype]

            argget("--inparser")
            writeFuncH(pars, argget("--outparserh"), argget("--inlexerh", "--outlexerh"), argsgetopt("--extraparserheaders"))
            print("Generated parser header file in " + str(time.time()-startTime) + "s: " + argget("--outparserh"))
        if "--outparsercpp" in argMap:
            startTime = time.time()

            parsertype = argget("--parsertype")
            writeFuncCPP = parserTypeCPPGens[parsertype]

            argget("--inparser")
            writeFuncCPP(pars, argget("--outparsercpp"), argget("--inparserh", "--outparserh"), [])
            print("Generated parser source file in " + str(time.time()-startTime) + "s: " + argget("--outparsercpp"))
        if "--outsemanticnodesh" in argMap:
            startTime = time.time()
            argget("--insemanticnodes", "--inparser")
            writeSemanticNodesMethodsH(semNodes, argget("--outsemanticnodesh"), argget("--inparserh", "--outparserh"), argsgetopt("--extrasemanticnodesheaders"))
            print("Generated parser process definitions source file in " + str(time.time()-startTime) + "s: " + argget("--outsemanticnodesh"))
        if "--outsemanticnodescpp" in argMap:
            startTime = time.time()
            argget("--insemanticnodes", "--inparser")
            writeSemanticNodesMethodsCPP(semNodes, argget("--outsemanticnodescpp"), argget("--inparserh", "--outparserh"), argsgetopt("--extrasemanticnodesheaders"))
            print("Generated parser process definitions source file in " + str(time.time()-startTime) + "s: " + argget("--outsemanticnodescpp"))
    except ArgumentError as e:
        print("Error: " + e.message)
        return 1

main()