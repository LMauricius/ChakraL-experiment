import os
import re
from enum import Enum
from typing import Iterator
from genUtil import *
from lexerGen import *

class RepeatType(Enum):
    Optional = 0
    Single = 1
    SingleOrMore = 2
    ZeroOrMore = 3

class ProductionType(Enum):
    Token = 0
    Node = 1
    SubProd = 2

class ProductionPart:
    def __init__(self, idName: str, hint: str, variable: str, symbol: str, type: ProductionType):
        self.idName = idName
        self.hint = hint
        self.variable = variable
        self.symbol = symbol
        self.possibilities = list[list[ProductionPart]]()
        self.type = type
        self.repeatCount = -1

class ParseNode:
    def __init__(self, name: str):
        self.name = name
        self.possibilities = list[list[ProductionPart]]()
        self.partCounter = 1

class Parser:
    def __init__(self):
        self.startNode = ""
        self.nodes = dict[str, ParseNode]()
        self.productionParts = list[ProductionPart]()

def iterProductionPartsPoss(possibilities : list[list[ProductionPart]]) -> Iterator[ProductionPart]:
    for poss in possibilities:
        for part in poss:
            yield part
            if part.type == ProductionType.SubProd:
                yield from iterProductionPartsPoss(part.possibilities)

def iterProductionParts(node : ParseNode) -> Iterator[ProductionPart]:
    #print(node.possibilities)
    yield from iterProductionPartsPoss(node.possibilities)


def iterParserLine(line : str) -> Iterator[str]:
    subStr = ""
    subStrStartPos = 0
    pos = 0
    insideQuotes = False
    insideEscape = False

    for c in line:
        pos += 1
        if insideQuotes:
            subStr += c
            insideEscape = False
            if c == "\\":
                insideEscape = True
            elif c == "\'" and not insideEscape:
                insideQuotes = False
        elif c == '=' or c == '(' or c == ')' or c == '[' or c == ']' or c == '|' or c == '+' or c == '*' or c == '?':
            if len(subStr) > 0:
                yield subStr, subStrStartPos
            yield c, subStrStartPos
            subStr = ""
            subStrStartPos = pos
        elif c == ' ' or c == '\t':
            if len(subStr) > 0:
                yield subStr, subStrStartPos
            subStr = ""
            subStrStartPos = pos
        else:
            subStr += c
            if c == "\'":
                insideQuotes = True

    if len(subStr) > 0:
        yield subStr, subStrStartPos

