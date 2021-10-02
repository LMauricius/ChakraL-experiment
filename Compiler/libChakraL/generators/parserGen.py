from __future__ import annotations
import os
import re
from enum import Enum
from typing import Iterator
from genUtil import *
from lexerGen import *
import time

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
    def __init__(self, idName: str, hint: str, variable: str, symbol: str, type: ProductionType, nodeName: str, isMainPart: bool = False):
        self.idName = idName
        self.hint = hint
        self.variable = variable
        self.symbol = symbol
        self.possibilities: list[list[ProductionPart]] = []
        self.type = type
        self.isMainPart = isMainPart
        self.nodeName = nodeName
        self.repeatCount = -1
        self.nextStateName: str = ""

class ParserState:
    def __init__(self, name: str, hint: str, type: StateType, nodeName: str):
        self.name = name
        self.hint = hint
        self.variable: str = None
        self.symbol: str = None
        self.type = type
        self.nodeName = nodeName
        self.nextState: ParserState = None
        self.branchStart: ParserState = None
        self.proxyForStates: list[ParserState] = []

class ParseNode:
    def __init__(self, name: str):
        self.name = name
        self.mainPart = ProductionPart(name, name, "<>", "<>", ProductionType.SubProd, name, True)
        self.startingParserState : ParserState = None
        self.partCounter = 1

class Parser:
    def __init__(self):
        self.startNode = ""
        self.nodes: dict[str, ParseNode] = {}
        self.parserStates: list[ParserState] = []

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

def detectRecursionsAndCrash(part : ProductionPart, path, visited: set[ParseNode], parser: Parser, nodeName: str):
    if part.type == ProductionType.Token:
        pass
    elif part.type == ProductionType.Node:
        node = parser.nodes[part.symbol]
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

