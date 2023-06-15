from __future__ import annotations
import sys
from lexerGen import *
from regexMacroGen import outputUnicodeMacros
from parserGenShared import *
from semanticMethodGen import *
from parserGenCustom import *
from parserGenRecursive import *
from operatorProdGen import *
from syntaxDocGen import outputSyntaxDoc
import time

class ArgumentError(Exception):
    def __init__(self, name: str):
        self.message = "Command requires " + name + " as an argument."

def main():
    # --inregexmacro <txt file> ... posix regex bracket expressions
    # --outunicoderegex <txt file> ... File to write unicode general categories as posix regex bracket expressions to
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
    # --extrasemanticinclheaders <file1> <file2> ... Header files to be included with the semantic node processor methods header file
    # --extrasemanticimplheaders <file1> <file2> ... Header files to be included with the semantic node processor methods cpp file
    # --outsyntaxdoc <file prefix> ... Syntax documentation files to write to
    # --syntaxdocexpand [keywords] [productions] [options] [subproductions] ... which parts to expand

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
    regexmacros: dict[str, str] = {}

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

        if "--inregexmacro" in argMap:
            startTime = time.time()
            for filename in argsget("--inregexmacro"):
                with open(filename) as file:
                    lines = file.readlines()
                    for ind in range(0, len(lines), 2):
                        regexmacros[lines[ind].strip()] = lines[ind+1].strip()
                        #print(f";;;;;{lines[ind].strip()} {lines[ind+1].strip()}")
            print("Loaded regex macro in " + str(time.time()-startTime) + "s: " + str(argsget("--inregexmacro")))
        if "--outunicoderegex" in argMap:
            startTime = time.time()
            outputUnicodeMacros(argget("--outunicoderegex"))
            print("Generated unicode regex file in " + str(time.time()-startTime) + "s: " + argget("--outunicoderegex"))
        if "--outoperators" in argMap:
            startTime = time.time()
            outputOperatorProductions(argget("--inoperators"), argget("--outoperators"))
            print("Generated operator productions file in " + str(time.time()-startTime) + "s: " + argget("--outoperators"))
        if "--inlexer" in argMap:
            startTime = time.time()
            lexer = loadLexer(argget("--inlexer"), regexmacros)
            print("Loaded lexer in " + str(time.time()-startTime) + "s: " + argget("--inlexer"))
        if "--insemanticnodes" in argMap:
            startTime = time.time()

            semNodes = loadSemanticNodes(argget("--insemanticnodes"))
            '''for name, node in loadSemanticNodes(argget("--insemanticnodes")).items():
                semNodes.setdefault(name, SemanticNode())
                semNodes[name].methods.update(node.methods)
                semNodes[name].privateMembers.update(node.privateMembers)
                semNodes[name].protectedMembers.update(node.protectedMembers)
                semNodes[name].publicMembers.update(node.publicMembers)'''
            print("Loaded semantic nodes in " + str(time.time()-startTime) + "s: " + argget("--insemanticnodes"))
        if "--inparser" in argMap:
            startTime = time.time()
            argget("--inlexer")
            parser = loadParser(lexer, argget("--inparser"), semNodes)

            semNodes = parser.semNodes
            '''for name, node in pars.semNodes.items():
                semNodes.setdefault(name, SemanticNode())
                semNodes[name].methods.update(node.methods)
                semNodes[name].privateMembers.update(node.privateMembers)
                semNodes[name].protectedMembers.update(node.protectedMembers)
                semNodes[name].publicMembers.update(node.publicMembers)'''

            print("Loaded parser in " + str(time.time()-startTime) + "s: " + argget("--inparser"))

            print("Loaded sematic nodes in " + str(time.time()-startTime) + "s: " + argget("--insemanticnodes"))
        if "--outlexerh" in argMap:
            startTime = time.time()
            argget("--inlexer")
            writeLexerH(lexer, argget("--outlexerh"))
            print("Generated lexer header file in " + str(time.time()-startTime) + "s: " + argget("--outlexerh"))
        if "--outlexercpp" in argMap:
            startTime = time.time()
            argget("--inlexer")
            writeLexerCPP(lexer, argget("--outlexercpp"), argget("--inlexerh", "--outlexerh"), ("--useSingleDFA" in argMap))
            print("Generated lexer source file in " + str(time.time()-startTime) + "s: " + argget("--outlexercpp"))
        if "--outparserh" in argMap:
            startTime = time.time()

            parsertype = argget("--parsertype")
            writeFuncH = parserTypeHeaderGens[parsertype]

            argget("--inparser")
            writeFuncH(parser, argget("--outparserh"), argget("--inlexerh", "--outlexerh"), argsgetopt("--extraparserheaders"))
            print("Generated parser header file in " + str(time.time()-startTime) + "s: " + argget("--outparserh"))
        if "--outparsercpp" in argMap:
            startTime = time.time()

            parsertype = argget("--parsertype")
            writeFuncCPP = parserTypeCPPGens[parsertype]

            argget("--inparser")
            writeFuncCPP(parser, argget("--outparsercpp"), argget("--inparserh", "--outparserh"), [])
            print("Generated parser source file in " + str(time.time()-startTime) + "s: " + argget("--outparsercpp"))
        if "--outsemanticnodesh" in argMap:
            startTime = time.time()
            argget("--insemanticnodes", "--inparser")
            writeSemanticNodesMethodsH(semNodes, argget("--outsemanticnodesh"), argget("--inlexerh", "--outlexerh"), argsgetopt("--extrasemanticinclheaders"))
            print("Generated parser process definitions source file in " + str(time.time()-startTime) + "s: " + argget("--outsemanticnodesh"))
        if "--outsemanticnodescpp" in argMap:
            startTime = time.time()
            argget("--insemanticnodes", "--inparser")
            writeSemanticNodesMethodsCPP(semNodes, argget("--outsemanticnodescpp"), argget("--insemanticnodesh", "--outsemanticnodesh"), argsgetopt("--extrasemanticimplheaders"))
            print("Generated parser process definitions source file in " + str(time.time()-startTime) + "s: " + argget("--outsemanticnodescpp"))

        if "--outsyntaxdoc" in argMap:
            startTime = time.time()
            argget("--inparser")
            outputSyntaxDoc(argget("--outsyntaxdoc"), lexer, parser, argsgetopt("--syntaxdocexpand"))
            print("Generated syntax documentation in " + str(time.time()-startTime) + "s: " + argget("--outsyntaxdoc"))

    except ArgumentError as e:
        print("ERROR: " + e.message)
        return 1

main()