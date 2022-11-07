from __future__ import annotations
import os
import re
from enum import Enum
from typing import Iterator, List, OrderedDict
from genUtil import *
from lexerGen import *
from semanticMethodGen import *
import time

from semanticMethodGen import SemanticNode
from semanticMethodGen import Member
from semanticMethodGen import semNodeExtends

NO_OUTPUT_PRODUCTION_STR = "-"
FALTHRU_OUTPUT_PRODUCTION_STR = "::"
FALTHRU_VARIABLE_STR = "."
LIST_VARIABLE_SUFFIX = ":"
ERROR_HELPER_STR_ASSERTIVE = "!"
ERROR_HELPER_STR_SYNC = "$"

class RepeatType(Enum):
    Optional = 0
    Single = 1
    SingleOrMore = 2
    ZeroOrMore = 3

class ProductionType(Enum):
    Token = 0
    Node = 1
    SubProd = 2

class StateType(Enum):
    Token = 0
    Node = 1
    Proxy = 2
    Branch = 3

class ProductionPart:
    def __init__(self, idName: str, hint: str, location: Location, variable: str, symbol: str, type: ProductionType, prodName: str, errorHelpers : List[str], isMainPart: bool = False):
        self.idName = idName
        self.hint = hint
        self.location = copy.copy(location)
        self.variable = variable
        self.variableIsList = None
        self.symbol = symbol
        self.possibilities: list[list[ProductionPart]] = []
        self.type = type
        self.isMainPart = isMainPart
        self.prodName = prodName
        self.errorHelpers = errorHelpers
        self.repeatCount : RepeatType = RepeatType.Single
        self.nextStateName: str = ""# used in custom parser type

class ParserState:
    def __init__(self, name: str, hint: str, type: StateType, semNodeName: str):
        self.name = name
        self.hint = hint
        self.variable: str = None
        self.symbol: str = None
        self.type = type
        self.semNodeName = semNodeName
        self.nextState: ParserState = None
        self.branchStart: ParserState = None
        self.proxyForStates: list[ParserState] = []

class Production:
    def __init__(self, name: str, location: Location):
        self.name = name
        self.outSemNodeName = name
        self.visibleSemNodeName = name
        self.mainPart = ProductionPart(name, name, location, "<>", "<>", ProductionType.SubProd, name, [], True)
        self.startingParserState : ParserState = None
        self.partCounter = 1

class Parser:
    def __init__(self):
        self.startProduction = ""
        self.productions: dict[str, Production] = {}
        #self.semNodeNames: set[str] = set()
        self.parserStates: list[ParserState] = []
        self.productionParts: list[ProductionPart] = []
        self.semNodes : OrderedDict[str, SemanticNode] = OrderedDict()

def detectAndMarkRecursions(poss : list[ProductionPart], nodeName: str):
    poss.isRecursive = None

    if len(poss) > 0:
        part = poss[0]

        if part.type == ProductionType.Token:
            poss.isRecursive = False
        elif part.type == ProductionType.Node:
            poss.isRecursive = (part.symbol == nodeName)
        elif part.type == ProductionType.SubProd:
            for subPoss in part.possibilities:
                detectAndMarkRecursions(subPoss, nodeName)
                if subPoss.isRecursive:
                    poss.isRecursive = True
    else:
        poss.isRecursive = False

def detectRecursionsAndCrash(part : ProductionPart, path, visited: set[Production], parser: Parser, nodeName: str):
    if part.type == ProductionType.Token:
        pass
    elif part.type == ProductionType.Node:
        if not part.symbol in parser.productions:
            raise SemanticError(f"node '{part.symbol}' used at <<{part.hint}>> but not defined", part.location)
        node = parser.productions[part.symbol]
        if not node in visited:
            visited.add(node)

            if part.symbol in path:
                pass# this is a recursion, but will be more precisely blamed later
            elif part.symbol == nodeName:
                pathStr = str(path)
                pathStr.replace("(", "")
                pathStr.replace(")", "")
                pathStr.replace(",", "->")
                raise SemanticError(f"At node '{nodeName}': Detected recursion through nodes {pathStr}->*{nodeName}*")
            else:
                detectRecursionsAndCrash(node.mainPart, (path, part.symbol), visited, parser, nodeName)
    elif part.type == ProductionType.SubProd:
        for subPoss in part.possibilities:
            if len(subPoss) > 0:
                detectRecursionsAndCrash(subPoss[0], path, visited, parser, nodeName)