def convertToStates(part : ProductionPart, nextState: ParserState, outParserStates: list[ParserState]):
    retState : ParserState = None# if retState == None, the newState will be stored in retState and returned
    storeState : ParserState = None# if storeState != None, the newState will be stored in storeState.branchStart instead of newState
    newState : ParserState = None

    #insertPos = len(outParserStates)
    
    # = Manage repeating =
    if part.repeatCount == RepeatType.Single:
        pass
    elif part.repeatCount == RepeatType.Optional:
        selectState = ParserState(part.idName+"__select", part.hint, StateType.Proxy, part.nodeName)
        outParserStates.append(selectState)

        if nextState is not None and nextState.type == StateType.Branch:
            skipBranch = nextState
        else:
            skipBranch = ParserState(part.idName+f"__cont", part.hint, StateType.Branch, part.nodeName)
            outParserStates.append(skipBranch)
            skipBranch.branchStart = nextState

        acceptBranch = ParserState(part.idName+f"__accept", part.hint, StateType.Branch, part.nodeName)
        outParserStates.append(acceptBranch)
        storeState = acceptBranch
        
        selectState.proxyForStates = [skipBranch, acceptBranch]

        nextState = skipBranch
        retState = selectState
    elif part.repeatCount == RepeatType.ZeroOrMore:
        repeatState = ParserState(part.idName+"__repeat", part.hint, StateType.Proxy, part.nodeName)
        outParserStates.append(repeatState)

        if nextState is not None and nextState.type == StateType.Branch:
            skipBranch = nextState
        else:
            skipBranch = ParserState(part.idName+f"__cont", part.hint, StateType.Branch, part.nodeName)
            outParserStates.append(skipBranch)
            skipBranch.branchStart = nextState

        cycleBranch = ParserState(part.idName+f"__cycle", part.hint, StateType.Branch, part.nodeName)
        outParserStates.append(cycleBranch)
        storeState = cycleBranch
        
        repeatState.proxyForStates = [skipBranch, cycleBranch]

        nextState = repeatState
        retState = repeatState
    elif part.repeatCount == RepeatType.SingleOrMore:
        repeatState = ParserState(part.idName+"__repeat", part.hint, StateType.Proxy, part.nodeName)
        outParserStates.append(repeatState)

        if nextState is not None and nextState.type == StateType.Branch:
            skipBranch = nextState
        else:
            skipBranch = ParserState(part.idName+f"__cont", part.hint, StateType.Branch, part.nodeName)
            outParserStates.append(skipBranch)
            skipBranch.branchStart = nextState

        cycleBranch = ParserState(part.idName+f"__cycle", part.hint, StateType.Branch, part.nodeName)
        outParserStates.append(cycleBranch)
        storeState = cycleBranch
        
        repeatState.proxyForStates = [skipBranch, cycleBranch]

        nextState = repeatState
        retState = None # We want to directly enter the new state

    # = Create new state =
    if part.type == ProductionType.SubProd:
        newState = ParserState(part.idName, part.hint, StateType.Proxy, part.nodeName)
        outParserStates.append(newState)
        i = 1
        for poss in part.possibilities:
            branch = ParserState(part.idName+f"__poss{i}", part.hint, StateType.Branch, part.nodeName)
            outParserStates.append(branch)

            insertInd = len(outParserStates)
            for subpart in reversed(poss):
                tmpOutParserStates = []
                subState = convertToStates(subpart, nextState, tmpOutParserStates)
                nextState = subState
                outParserStates[insertInd:insertInd] = tmpOutParserStates

            assert(nextState is not None)
            branch.branchStart = nextState
            newState.proxyForStates.append(branch)
            i += 1
    elif part.type == ProductionType.Token:
        newState = ParserState(part.idName, part.hint, StateType.Token, part.nodeName)
        outParserStates.append(newState)
        newState.variable = part.variable
        newState.symbol = part.symbol
        newState.nextState = nextState
    elif part.type == ProductionType.Node:
        newState = ParserState(part.idName, part.hint, StateType.Node, part.nodeName)
        outParserStates.append(newState)
        newState.variable = part.variable
        newState.symbol = part.symbol
        newState.nextState = nextState

    # = Store new state =
    if retState is None:
        retState = newState
    if storeState is not None:
        assert(newState is not None)
        storeState.branchStart = newState
        
    # = Return states =
    return retState


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
                curPart = ProductionPart(curPartName(), curPartHint(), "", "", ProductionType.SubProd, counterNode.name)
                counterNode.partCounter += 1
                curOption.append(curPart)
                parseParserFileParseNodeProduction(lineInd, lexer, counterNode, curPart.possibilities, parserIt, fullLine, ')')
            elif curStr == '[':
                curPart = ProductionPart(curPartName(), curPartHint(), "", "", ProductionType.SubProd, counterNode.name)
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
                curPart = ProductionPart(curPartName(), curPartHint(), "", "", ProductionType.SubProd, counterNode.name)
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
                        for regex, token in lexer.regexTokenPairs:
                            if re.match("^"+regex+"$", qStr, re.M):
                                lexeme = token
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
    print("Loading parser ", filename)

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
                if len(parser.startNode) == 0:
                    parser.startNode = curNodeName
            curNode = parser.nodes[curNodeName]
            
            # add production
            try:
                parseParserFileParseNodeProduction(lineInd, lexer, curNode, curNode.mainPart.possibilities, parserIt, l, "")
            except StopIteration:
                pass

            l, lineInd = next(lines, ("",-1))
    except FormatError as e:
        print("ERROR At line " + str(e.lineInd) + ": " + e.message)
        sys.exit(1)
    except StopIteration:
        pass
    
    try:
        print("Converting to state machine...")
        startTime = time.time()
        for name, node in parser.nodes.items():
            node.startingParserState = convertToStates(node.mainPart, None, parser.parserStates)
        print("Converted to state machine in " + str(time.time()-startTime) + "s!")
        
        print("Checking for recursions...")
        startTime = time.time()
        for name, node in parser.nodes.items():
            detectRecursionsAndCrash(node.mainPart, [], set(), parser, name)
        print("No recursions found in " + str(time.time()-startTime) + "s!")
    except SemanticError as e:
        print("ERROR " + e.message)
        sys.exit(1)
    
    return parser




