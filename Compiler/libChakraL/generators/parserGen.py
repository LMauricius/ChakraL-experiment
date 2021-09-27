from __future__ import annotations
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
        #self.altStatePartNames: set[str] = set() # epsilon transitions

class ParseNode:
    def __init__(self, name: str):
        self.name = name
        self.mainPart = ProductionPart(name, name, "<>", "<>", ProductionType.SubProd, name, True)
        #self.possibilities: list[list[ProductionPart]] = []
        self.partCounter = 1

class Parser:
    def __init__(self):
        self.startNode = ""
        self.nodes: dict[str, ParseNode] = {}
        self.productionParts: dict[str, ProductionPart] = {}

def iterSubProductionParts(part : ProductionPart) -> Iterator[ProductionPart]:
    if part.type == ProductionType.SubProd:
        for poss in part.possibilities:
            for subpart in poss:
                yield subpart
                yield from iterSubProductionParts(subpart)

def iterProductionParts(node : ParseNode) -> Iterator[ProductionPart]:
    #print(node.possibilities)
    yield node.mainPart
    yield from iterSubProductionParts(node.mainPart)

def setTransitions(production : list[ProductionPart]):
    nextStateName: str = ""
    #possAltStates: set[str] = {nextState}

    for part in reversed(production):
        if part.type == ProductionType.SubProd:
            for poss in part.possibilities:
                setTransitions(poss)

        part.nextStateName = nextStateName

        '''if part.repeatCount == RepeatType.Optional or part.repeatCount == RepeatType.ZeroOrMore:
            part.altStatePartNames.update(possAltStates)
        else:
            possAltStates = set()'''
            
        '''if part.repeatCount == RepeatType.SingleOrMore or part.repeatCount == RepeatType.ZeroOrMore:
            part.nextStatePartNames.add(part.idName)'''

        #possAltStates.add(part.idName)
        nextStateName = part.idName


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
            curNode = parser.nodes[curNodeName]
            
            # add production
            try:
                parseParserFileParseNodeProduction(lineInd, lexer, curNode, curNode.mainPart.possibilities, parserIt, l, "")
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
            parser.productionParts[part.idName] = part
        
        setTransitions([node.mainPart])
        #for poss in node.mainPart.possibilities:
        #    setTransitions(poss)
    
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
    TB();TB();LN("virtual void process();")
    TB();TB();LN("void pullFrom(ParseNode& other);")
    TB();TB();LN("")
    TB();TB();LN("std::map<std::string, std::list<ParseNodePtr>> nodeLists;")
    TB();TB();LN("std::map<std::string, std::list<Token>> tokenLists;")
    TB();TB();LN("ParseNodePtr contToNode = nullptr;")
    TB();LN("};")
    
    for name, node in parser.nodes.items():
        TB();LN("class ParseNode_" + name + " : public ParseNode { public: ~ParseNode_" + name + "(); void process(); };")
    LN("")
    
    LN("")
    TB();LN("// State utils")
    TB();LN("struct StateSet;")
    TB();LN("struct State;")
    TB();LN("using StatePtr = std::shared_ptr<State>;")
    TB();LN("using NextFuncT = bool (*)(StatePtr curState, StateSet& nextStates, const Token& token);// returns whether the token matches")
    TB();LN("")
    TB();LN("struct State {")
    TB();TB();LN("NextFuncT nextFunc;")
    TB();TB();LN("std::set<StatePtr> parentStates;")
    TB();TB();LN("// This points to the current node, where we store the variables")
    TB();TB();LN("ParseNodePtr node = nullptr;")
    TB();TB();LN("// Used only if the state represents a sub-node part; this points to the sub-node, that will be stored in a variable of the current node")
    TB();TB();LN("ParseNodePtr subNode = nullptr;")
    TB();TB();LN("std::set<ParseNodePtr> contFromNodes;")
    TB();TB();LN("size_t childStateCtr = 0;")
    TB();TB();LN("")
    TB();TB();LN("inline State(NextFuncT nextFunc): nextFunc(nextFunc) {{}}")
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
    TB();LN("};")
    LN("")
    TB();LN("class ParserError {")
    TB();LN('public:')
    TB();TB();LN('inline ParserError(Token token, std::wstring msg): token(token), msg(msg) {{}}')
    TB();TB();LN('std::wstring msg;')
    TB();TB();LN('Token token;')
    TB();LN("};")
    LN("")
    TB();LN("std::list<Token> parse(const std::list<Token> &input, std::list<ParserError>& outErrors);")
    LN("")
    LN("}")

    f.close()