def hasRecursion(part : ProductionPart, nodeName: str, parser: Parser, visited: dict[Production, bool]) -> bool:
    if part.type == ProductionType.Token:
        pass
    elif part.type == ProductionType.Node:
        if not part.symbol in parser.productions:
            raise SemanticError(f"node '{part.symbol}' used at <<{part.hint}>> but not defined", part.location)
        node = parser.productions[part.symbol]

        if node in visited.keys():
            return visited[node]
        else:
            if part.symbol == nodeName:
                visited[node] = True
                return True
            else:
                visited[node] = hasRecursion(node.mainPart, nodeName, parser, visited)
                return visited[node]
    elif part.type == ProductionType.SubProd:
        for subPoss in part.possibilities:
            if len(subPoss) > 0:
                if hasRecursion(subPoss[0], nodeName, parser, visited):
                    return True
        return False

def hasUnavoidableReference(part : ProductionPart, nodeName: str, parser: Parser, visited: dict[Production, bool]) -> bool:
    if part.type == ProductionType.Token:
        pass
    elif part.type == ProductionType.Node:
        if not part.symbol in parser.productions:
            raise SemanticError(f"node '{part.symbol}' used at <<{part.hint}>> but not defined", part.location)
        node = parser.productions[part.symbol]

        if node in visited.keys():
            return visited[node]
        else:
            if part.symbol == nodeName:
                visited[node] = True
                return True
            else:
                visited[node] = hasUnavoidableReference(node.mainPart, nodeName, parser, visited)
                return visited[node]
    elif part.type == ProductionType.SubProd:
        ret = True
        for subPoss in part.possibilities:
            if len(subPoss) > 0:
                if not hasUnavoidableReference(subPoss[0], nodeName, parser, visited):
                    ret = False
                    break
        return ret

# Will be allowed
'''def detectForbiddenRecursionsAndCrash(poss : list[ProductionPart], nodeName: str):

    if len(poss) > 0:
        part = poss[0]

        if part.type == ProductionType.Token:
            pass
        elif part.type == ProductionType.Node:
            if part.symbol == nodeName and part.nodeName != nodeName:
                raise FormatError(f"Detected forbidden recursion through node '{part.nodeName}'", f"node '{nodeName}'")
            detectForbiddenRecursionsAndCrash()
        elif part.type == ProductionType.SubProd:
            for subPoss in part.possibilities:
                detectRecursionsAndCrash(subPoss, nodeName)
    else:
        poss.isRecursive = False'''

def extractParts(part : ProductionPart, outputList : list[ProductionPart]) -> None:
    if part.type == ProductionType.SubProd:
        for poss in part.possibilities:
            for subpart in poss:
                extractParts(subpart, outputList)
    outputList.append(part)