def writeParserH(parser: Parser, filename: str, lexerHeaderfile: str):
    print("Writing parser ", filename)
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
    LN('#include <map>')
    LN('#include <set>')
    LN('#include <memory>')
    LN('#include "' + os.path.basename(lexerHeaderfile) + '"')
    LN("")
    LN("namespace ChakraL {")
    LN("")
    TB();LN("class ParseNode;")
    TB();LN("using ParseNodePtr = std::shared_ptr<ParseNode>;")
    LN("")
    TB();LN("class ParseNode {")
    TB();LN("public:")
    TB();TB();LN("virtual ~ParseNode();")
    TB();TB();LN("virtual void process() = 0;")
    TB();TB();LN("virtual std::string_view name() const = 0;")
    TB();TB();LN("void pullFrom(ParseNode& other);")
    TB();TB();LN("")
    TB();TB();LN("std::map<std::string, std::list<ParseNodePtr>> nodeLists;")
    TB();TB();LN("std::map<std::string, std::list<Token>> tokenLists;")
    TB();TB();LN("ParseNodePtr continuationNode = nullptr;")
    TB();LN("};")
    
    for name, node in parser.nodes.items():
        TB();LN("class ParseNode_" + name + " : public ParseNode { public: ~ParseNode_" + name + "(); void process(); std::string_view name() const; };")
    LN("")
    
    LN("")
    TB();LN("// State utils")
    TB();LN("struct StateSet;")
    TB();LN("struct State;")
    TB();LN("using StatePtr = std::shared_ptr<State>;")
    TB();LN("using NextFuncT = bool (*)(StatePtr curState, StateSet& nextStates, const Token& token, ParseNodePtr node);// returns whether the token matches. Node must be used instead of state.node for new states")
    TB();LN("")
    TB();LN("struct State {")
    TB();TB();LN("NextFuncT nextFunc;")
    TB();TB();LN("std::set<StatePtr> parentStates;")
    TB();TB();LN("// This points to the current node, where we store the variables")
    TB();TB();LN("ParseNodePtr node = nullptr;")
    TB();TB();LN("std::list<ParseNodePtr*> outputVars;// save to vars on confirm")
    TB();TB();LN("size_t childStateCtr = 0;")
    TB();TB();LN("")
    TB();TB();LN("inline State(NextFuncT nextFunc): nextFunc(nextFunc) {}")
    TB();TB();LN("State() = default;")
    TB();TB();LN("State(const State&) = default;")
    TB();TB();LN("State(State&&) = default;")
    TB();TB();LN("State& operator=(const State&) = default;")
    TB();TB();LN("State& operator=(State&&) = default;")
    TB();TB();LN("")
    TB();LN("};")
    TB();LN("")
    TB();LN("struct StateComparatorLess {")
    TB();TB();LN("using is_transparent = std::true_type;")
    TB();TB();LN("")
    TB();TB();LN("inline bool operator()(const StatePtr& left, const StatePtr& right) const {")
    TB();TB();TB();LN("return (left->nextFunc < right->nextFunc);")
    TB();TB();LN("}")
    TB();TB();LN("inline bool operator()(const NextFuncT& left, const StatePtr& right) const {")
    TB();TB();TB();LN("return (left < right->nextFunc);")
    TB();TB();LN("}")
    TB();TB();LN("inline bool operator()(const StatePtr& left, const NextFuncT& right) const {")
    TB();TB();TB();LN("return (left->nextFunc < right);")
    TB();TB();LN("}")
    TB();LN("};")
    TB();LN("")
    TB();LN("class StateSet {")
    TB();LN("public:")
    TB();TB();LN("std::set<StatePtr, StateComparatorLess> stdSet;")
    TB();TB();LN("std::set<StatePtr, StateComparatorLess> stdSetHidden;")
    TB();TB();LN("")
    TB();TB();LN("inline StatePtr operator[](NextFuncT nextFunc) {")
    TB();TB();TB();LN("auto it = stdSet.find(nextFunc);")
    TB();TB();TB();LN("if (it == stdSet.end()) {")
    TB();TB();TB();TB();LN("it = stdSetHidden.find(nextFunc);")
    TB();TB();TB();TB();LN("if (it == stdSetHidden.end()) {")
    TB();TB();TB();TB();TB();LN("it = stdSet.insert(std::make_shared<State>(nextFunc)).first;")
    TB();TB();TB();TB();LN("} else {")
    TB();TB();TB();TB();TB();LN("StatePtr statePtr = *it;")
    TB();TB();TB();TB();TB();LN("stdSetHidden.erase(it);")
    TB();TB();TB();TB();TB();LN("it = stdSet.insert(statePtr).first;")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("return *it;")
    TB();TB();LN("}")
    TB();TB();LN("inline StatePtr getHidden(NextFuncT nextFunc) {")
    TB();TB();TB();LN("auto it = stdSet.find(nextFunc);")
    TB();TB();TB();LN("if (it == stdSet.end()) {")
    TB();TB();TB();TB();LN("it = stdSetHidden.find(nextFunc);")
    TB();TB();TB();TB();LN("if (it == stdSetHidden.end()) {")
    TB();TB();TB();TB();TB();LN("it = stdSetHidden.insert(std::make_shared<State>(nextFunc)).first;")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("return *it;")
    TB();TB();LN("}")
    TB();TB();LN("")
    TB();TB();LN("inline size_t size() const {return stdSet.size();}")
    TB();TB();LN("inline std::set<StatePtr, StateComparatorLess>::iterator begin() {return stdSet.begin();}")
    TB();TB();LN("inline std::set<StatePtr, StateComparatorLess>::iterator end() {return stdSet.end();}")
    TB();TB();LN("")
    TB();LN("};")
    LN("")
    TB();LN("class ParserError {")
    TB();LN('public:')
    TB();TB();LN('inline ParserError(Token token, std::wstring msg): token(token), msg(msg) {{}}')
    TB();TB();LN('std::wstring msg;')
    TB();TB();LN('Token token;')
    TB();LN("};")
    LN("")
    TB();LN("ParseNodePtr parse(const std::list<Token> &input, std::list<ParserError>& outErrors);")
    LN("")
    LN("}")

    f.close()


