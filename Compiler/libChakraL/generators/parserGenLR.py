from __future__ import annotations
import os
import re
from enum import Enum
from typing import Iterator
from genUtil import *
from lexerGen import *
from parserGenShared import *
import time

def writeCustomParserH(parser: Parser, filename: str, lexerHeaderfile: str, extraheaderfiles: list[str]):
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
    for hf in extraheaderfiles+[lexerHeaderfile]:
        LN(f'#include "{os.path.relpath(hf, start=os.path.dirname(filename))}"')
    #LN('#include "../autoinclude/' + os.path.basename(lexerHeaderfile) + '"')
    #LN('#include "chakralParserPrereqCustom.h"')
    LN("")
    LN("namespace ChakraL {")
    LN("")
    
    for name in parser.semNodeNames:
        TB();LN("class SemanticNode_" + name + " : public SemanticNode { public: ~SemanticNode_" + name + "(); void process(); std::string_view name() const; };")
    LN("")
    
    LN("")
    
    LN("")
    TB();LN("SemanticNodePtr getOrganized(SemanticNodePtr node, bool checkReplacement = true);")
    TB();LN("void extractErrors(SemanticNodePtr node, std::list<ParserError>& outErrors);")
    TB();LN("SemanticNodePtr parse(const std::list<Token> &input, std::list<ParserError>& outErrors);")
    LN("")
    LN("}")

    f.close()