def convertToStates(part : ProductionPart, nextState: ParserState, parser: Parser, outParserStates: list[ParserState]):
    retState : ParserState = None# if retState == None, the newState will be stored in retState and returned
    storeState : ParserState = None# if storeState != None, the newState will be stored in storeState.branchStart instead of newState
    newState : ParserState = None

    #insertPos = len(outParserStates)
    def getSemNodeName(part : ProductionPart)->str:
        return parser.productions[part.prodName].outSemNodeName
    
    # = Manage repeating =
    if part.repeatCount == RepeatType.Single:
        pass
    elif part.repeatCount == RepeatType.Optional:
        selectState = ParserState(part.idName+"__select", part.hint, StateType.Proxy, getSemNodeName(part))
        outParserStates.append(selectState)

        if nextState is None or nextState.type == StateType.Branch:
            skipBranch = nextState
        else:
            skipBranch = ParserState(part.idName+"__cont", part.hint, StateType.Branch, getSemNodeName(part))
            outParserStates.append(skipBranch)
            skipBranch.branchStart = nextState

            #if part.idName+"__cont" == "a_valueLiteral_14__cont":
            #    print(skipBranch.branchStart)

        acceptBranch = ParserState(part.idName+f"__accept", part.hint, StateType.Branch, getSemNodeName(part))
        outParserStates.append(acceptBranch)
        storeState = acceptBranch
        
        selectState.proxyForStates = [skipBranch, acceptBranch]

        nextState = skipBranch
        retState = selectState
    elif part.repeatCount == RepeatType.ZeroOrMore:
        repeatState = ParserState(part.idName+"__repeat", part.hint, StateType.Proxy, getSemNodeName(part))
        outParserStates.append(repeatState)

        if nextState is None or nextState.type == StateType.Branch:
            skipBranch = nextState
        else:
            skipBranch = ParserState(part.idName+f"__cont", part.hint, StateType.Branch, getSemNodeName(part))
            outParserStates.append(skipBranch)
            skipBranch.branchStart = nextState

        cycleBranch = ParserState(part.idName+f"__cycle", part.hint, StateType.Branch, getSemNodeName(part))
        outParserStates.append(cycleBranch)
        storeState = cycleBranch
        
        repeatState.proxyForStates = [skipBranch, cycleBranch]

        nextState = repeatState
        retState = repeatState
    elif part.repeatCount == RepeatType.SingleOrMore:
        repeatState = ParserState(part.idName+"__repeat", part.hint, StateType.Proxy, getSemNodeName(part))
        outParserStates.append(repeatState)

        if nextState is None or nextState.type == StateType.Branch:
            skipBranch = nextState
        else:
            skipBranch = ParserState(part.idName+f"__cont", part.hint, StateType.Branch, getSemNodeName(part))
            outParserStates.append(skipBranch)
            skipBranch.branchStart = nextState

        cycleBranch = ParserState(part.idName+f"__cycle", part.hint, StateType.Branch, getSemNodeName(part))
        outParserStates.append(cycleBranch)
        storeState = cycleBranch
        
        repeatState.proxyForStates = [skipBranch, cycleBranch]

        nextState = repeatState
        retState = None # We want to directly enter the new state

    # = Create new state =
    if part.type == ProductionType.SubProd:
        if len(part.possibilities) > 1:
            newState = ParserState(part.idName, part.hint, StateType.Proxy, getSemNodeName(part))
            assert(newState is not None)
            outParserStates.append(newState)
            i = 1
            for poss in part.possibilities:
                if len(poss) > 0:
                    branch = ParserState(part.idName+f"__poss{i}", poss[0].hint, StateType.Branch, getSemNodeName(part))
                    outParserStates.append(branch)

                    insertInd = len(outParserStates)
                    tmpNextState = nextState
                    for subpart in reversed(poss):
                        tmpOutParserStates = []
                        subState = convertToStates(subpart, tmpNextState, parser, tmpOutParserStates)
                        assert(subState is not None)
                        tmpNextState = subState
                        outParserStates[insertInd:insertInd] = tmpOutParserStates

                    assert(tmpNextState is not None)
                    branch.branchStart = tmpNextState
                    newState.proxyForStates.append(branch)
                    i += 1
            assert(newState is not None)
        elif len(part.possibilities) == 1:
            poss = part.possibilities[0]
            assert(len(poss) > 0)
            if part.isMainPart:# main part must always branch
                branch = ParserState(part.idName, part.hint, StateType.Branch, getSemNodeName(part))
                outParserStates.append(branch)

                insertInd = len(outParserStates)
                tmpNextState = nextState
                for subpart in reversed(poss):
                    tmpOutParserStates = []
                    subState = convertToStates(subpart, tmpNextState, parser, tmpOutParserStates)
                    assert(subState is not None)
                    tmpNextState = subState
                    outParserStates[insertInd:insertInd] = tmpOutParserStates

                assert(tmpNextState is not None)
                branch.branchStart = tmpNextState
                newState = branch
                assert(newState is not None)
            else:
                insertInd = len(outParserStates)
                tmpNextState = nextState
                for subpart in reversed(poss):
                    tmpOutParserStates = []
                    subState = convertToStates(subpart, tmpNextState, parser, tmpOutParserStates)
                    tmpNextState = subState
                    outParserStates[insertInd:insertInd] = tmpOutParserStates

                assert(tmpNextState is not None)
                newState = tmpNextState
            assert(newState is not None)
        else:
            print("!!!ERROR")
            print(part.hint)
            print(part.idName)
            print(part.__dict__)
            print("!!!ENDERROR")
            assert(False)
        assert(newState is not None)

    elif part.type == ProductionType.Token:
        newState = ParserState(part.idName, part.hint, StateType.Token, getSemNodeName(part))
        outParserStates.append(newState)
        newState.variable = part.variable
        newState.symbol = part.symbol
        newState.nextState = nextState
        assert(newState is not None)
    elif part.type == ProductionType.Node:
        newState = ParserState(part.idName, part.hint, StateType.Node, getSemNodeName(part))
        outParserStates.append(newState)
        newState.variable = part.variable
        newState.symbol = part.symbol
        newState.nextState = nextState
        assert(newState is not None)
    else:
        assert(False)

    # = Store new state =
    if retState is None:
        assert(newState is not None)
        retState = newState
    if storeState is not None:
        assert(newState is not None)
        storeState.branchStart = newState
        
    # = Return states =
    assert(retState is not None)
    return retState