def writeParserProcessCPP(parser: Parser, filename: str, headerfile: str):
    definitions: map[str, str] = {}
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
    except FileNotFoundError as e:
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
    
    LN('#include <vector>')
    LN('#include <string_view>')
    LN('#include <regex>')
    LN("")
    LN("namespace ChakraL")
    LN("{")
    LN("")
    TB();LN("ParseNode::~ParseNode() {")
    TB();LN("};")
    TB();LN("void ParseNode::process() {")
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
    TB();LN("")
    
    # Declarations
    for name, part in parser.productionParts.items():
        #TB();LN("bool n_" + part.idName + "(StatePtr curState, StateSet& nextStates, const Token& token);")
        TB();LN("void a_" + part.idName + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, ParseNodePtr curNode);")

    for name, part in parser.productionParts.items():
        LN("")
        TB();LN("// " + part.hint)

        #
        # *** Next state func ***
        #

        TB();LN("bool n_" + part.idName + "(StatePtr curState, StateSet& nextStates, const Token& token) {")

        if part.type == ProductionType.Token:
            TB();TB();LN("if (token.type != TokenType::" + part.symbol + ")")
            TB();TB();TB();LN("return false;")
            if len(part.variable) > 0:
                TB();TB();LN("curState->node->tokenLists[\"" + part.variable + "\"].push_back(token);")
        elif part.type == ProductionType.Node:
            TB();TB();LN("curState->node->nodeLists[\"" + part.variable + "\"].push_back(curState->subNode);")
            #TB();TB();LN("curState.node->nodeLists[\"" + part.variable + "\"].push_back(curState.subNode);")
            '''TB();TB();LN("if (curState.subNode) {")
            TB();TB();TB();LN("curState.node->nodeLists[\"" + part.variable + "\"].push_back(curState.subNode);")
            TB();TB();TB();LN("curState.subNode = nullptr;// prevent from adding same node multiple times")
            TB();TB();LN("}")'''

        # The following happens after confirming the prod part matches:
        
        # Add next state(s)
        if part.nextStateName == "":
            TB();TB();LN("for (auto par : curState->parentStates) par->nextFunc(par, nextStates, token);")
        else:
            TB();TB();LN("a_" + part.nextStateName + "(curState->parentStates, nextStates, curState->node);")

        # Repeat current state if needed
        if part.repeatCount == RepeatType.SingleOrMore or part.repeatCount == RepeatType.ZeroOrMore:
            TB();TB();LN("a_" + part.idName + "(curState->parentStates, nextStates, curState->node);")

        TB();TB();LN("return true;")
        TB();LN("}")

        #
        # *** Add state func ***
        #

        TB();LN("void a_" + part.idName + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, ParseNodePtr curNode) {")

        # add new state if needed
        if part.type == ProductionType.SubProd or part.type == ProductionType.Node:
            TB();TB();LN("StatePtr state = nextStates.getHidden(&n_" + part.idName + ");")
        else:
            TB();TB();LN("StatePtr state = nextStates[&n_" + part.idName + "];")

        # add parents
        TB();TB();LN("state->parentStates.insert(parentStates.begin(), parentStates.end());")

        # If the state is new, set its parameters
        TB();TB();LN("if (state->node == nullptr) {// The state is newly added")
        if part.isMainPart:
            TB();TB();TB();LN("state->node = std::make_shared<ParseNode_"+part.idName+">();")
            TB();TB();TB();LN("for (auto par : parentStates) par->subNode = state->node;")
        else:
            TB();TB();TB();LN("state->node = curNode;")

        if part.type == ProductionType.SubProd:
            for poss in part.possibilities:
                TB();TB();TB();LN("a_" + poss[0].idName + "({state}, nextStates, curNode);")
        elif part.type == ProductionType.Node:
            TB();TB();TB();LN("a_" + part.symbol + "({state}, nextStates, curNode);")
            TB();TB();LN("state->node->nodeLists[\"" + part.variable + "\"].push_back(state->subNode);")
        TB();TB();LN("}")

        if part.repeatCount == RepeatType.SingleOrMore or part.repeatCount == RepeatType.ZeroOrMore:
            pass
        '''for altName in part.altStatePartNames:
            if nextName == "_return_parent_":
                TB();TB();LN("for (auto par : parentStates) par->nextFunc(par, nextStates, token);")
            else:
                TB();TB();LN("a_" + nextName + "(parentStates, nextStates, curNode);")'''
        #TB();TB();LN("return state;")
        TB();LN("}")
    
    LN("")
    TB();LN("std::list<Token> parse(const std::list<Token> &input, std::list<ParserError>& outErrors)")
    TB();LN("{")
    TB();LN("}")
    LN("")
    LN("}")

    f.close()