def writeCustomParserCPP(parser: Parser, filename: str, headerfile: str, extraheaderfiles: list[str]):
    print("Writing parser ", filename)
    f = open(filename, "wt")

    def TB():
        f.write('    ')
    def LN(s: str):
        f.write(s)
        f.write('\n')

    LN("// This file is autogenerated. Do not edit!")
    LN("")
    for hf in extraheaderfiles+[headerfile]:
        LN(f'#include "{os.path.relpath(hf, start=os.path.dirname(filename))}"')
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
            TB();TB();LN("void a_" + state.name + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, SemanticNodeVariable* outputVar);")
        else:
            TB();TB();LN("void a_" + state.name + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, SemanticNodePtr curNode);")

    for state in parser.parserStates:
        TB();LN("")
        TB();TB();LN("// " + state.hint)

        #
        # *** Next state func ***
        #

        if state.type != StateType.Proxy:
            TB();TB();LN("bool n_" + state.name + "(StatePtr curState, StateSet& nextStates, const Token& token, bool isSuccessful) {")

            if state.type == StateType.Branch or state.type == StateType.Node:
                TB();TB();TB();LN("curState->childStateCtr--;")
                TB();TB();TB();LN("if (!isSuccessful) {")
                TB();TB();TB();TB();LN("if (curState->childStateCtr == 0) {")
                TB();TB();TB();TB();TB();LN("curState->node->isSuccessful = false;")
                TB();TB();TB();TB();TB();LN("for (auto par : curState->parentStates) par->nextFunc(par, nextStates, token, false);")
                TB();TB();TB();TB();LN("}")
                TB();TB();TB();TB();LN("return false;")
                TB();TB();TB();LN("}")
                TB();TB();TB();LN("curState->node->isSuccessful = true;")

            if state.type == StateType.Token:
                TB();TB();TB();LN("if (token.type != TokenType::" + state.symbol + ") {")
                TB();TB();TB();TB();LN("curState->node->errors.emplace_back(token, std::wstring(L\"("+state.name+") Expected " + state.symbol + ", got \")+WTokenNames[(int)token.type]);")
                TB();TB();TB();TB();LN("curState->node->isSuccessful = false;")
                TB();TB();TB();TB();LN("for (auto par : curState->parentStates) par->nextFunc(par, nextStates, token, false);")
                TB();TB();TB();TB();LN("return false;")
                TB();TB();TB();LN("}")
                if state.variable is not None and state.variable != "":
                    TB();TB();TB();LN("curState->node->tokenLists[\"" + state.variable + "\"].push_back(token);")
            elif state.type == StateType.Branch:
                '''TB();TB();TB();LN("bool isRelevant = false;")
                TB();TB();TB();LN("for (auto var : curState->outputVars) isRelevant = isRelevant || var->trySet(curState->node);")
                TB();TB();TB();LN("if (!isRelevant) return false;")'''
                TB();TB();TB();LN("for (auto var : curState->outputVars) var->trySet(curState->node);")

            # The following happens after confirming the prod part matches:
            
            # Add next state
            if state.nextState is None:
                TB();TB();TB();LN("for (auto par : curState->parentStates) par->nextFunc(par, nextStates, token, true);")
            elif state.nextState.type == StateType.Branch or state.nextState.type == StateType.Proxy:
                TB();TB();TB();LN("a_" + state.nextState.name + "(curState->parentStates, nextStates, &(curState->node->continuationNode));")
            else:
                TB();TB();TB();LN("a_" + state.nextState.name + "(curState->parentStates, nextStates, curState->node);")

            TB();TB();TB();LN("return true;")
            TB();TB();LN("}")

        #
        # *** Add state func ***
        #

        if state.type == StateType.Branch or state.type == StateType.Proxy:
            TB();TB();LN("void a_" + state.name + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, SemanticNodeVariable* outputVar) {")
        else:
            TB();TB();LN("void a_" + state.name + "(const std::set<StatePtr>& parentStates, StateSet& nextStates, SemanticNodePtr curNode) {")

        # add new state if needed
        if state.type == StateType.Token:
            TB();TB();TB();LN("StatePtr state = nextStates[&n_" + state.name + "];")
        elif state.type != StateType.Proxy:
            TB();TB();TB();LN("StatePtr state = nextStates.getHidden(&n_" + state.name + ");")
        
        if state.type == StateType.Proxy:
            for subState in state.proxyForStates:
                if subState is None:
                    TB();TB();TB();LN("Token token = Token();")
                    TB();TB();TB();LN("for (auto par : parentStates) par->nextFunc(par, nextStates, token, true);")
                    break
            for subState in state.proxyForStates:
                if subState is not None:
                    TB();TB();TB();LN("a_" + subState.name + "(parentStates, nextStates, outputVar);")
        else:# Branch, Node or Token

            # add parents
            TB();TB();TB();LN("state->parentStates.insert(parentStates.begin(), parentStates.end());")
            TB();TB();TB();LN("for (auto par : state->parentStates) par->childStateCtr++;")
                
            
            if state.type == StateType.Branch:
                TB();TB();TB();LN("state->outputVars.push_back(outputVar);")

            # If the state is new, set its parameters
            TB();TB();TB();LN("if (state->node == nullptr) {// The state is newly added")
            if state.type == StateType.Branch:
                TB();TB();TB();TB();LN("state->node = std::make_shared<SemanticNode_"+state.semNodeName+">();")
                if state.branchStart is None:
                    TB();TB();TB();TB();LN("Token token = Token();")
                    TB();TB();TB();TB();LN("for (auto par : state->parentStates) par->nextFunc(par, nextStates, token, true);")
                elif state.branchStart.type == StateType.Branch or state.branchStart.type == StateType.Proxy:
                    TB();TB();TB();TB();LN("a_" + state.branchStart.name + "({state}, nextStates, &(state->node->continuationNode));")
                else:
                    TB();TB();TB();TB();LN("a_" + state.branchStart.name + "({state}, nextStates, state->node);")
            else:
                TB();TB();TB();TB();LN("state->node = curNode;")

                if state.type == StateType.Node:
                    assert(parser.productions[state.symbol].startingParserState.type == StateType.Proxy or parser.productions[state.symbol].startingParserState.type == StateType.Branch)
                    if state.variable == ":":
                        TB();TB();TB();TB();LN("a_" + state.symbol + "({state}, nextStates, &(curNode->replacementNode));")
                    else:
                        TB();TB();TB();TB();LN("a_" + state.symbol + "({state}, nextStates, &(curNode->nodeLists[\"" + state.variable + "\"].emplace_back(nullptr)));")
                
            TB();TB();TB();LN("}")

        TB();TB();LN("}")
    
    TB();LN("}")
    TB();LN("")
    for name in parser.semNodeNames:
        TB();LN("SemanticNode_" + name + "::~SemanticNode_" + name + "() {}")
        TB();LN("std::string_view SemanticNode_" + name + "::name() const { return \"" + name + "\"; }")
    LN("")
    LN("")
    TB();LN("SemanticNodePtr parse(const std::list<Token> &input, std::list<ParserError>& outErrors)")
    TB();LN("{")
    TB();TB();LN("SemanticNodePtr res = std::make_shared<SemanticNode_"+parser.productions[parser.startProduction].semNodeName+">();")
    TB();TB();LN("StateSet curStates, nextStates;")
    TB();TB();LN("")
    TB();TB();LN("a_" + parser.startProduction + "({}, nextStates, &(res->continuationNode));")
    TB();TB();LN("")
    TB();TB();LN("auto tokenIt = input.begin();")
    TB();TB();LN("while (nextStates.size() > 0) {")
    TB();TB();TB();LN("curStates.stdSet = nextStates.stdSet;")
    TB();TB();TB();LN("nextStates.stdSetHidden.clear();")
    TB();TB();TB();LN("nextStates.stdSet.clear();")
    TB();TB();TB();LN("for (auto& state : curStates) {")
    TB();TB();TB();TB();LN("state->nextFunc(state, nextStates, *tokenIt, true);")
    TB();TB();TB();LN("}")
    #TB();TB();TB();LN("std::wcout << \"Parsed \" << tokenIt->line << L\", position \" << tokenIt->character << L\", token \" << tokenIt->str << std::endl;")
    TB();TB();TB();LN("tokenIt++;")
    TB();TB();TB();LN("if (tokenIt == input.end()) {outErrors.emplace_back(Token(), L\"Parser reached the end of token list.\"); break;}")
    TB();TB();LN("}")
    TB();TB();LN("extractErrors(res, outErrors);")
    TB();TB();LN("return res;")
    TB();LN("}")
    LN("")
    LN("}")

    f.close()