def iterParserLine(line : str) -> Iterator[str]:
    subStr = ""
    subStrStartPos = 0
    pos = 0
    insideQuotes = False
    quoteTerm = " "
    insideEscape = False

    for c in line:
        pos += 1
        if insideQuotes:
            subStr += c
            insideEscape = False
            if c == "\\":
                insideEscape = True
            elif c == quoteTerm and not insideEscape:
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
            if c == "\'" or c == "\"":
                insideQuotes = True
                quoteTerm = c

    if len(subStr) > 0:
        yield subStr, subStrStartPos

# Yes.
def parseParserFileParseNodeProduction(location: Location, lexer: Lexer, counterNode: Production, target: list[list[ProductionPart]], parserIt: Iterator[str], fullLine: str, stopStr: str):
    curOption = []
    curStr = ""
    curStrPos = 0
    curPart = None
    curErrorHelpers = []

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
                curPart = ProductionPart(curPartName(), curPartHint(), location, "", "", ProductionType.SubProd, counterNode.name, curErrorHelpers)
                curErrorHelpers = []
                counterNode.partCounter += 1
                curOption.append(curPart)
                parseParserFileParseNodeProduction(location, lexer, counterNode, curPart.possibilities, parserIt, fullLine, ')')
            elif curStr == '[':
                curPart = ProductionPart(curPartName(), curPartHint(), location, "", "", ProductionType.SubProd, counterNode.name, curErrorHelpers)
                curErrorHelpers = []
                counterNode.partCounter += 1
                curPart.repeatCount = RepeatType.Optional
                curOption.append(curPart)
                parseParserFileParseNodeProduction(location, lexer, counterNode, curPart.possibilities, parserIt, fullLine, ']')
                curPart = None
            elif curStr == '+':
                if curPart == None:
                    raise FormatError("Error at '+'; must follow a symbol or sequence", location)
                curPart.repeatCount = RepeatType.SingleOrMore
                curPart = None
            elif curStr == '*':
                if curPart == None:
                    raise FormatError("Error at '*'; must follow a symbol or sequence", location)
                curPart.repeatCount = RepeatType.ZeroOrMore
                curPart = None
            elif curStr == '?':
                if curPart == None:
                    raise FormatError("Error at '?'; must follow a symbol or sequence", location)
                curPart.repeatCount = RepeatType.Optional
                curPart = None
            elif curStr[0] == '<':
                curErrorHelpers.append(curStr[1:-1])
                #print(curErrorHelpers)
            elif curStr == ']' or curStr == ')':
                raise FormatError("Unexpected closing bracket " + curStr, location)
            else:
                curPart = ProductionPart(curPartName(), curPartHint(), location, "", "", ProductionType.SubProd, counterNode.name, curErrorHelpers)
                curErrorHelpers = []
                counterNode.partCounter += 1

                # variable
                colonInd = curStr.find(':', 0)
                symbolInd = 0
                if colonInd != -1:

                    # a bit hackish... for detecting LIST_VARIABLE_SUFFIX that's a colon currently
                    if curStr[colonInd+1] == ':':
                        colonInd += 1

                    var = curStr[0:colonInd]
                    if not ("\'" in var or "\"" in var):
                        if var.endswith(LIST_VARIABLE_SUFFIX):
                            curPart.variable = var[0:(-len(LIST_VARIABLE_SUFFIX))]
                            curPart.variableIsList = True
                        else:
                            curPart.variable = var
                            curPart.variableIsList = False
                        symbolInd = colonInd+1

                # symbol
                
                symbolOrString = curStr[symbolInd:]
                symbol = ""
                
                if symbolOrString[0] == "\'" or symbolOrString[0] == "\"":
                    # quoted symbols
                    if symbolOrString[-1] != '\'' and symbolOrString[-1] != '\"':
                        raise FormatError(f"Expected a '\\{symbolOrString[0]}'", location)

                    qStr = unescapeString(symbolOrString[1 : -1])

                    symbol = ""
                    for string, token in lexer.stringTokenPairs:
                        if string == qStr:
                            symbol = token
                            break
                    if symbol == "":
                        raise FormatError(f"Unrecognizable string '{qStr}'", location)
                else:
                    # normal symbols
                    symbol = symbolOrString
                
                if symbol in lexer.tokenTypes:
                    curPart.type = ProductionType.Token
                    curPart.symbol = symbol
                else:
                    curPart.type = ProductionType.Node
                    curPart.symbol = symbol

                '''if curStr[0] == '<':
                    if curStr[-1] != '>':
                        raise FormatError("Expected a '>'", location)
                        
                    # argument
                    semicInd = curStr.find(':', 1)
                    if semicInd != -1:
                        curPart.variable = curStr[1:semicInd]
                        #if curPart.variable == "":# the prefix was only a semicolon
                        #    curPart.variable = ":"
                    else:
                        semicInd = 0

                    # store vals
                    curPart.symbol = curStr[semicInd+1:-1]
                    curPart.type = ProductionType.Node
                else:
                    curPart.type = ProductionType.Token

                    # quoted lexemes
                    if "\'" in curStr or "\"" in curStr:
                        if curStr[-1] != '\'' and curStr[-1] != '\"':
                            raise FormatError("Expected a '\\''", location)

                        # find quote
                        qPos = curStr.find("\'")
                        if qPos == -1: qPos = curStr.find("\"")
                        startQ = qPos+1
                        endQ = len(curStr)-1
                        qStr = unescapeString(curStr[startQ : endQ])
                        #print(curStr, qStr)

                        # find corresponding lexeme
                        lexeme = ""
                        #print((qStr))
                        for string, token in lexer.stringTokenPairs:
                            if string == qStr:
                                lexeme = token
                                break
                        if len(lexeme) == 0:
                            raise FormatError("Don't know what '" + safeStrConvert(qStr) + "' is", location)
                        curPart.symbol = lexeme

                        # argument
                        semicInd = curStr.find(':', 0)
                        if semicInd != -1 and semicInd < startQ:
                            curPart.variable = curStr[0:semicInd]
                            #if curPart.variable == "":
                            #    raise FormatError("Lexemes can't have only semicolons for prefix", location)

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
                    '''
                curOption.append(curPart)
                #print(location, curPart.variable, curPart.symbol,  "- "+curStr+"")


            curStr, curStrPos = next(parserIt, ("",0))

        #print("Option:", curOption)
        target.append(curOption)
        curOption = []

    except StopIteration:
        #print("Option:", curOption)
        target.append(curOption)
        curOption = []
        raise