# Yes.
def parseParserFileParseNodeProduction(lineInd: int, lexer: Lexer, counterNode: ParseNode, target: list[list[ProductionPart]], parserIt: Iterator[str], fullLine: str, stopStr: str):
    curOption = []
    curStr = ""
    curStrPos = 0
    curPart = None

    def curPartName():
        return counterNode.name + "_" + str(counterNode.partCounter)

    def curPartHint():
        if fullLine[0] == '=':
            return counterNode.name + " " +fullLine[0:curStrPos] + "_ " + fullLine[curStrPos:]
        else:
            return fullLine[0:curStrPos] + "_ " + fullLine[curStrPos:]

    try:
        curStr, curStrPos = next(parserIt, ("",0))
        while curStr != stopStr:
            #print("'"+curStr+"'")
            if curStr == '|':
                #print("Option:", curOption)
                target.append(curOption)
                curOption = []
            elif curStr == '(':
                curPart = ProductionPart(curPartName(), curPartHint(), "", "", ProductionType.SubProd)
                counterNode.partCounter += 1
                curOption.append(curPart)
                parseParserFileParseNodeProduction(lineInd, lexer, counterNode, curPart.possibilities, parserIt, fullLine, ')')
            elif curStr == '[':
                curPart = ProductionPart(curPartName(), curPartHint(), "", "", ProductionType.SubProd)
                counterNode.partCounter += 1
                curPart.repeatCount = RepeatType.Optional
                curOption.append(curPart)
                parseParserFileParseNodeProduction(lineInd, lexer, counterNode, curPart.possibilities, parserIt, fullLine, ']')
                curPart = None
            elif curStr == '+':
                if curPart == None:
                    raise FormatError("Error at '+'; must follow a symbol or sequence", lineInd)
                curPart.repeatCount = RepeatType.SingleOrMore
                curPart = None
            elif curStr == '*':
                if curPart == None:
                    raise FormatError("Error at '*'; must follow a symbol or sequence", lineInd)
                curPart.repeatCount = RepeatType.ZeroOrMore
                curPart = None
            elif curStr == '?':
                if curPart == None:
                    raise FormatError("Error at '?'; must follow a symbol or sequence", lineInd)
                curPart.repeatCount = RepeatType.Optional
                curPart = None
            elif curStr == ']' or curStr == ')':
                raise FormatError("Unexpected closing bracket " + curStr, lineInd)
            else:
                curPart = ProductionPart(curPartName(), curPartHint(), "", "", ProductionType.SubProd)
                counterNode.partCounter += 1

                if curStr[0] == '<':
                    if curStr[-1] != '>':
                        raise FormatError("Expected a '>'", lineInd)
                        
                    # argument
                    semicInd = curStr.find(':', 1)
                    if semicInd != -1:
                        curPart.variable = curStr[1:semicInd]
                        if curPart.variable == "":# the prefix was only a semicolon
                            curPart.variable = ":"
                    else:
                        semicInd = 0

                    # store vals
                    curPart.symbol = curStr[semicInd+1:-1]
                    curPart.type = ProductionType.Node
                else:
                    curPart.type = ProductionType.Token

                    # quoted lexemes
                    if "\'" in curStr:
                        if curStr[-1] != '\'':
                            raise FormatError("Expected a '\\''", lineInd)

                        # find quote
                        startQ = curStr.find("\'")+1
                        endQ = len(curStr)-1
                        qStr = unescapeString(curStr[startQ : endQ])
                        #print(curStr, qStr)

                        # find corresponding lexeme
                        lexeme = ""
                        #print((qStr))
                        for regexTokenPair in lexer.regexTokenPairs:
                            if re.match("^"+regexTokenPair[0]+"$", qStr, re.M):
                                lexeme = regexTokenPair[1]
                                break
                        if len(lexeme) == 0:
                            raise FormatError("Don't know what '" + safeStrConvert(qStr) + "' is", lineInd)
                        curPart.symbol = lexeme

                        # argument
                        semicInd = curStr.find(':', 1)
                        if semicInd != -1 and semicInd < startQ:
                            curPart.variable = curStr[1:semicInd]
                            if curPart.variable == "":
                                raise FormatError("Lexemes can't have only semicolons for prefix", lineInd)

                    # non quoted lexemes
                    else:
                        # argument
                        semicInd = curStr.find(':', 1)
                        if semicInd != -1:
                            curPart.variable = curStr[0:semicInd]
                        else:
                            semicInd = 0

                        # store symbol
                        curPart.symbol = curStr[semicInd+1:]
                    
                curOption.append(curPart)
                #print(lineInd, curPart.variable, curPart.symbol,  "- "+curStr+"")


            curStr, curStrPos = next(parserIt, ("",0))

        #print("Option:", curOption)
        target.append(curOption)
        curOption = []

    except StopIteration:
        #print("Option:", curOption)
        target.append(curOption)
        curOption = []
        raise


def loadParser(lexer: Lexer, filename: str):
    print("...Loading parser ", filename)

    lines = meaningfulLines(filename)
    parser = Parser()
    curNodeName = ""

    try:
        lineInd = 0
        l, lineInd = next(lines, ("",-1))
        while len(l):
            #print("...Line ", l)

            parserIt = iterParserLine(l)
            try:
                subStrPos = 0
                substr, subStrPos = next(parserIt, ("",0))

                # left side of production
                if substr != '=':
                    curNodeName = substr
                    substr, subStrPos = next(parserIt, ("",0))
                    if substr != '=':
                        raise FormatError("Expected a '=', got '"+substr+"'", lineInd)
            except StopIteration:
                raise FormatError("Expected a '=' or a node name, got nothing", lineInd)

            # check if node exists
            if not curNodeName in parser.nodes:
                parser.nodes[curNodeName] = ParseNode(curNodeName)
            curNode = parser.nodes[curNodeName]
            
            # add production
            try:
                parseParserFileParseNodeProduction(lineInd, lexer, curNode, curNode.possibilities, parserIt, l, "")
            except StopIteration:
                pass

            l, lineInd = next(lines, ("",-1))
    except FormatError as e:
        print("At line " + str(e.lineInd) + ": " + e.message)
    except StopIteration:
        pass
    
    for name, node in parser.nodes.items():
        #print(name, node)
        for part in iterProductionParts(node):
            parser.productionParts.append(part)
    
    return parser




