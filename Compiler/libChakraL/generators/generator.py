import sys
from lexerGen import *
from parserGen import *
from parserExprGen import *

def main():
    # arg1 = definition folder
    # arg2 = header folder
    # arg3 = cpp folder

    outputExprProductions(sys.argv[1]+"operatorTable.txt", sys.argv[1]+"autoParserExpressions.txt")

    lex = loadLexer(sys.argv[1]+"lexer.txt")
    pars = loadParser(lex, sys.argv[1]+"parser.txt")

    writeLexerH(lex, sys.argv[2]+"chakralLexer.h")
    writeLexerCPP(lex, sys.argv[3]+"chakralLexer.cpp", sys.argv[2]+"chakralLexer.h")
    writeParserH(pars, sys.argv[2]+"chakralParser.h", sys.argv[2]+"chakralLexer.h")
    writeParserCPP(pars, sys.argv[3]+"chakralParser.cpp", sys.argv[2]+"chakralParser.h")

main()