def writeParserProcessCPP(parser: Parser, filename: str, headerfile: str):
    definitions: dict[str, str] = {}
    for name, node in parser.nodes.items():
        #declarations[name] = "    ParseNode_" + name + "::process("
        definitions[name] = ""

    print("Reading old parser nodes process definitions ", filename)
    try:
        with open(filename, "rt") as f:
            curDef = ""
            for line in f:
                if line.startswith("    void ParseNode_"):
                    curDef = line[len("    void ParseNode_"):line.find("::")]
                elif line.startswith("    }"):
                    curDef = ""
                elif len(curDef) > 0:
                    definitions[curDef] += line
    except FileNotFoundError:
        print("No old parser nodes process definitions found")

    print("Writing new parser nodes process definitions ", filename)
    with open(filename, "wt") as f:

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
        TB();LN("")
        for name, definition in definitions.items():
            LN("    void ParseNode_" + name + "::process() {")
            f.write(definition)
            LN("    }")
            TB();LN("")
        LN("}")


def writeParserCPP(parser: Parser, filename: str, headerfile: str):
    print("Writing parser ", filename)
    f = open(filename, "wt")

    def TB():
        f.write('    ')
    def LN(s: str):
        f.write(s)
        f.write('\n')

    LN("// This file is autogenerated. Do not edit!")
    LN("")
    LN('#include "' + os.path.basename(headerfile) + '"')
    LN('#include <iostream>')
    
    LN("")
    LN("namespace ChakraL")
    LN("{")
    LN("")
    TB();LN("namespace")
    TB();LN("{")
    TB();TB();LN("")
    
    # Declarations
    for state in parser.parserStates:
        if state.type == StateType.Branch or state.type == StateType.Proxy:
            TB();TB();LN("void a_" + state.name + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, ParseNodePtr* outputVar);")
        else:
            TB();TB();LN("void a_" + state.name + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, ParseNodePtr curNode);")

    for state in parser.parserStates:
        TB();LN("")
        TB();TB();LN("// " + state.hint)

        #
        # *** Next state func ***
        #

        if state.type != StateType.Proxy:
            TB();TB();LN("bool n_" + state.name + "(StatePtr curState, StateSet& nextStates, const Token& token, ParseNodePtr node) {")

            if state.type == StateType.Token:
                TB();TB();TB();LN("if (token.type != TokenType::" + state.symbol + ")")
                TB();TB();TB();TB();LN("return false;")
                if state.variable is not None:
                    TB();TB();TB();LN("curState->node->tokenLists[\"" + state.variable + "\"].push_back(token);")
            elif state.type == StateType.Branch:
                TB();TB();TB();LN("for (auto var : curState->outputVars) *var = curState->node;")

            # The following happens after confirming the prod part matches:
            
            # Add next state
            if state.nextState is None:
                TB();TB();TB();LN("for (auto par : curState->parentStates) par->nextFunc(par, nextStates, token, node);")
            elif state.nextState.type == StateType.Branch or state.nextState.type == StateType.Proxy:
                TB();TB();TB();LN("a_" + state.nextState.name + "(curState->parentStates, nextStates, &(node->continuationNode));")
            else:
                TB();TB();TB();LN("a_" + state.nextState.name + "(curState->parentStates, nextStates, node);")

            TB();TB();TB();LN("return true;")
            TB();TB();LN("}")

        #
        # *** Add state func ***
        #

        if state.type == StateType.Branch or state.type == StateType.Proxy:
            TB();TB();LN("void a_" + state.name + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, ParseNodePtr* outputVar) {")
        else:
            TB();TB();LN("void a_" + state.name + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, ParseNodePtr curNode) {")

        # add new state if needed
        if state.type == StateType.Token:
            TB();TB();TB();LN("StatePtr state = nextStates[&n_" + state.name + "];")
        elif state.type != StateType.Proxy:
            TB();TB();TB();LN("StatePtr state = nextStates.getHidden(&n_" + state.name + ");")
        
        if state.type == StateType.Node:
            assert(parser.nodes[state.symbol].startingParserState.type == StateType.Proxy)
            TB();TB();TB();LN("a_" + state.symbol + "({state}, nextStates, &(curNode->nodeLists[\"" + state.variable + "\"].emplace_back(nullptr)));")
        elif state.type == StateType.Proxy:
            for subState in state.proxyForStates:
                TB();TB();TB();LN("a_" + subState.name + "(parentStates, nextStates, outputVar);")
        else:# Branch or Token

            # add parents
            TB();TB();TB();LN("state->parentStates.insert(parentStates.begin(), parentStates.end());")
            
            if state.type == StateType.Branch:
                TB();TB();TB();LN("state->outputVars.push_back(outputVar);")

            # If the state is new, set its parameters
            TB();TB();TB();LN("if (state->node == nullptr) {// The state is newly added")
            if state.type == StateType.Branch:
                TB();TB();TB();TB();LN("state->node = std::make_shared<ParseNode_"+state.nodeName+">();")
                if state.branchStart is None:
                    TB();TB();TB();TB();LN("for (auto par : state->parentStates) par->nextFunc(par, nextStates, Token(), state->node);")
                elif state.branchStart.type == StateType.Branch or state.branchStart.type == StateType.Proxy:
                    TB();TB();TB();TB();LN("a_" + state.branchStart.name + "({state}, nextStates, &(state->node->continuationNode));")
                else:
                    TB();TB();TB();TB();LN("a_" + state.branchStart.name + "({state}, nextStates, state->node);")
            else:
                TB();TB();TB();TB();LN("state->node = curNode;")
            TB();TB();TB();LN("}")

        TB();TB();LN("}")
    
    TB();LN("}")
    TB();LN("")
    TB();LN("ParseNode::~ParseNode() {")
    TB();LN("};")
    TB();LN("void ParseNode::process() {")
    TB();LN("};")
    TB();LN("std::string_view ParseNode::name() const {")
    TB();TB();LN("return \"UNDEFINED_NODE\";")
    TB();LN("};")
    TB();LN("")
    TB();LN("void ParseNode::pullFrom(ParseNode& other) {")
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
    for name, node in parser.nodes.items():
        TB();LN("ParseNode_" + name + "::~ParseNode_" + name + "() {}")
        TB();LN("std::string_view ParseNode_" + name + "::name() const { return \"" + name + "\"; }")
    LN("")
    TB();LN("ParseNodePtr parse(const std::list<Token> &input, std::list<ParserError>& outErrors)")
    TB();LN("{")
    TB();TB();LN("ParseNodePtr res = std::make_shared<ParseNode_"+parser.startNode+">();;")
    TB();TB();LN("StateSet curStates, nextStates;")
    TB();TB();LN("")
    TB();TB();LN("a_" + parser.startNode + "({}, nextStates, &(res->continuationNode));")
    TB();TB();LN("")
    TB();TB();LN("auto tokenIt = input.begin();")
    TB();TB();LN("while (nextStates.size() > 0) {")
    TB();TB();TB();LN("curStates.stdSet = nextStates.stdSet;")
    TB();TB();TB();LN("nextStates.stdSetHidden.clear();")
    TB();TB();TB();LN("nextStates.stdSet.clear();")
    TB();TB();TB();LN("for (auto& state : curStates) {")
    TB();TB();TB();TB();LN("state->nextFunc(state, nextStates, *tokenIt, state->node);")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("std::wcout << \"Parsed \" << tokenIt->line << L\", position \" << tokenIt->character << L\", token \" << tokenIt->str << std::endl;")
    TB();TB();TB();LN("tokenIt++;")
    TB();TB();TB();LN("if (tokenIt == input.end()) {outErrors.emplace_back(Token(), L\"Parser reached the end of token list.\"); break;}")
    TB();TB();LN("}")
    TB();TB();LN("return res;")
    TB();LN("}")
    LN("")
    LN("}")

    f.close()