def loadParser(lexer: Lexer, filename: str, semNodes : OrderedDict[str, SemanticNode]):
    print("Loading parser ", filename)

    lines = meaningfulLines(filename)
    parser = Parser()
    parser.semNodes = semNodes
    curNodeName = None

    try:
        l, location = next(lines, ("", Location()))
        while len(l):
            #print("...Line ", l)

            parserIt = iterParserLine(l)
            try:
                subStrPos = 0
                substr, subStrPos = next(parserIt, ("",0))

                # left side of production

                if substr != '=' and substr != '->':# new node
                    curNodeName = substr
                    substr, subStrPos = next(parserIt, ("",0))
                    if substr != '=' and substr != '->':
                        raise FormatError("Expected a '=' or a '->' got '"+substr+"'", location)

                # check if node exists
                if not curNodeName in parser.productions:
                    parser.productions[curNodeName] = Production(curNodeName, location)
                    if len(parser.startProduction) == 0:
                        parser.startProduction = curNodeName
                curNode = parser.productions[curNodeName]
                        
                if substr == '->':# semantic node
                    try:
                        substr, subStrPos = next(parserIt, ("",0))
                        
                        parser.productions[curNodeName].outSemNodeName = substr
                        parser.productions[curNodeName].visibleSemNodeName = substr
                        
                        try:
                            substr, subStrPos = next(parserIt, ("",0))
                            if substr != "":
                                parser.productions[curNodeName].outSemNodeName = substr
                        except StopIteration:
                            pass

                    except StopIteration:
                        raise FormatError("Expected a semantic node name, got nothing", location)
                elif substr == '=':# semantic node
                    # add production
                    try:
                        parseParserFileParseNodeProduction(location, lexer, curNode, curNode.mainPart.possibilities, parserIt, l, "")
                    except StopIteration:
                        pass
                
            except StopIteration:
                raise FormatError("Expected a '=', '->' or a prod name, got nothing", location)

            l, location = next(lines, ("", Location()))
    except FormatError as e:
        print("ERROR " + str(e.location) + ": " + e.message)
        sys.exit(1)
    except StopIteration:
        pass
    
    try:
        
        for name, prod in parser.productions.items():
            extractParts(prod.mainPart, parser.productionParts)
        
        print("Extracting semantic nodes...")
        for name, prod in parser.productions.items():
            if prod.outSemNodeName != NO_OUTPUT_PRODUCTION_STR and prod.outSemNodeName != FALTHRU_OUTPUT_PRODUCTION_STR:
                #parser.semNodeNames.add(prod.outSemNodeName)
                parser.semNodes.setdefault(prod.outSemNodeName, SemanticNode())
                parser.semNodes.setdefault(prod.visibleSemNodeName, SemanticNode())


        handledProds : set[str] = set()
        def processVariables(prodName):
            if prodName in handledProds:
                return

            prod = parser.productions[prodName]
            semNode = parser.semNodes.get(prod.outSemNodeName)

            parts : list[ProductionPart] = []
            extractParts(prod.mainPart, parts)

            for part in parts:
                if part.type == ProductionType.Node and part.symbol not in parser.productions.keys():
                    raise SemanticError(f"Variable {part.variable} of prod <<{part.hint}>> contains a production '{part.symbol}', which is undefined", part.location)

                if (part.type == ProductionType.Node or part.type == ProductionType.Token) and len(part.variable) > 0:
                    if part.variable != FALTHRU_VARIABLE_STR:

                        if semNode is None:
                            raise SemanticError(f"Variable {part.variable} of part <<{part.hint}>> ({part.type}) of prod <<{part.prodName}>> assigned to None node", part.location)
                        
                        varType = ""
                        defVal = ""

                        if part.type == ProductionType.Node:
                            varType = f"Ptr<SemanticNode_{parser.productions[part.symbol].visibleSemNodeName}>"
                            #varType = f"SemanticNodePtr"
                            defVal = "nullptr"
                        elif part.type == ProductionType.Token:
                            varType = "Token"

                        if part.variableIsList:
                            varType = f"std::list<{varType}>"
                            defVal = ""
                        
                        semNode.publicMembers.setdefault(part.variable, Member(part.variable, varType, defVal))
                    else:
                        childSemNodeName = parser.productions[part.symbol].visibleSemNodeName
                        parentSemNodeName = prod.visibleSemNodeName
                        if not semNodeExtends(childSemNodeName, parentSemNodeName, parser.semNodes):
                            raise SemanticError(f"Forwarding of variable in prod <<{part.hint}>> contains a semantic node of type '{childSemNodeName}', but the production needs to be of type '{parentSemNodeName}' which isn't an ancestor of the variable's type.", part.location)

            
            if prod.outSemNodeName != FALTHRU_OUTPUT_PRODUCTION_STR and not semNodeExtends(prod.outSemNodeName, prod.visibleSemNodeName, parser.semNodes):
                raise SemanticError(f"Visible semantic node '{prod.visibleSemNodeName}' of prod <<{part.prodName}>> isn't a parent of the outing semantic node '{prod.outSemNodeName}'.", part.location)
            
            handledProds.add(prodName)
        for prodName, prod in parser.productions.items():
            processVariables(prodName)


        print("Converting to state machine...")
        startTime = time.time()
        for name, prod in parser.productions.items():
            prod.startingParserState = convertToStates(prod.mainPart, None, parser, parser.parserStates)
        print("Converted to state machine in " + str(time.time()-startTime) + "s!")

        # Check if all referenced productions are defined
        for part in parser.productionParts:
            if part.type == ProductionType.Node:
                if not part.symbol in parser.productions:
                    raise SemanticError(f"Production '{part.symbol}' referenced in <<{part.hint}>> at line {part.location} but not defined.", part.location)
        
        print("Checking for recursions...")
        startTime = time.time()
        for name, prod in parser.productions.items():
            if hasUnavoidableReference(prod.mainPart, name, parser, {}):
                raise SemanticError(f"At node '{name}': Cannot avoid recursion through any productions")
        print("No forbidden recursions found in " + str(time.time()-startTime) + "s!")
    except SemanticError as e:
        print("ERROR " + str(e.location) + ": " + e.message)
        sys.exit(1)
    
    return parser