def writeParserH(parser: Parser, filename: str, lexerHeaderfile: str):
    print("...Writing parser ", filename)
    f = open(filename, "wt")

    def TB():
        f.write('    ')
    def LN(s: str):
        f.write(s)
        f.write('\n')

    LN("// This file is autogenerated. Do not edit!")
    LN("")
    LN('#include <list>')
    LN('#include <string>')
    LN('#include <map>')
    LN('#include <memory>')
    LN('#include "' + os.path.basename(lexerHeaderfile) + '"')
    LN("")
    LN("namespace ChakraL {")
    LN("")
    TB();LN("class ParseNode {")
    TB();LN("public:")
    TB();TB();LN("virtual void process();")
    TB();TB();LN("void appendMove(ParseNode& other);")
    TB();TB();LN("")
    TB();TB();LN("std::map<std::string, std::list<std::unique_ptr<ParseNode>>> nodeLists;")
    TB();TB();LN("std::map<std::string, std::list<Token>> tokenLists;")
    TB();LN("};")
    for name, node in parser.nodes.items():
        LN("")
        TB();LN("class ParseNode_" + name + " : public ParseNode {")
        TB();LN("public:")
        TB();TB();LN("void process();")
        TB();LN("};")
    LN("")
    LN("")
    TB();LN("// State utils")
    TB();LN("struct StateData;")
    TB();LN("struct State;")
    TB();LN("struct ParserBranch;")
    TB();LN("struct ParserData;")
    TB();LN("")
    TB();LN("struct StateData {")
    TB();TB();LN("ParseNode* node;")
    TB();LN("};")
    TB();LN("")
    TB();LN("struct State {")
    TB();TB();LN("// returns whether the state branches")
    TB();TB();LN("bool (*stateHandler)(ParserData& parserData, ParserBranch& branch);")
    TB();TB();LN("")
    TB();TB();LN("StateData data;")
    TB();LN("};")
    TB();LN("")
    TB();LN("struct ParserBranch {")
    TB();TB();LN("std::vector<State> stack;")
    TB();TB();LN("ParserBranch* parent;")
    TB();TB();LN("size_t branchCount=0;")
    TB();LN("};")
    TB();LN("")
    TB();LN("struct ParserData {")
    TB();TB();LN("std::list<ParserBranch> activeBranches;")
    TB();TB();LN("std::list<ParserBranch> ambiguousBranches;")
    TB();LN("};")
    LN("")
    LN("}")

    f.close()


def writeParserCPP(parser: Parser, filename: str, headerfile: str):
    print("...Writing parser ", filename)
    f = open(filename, "wt")

    def TB():
        f.write('    ')
    def LN(s: str):
        f.write(s)
        f.write('\n')

    LN("// This file is autogenerated. Do not edit!")
    LN("")
    LN('#include "' + os.path.basename(headerfile) + '"')
    
    LN('#include <vector>')
    LN('#include <string_view>')
    LN('#include <regex>')
    LN("")
    LN("namespace ChakraL")
    LN("{")
    LN("")
    TB();LN("void ParseNode::process() {")
    TB();LN("};")
    TB();LN("")
    TB();LN("void ParseNode::appendMove(ParseNode& other) {")
    TB();TB();LN("for (auto& varNodesPair : other.nodeLists) {")
    TB();TB();TB();LN("const std::string &varName = varNodesPair.first;")
    TB();TB();TB();LN("auto &otherList = varNodesPair.second;")
    TB();TB();TB();LN("auto &myList = nodeLists[varName];")
    TB();TB();TB();LN("myList.splice(otherList.begin(), otherList);")
    TB();TB();LN("}")
    TB();TB();LN("for (auto& varTokensPair : other.tokenLists) {")
    TB();TB();TB();LN("const std::string &varName = varTokensPair.first;")
    TB();TB();TB();LN("auto &otherList = varTokensPair.second;")
    TB();TB();TB();LN("auto &myList = tokenLists[varName];")
    TB();TB();TB();LN("otherList.splice(myList.begin(), myList);")
    TB();TB();LN("}")
    TB();LN("};")
    TB();LN("")
    for part in parser.productionParts:
        TB();LN("void h_" + part.idName + "(ParserData& parserData, ParserBranch& branch);")
    for part in parser.productionParts:
        LN("")
        TB();LN("// " + part.hint)
        TB();LN("void h_" + part.idName + "(ParserData& parserData, ParserBranch& branch) {")
        # Now do all the checking, depending on the type of production part
        TB();LN("}")
    LN("")
    LN("}")

    f.close()