from __future__ import annotations
import json
import os
import re
from enum import Enum
from typing import Iterator
from genUtil import *
from lexerGen import *
from parserGenShared import *
import time

def writeRecursiveParserH(parser: Parser, filename: str, lexerHeaderfile: str, extraheaderfiles: list[str]):
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
    
    for name, semNode in parser.semNodes.items():
        TB();LN("class SemanticNode_" + name + " : public SemanticNode { public: ~SemanticNode_" + name + "(); void process(); std::string_view name() const; };")
    LN("")
    
    LN("")
    
    LN("")
    TB();LN("SemanticNodePtr parse(const std::list<Token> &input, std::list<ParserError>& outErrors);")
    LN("")
    LN("}")

    f.close()

def getIterationSnippets(parser: Parser, subpart : ProductionPart, part : ProductionPart) -> Tuple[str, str, str]:
    initializerCodeStr = ""# The code that checks tokens, sets isOk to whether the production accepts the tokens
    checkerCodeStr = ""# The code that checks tokens, sets isOk to whether the production accepts the tokens
    executorCodeStr = [] # The code that moves iterator if isOk

    # SubProd
    if subpart.type == ProductionType.SubProd:
        initializerCodeStr = f"testInd = (ind < tokenNum? check_{subpart.idName}(tokenNum, tokens, data, ind) : FAIL_IND)"
        checkerCodeStr = "testInd != FAIL_IND"
        executorCodeStr.append(f"commands.emplace_back(new CommBranch(&(data.at(ind).commands[ProductionInd::{subpart.idName}])));")
        executorCodeStr.append("ind = testInd;")
    # Node
    elif subpart.type == ProductionType.Node:
        initializerCodeStr = f"testInd = (ind < tokenNum? check_{subpart.symbol}(tokenNum, tokens, data, ind) : FAIL_IND)"
        checkerCodeStr = "testInd != FAIL_IND"

        if parser.productions[part.prodName].semNodeName != FALTHRU_OUTPUT_PRODUCTION_STR and subpart.variable != FALTHRU_VARIABLE_STR:
            if subpart.variable != "":
                if subpart.variableIsList:
                    executorCodeStr.append(f"commands.emplace_back(new CommBranchWithList(&(data.at(ind).commands[ProductionInd::{subpart.symbol}]), \"{subpart.variable}\"));")
                else:
                    executorCodeStr.append(f"commands.emplace_back(new CommBranchWithVar(&(data.at(ind).commands[ProductionInd::{subpart.symbol}]), \"{subpart.variable}\"));")
            else:
                executorCodeStr.append(f"commands.emplace_back(new CommBranchWithNoVar(&(data.at(ind).commands[ProductionInd::{subpart.symbol}])));")
        else:
            executorCodeStr.append(f"commands.emplace_back(new CommBranch(&(data.at(ind).commands[ProductionInd::{subpart.symbol}])));")
            #executorCodeStr.append(f"commands.emplace_back(new CommBranch(data.at(ind).commands[ProductionInd::{subpart.symbol}].begin()));")
        
        executorCodeStr.append("ind = testInd;")
        
        '''if parser.productions[part.prodName].semNodeName != FALTHRU_OUTPUT_PRODUCTION_STR:
            executorCodeStr.append(f"commands.emplace_back(new CommPopNodeVar());")'''
    # Token
    elif subpart.type == ProductionType.Token:
        initializerCodeStr = ""
        checkerCodeStr = f"ind < tokenNum && tokens.at(ind).type == TokenType::{subpart.symbol}"
        if subpart.variable != "":
            if subpart.variableIsList:
                executorCodeStr.append(f"commands.emplace_back(new CommSaveTokenList(\"{subpart.variable}\", ind));")
            else:
                executorCodeStr.append(f"commands.emplace_back(new CommSaveTokenVar(\"{subpart.variable}\", ind));")
        executorCodeStr.append("ind++;")
    return (initializerCodeStr, checkerCodeStr, executorCodeStr)


def writeRecursiveParserCPP(parser: Parser, filename: str, headerfile: str, extraheaderfiles: list[str]):
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
    LN('#include <sstream>')
    LN('#include <algorithm>')
    
    LN("")
    LN("namespace ChakraL")
    LN("{")
    LN("")
    TB();LN("namespace")
    TB();LN("{")

    # Parser command predef
    
    TB();TB();LN("struct ParserState;")
    TB();TB();LN("struct ParserCommand {")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) = 0;")
    TB();TB();TB();LN("virtual void print(size_t indent) = 0;")
    TB();TB();LN("};")
    TB();TB();LN("")
    TB();TB();LN("using ParserCommandBranch = std::vector<std::unique_ptr<ParserCommand>>;")
    TB();TB();LN("")

    # Token data

    TB();TB();LN("enum class ProductionInd : uint16_t {")
    for part in parser.productionParts:
        if part.type == ProductionType.SubProd:
            #if part.isMainPart:
                TB();TB();TB();LN(f"{part.idName},")
    TB();TB();LN("};")
    TB();TB();LN("")
    TB();TB();LN("using TokenInd = uint32_t;")
    TB();TB();LN("const TokenInd FAIL_IND = -1;")
    TB();TB();LN("")
    TB();TB();LN("struct TokenAssignedData {")
    for part in parser.productionParts:
        if part.type == ProductionType.SubProd:
            if part.isMainPart:
                TB();TB();TB();LN(f"bool checked_{part.idName} : 1 = false;")
                TB();TB();TB();LN(f"bool is_{part.idName} : 1 = false;")
    TB();TB();TB();LN(f"std::map<ProductionInd, TokenInd> endInds;")
    TB();TB();TB();LN(f"std::map<ProductionInd, ParserCommandBranch> commands;")
    TB();TB();LN("};")
    TB();TB();LN("")

    # Parser commands

    TB();TB();LN("struct ParserState {")
    #TB();TB();TB();LN("std::vector<ParserCommandBranch::iterator> commStack;")
    #TB();TB();TB();LN("std::vector<SemanticNodePtr> nodeStack;")
    #TB();TB();TB();LN("std::vector<SemanticNodePtr*> nodeVarStack;")
    TB();TB();TB();LN("")
    TB();TB();TB();LN("std::vector<Token> tokens;")
    TB();TB();TB();LN("std::vector<TokenAssignedData> data;")
    TB();TB();LN("};")
    TB();TB();LN("")
    # CommBranch
    TB();TB();LN("struct CommBranch : public ParserCommand {")
    #TB();TB();TB();LN("ParserCommandBranch::iterator it;")
    TB();TB();TB();LN("ParserCommandBranch* br;")
    TB();TB();TB();LN("CommBranch(ParserCommandBranch* br) : br(br) {}")
    #TB();TB();TB();LN("CommBranch(ParserCommandBranch::iterator it) : it(it) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    #TB();TB();TB();TB();LN("state->commStack.push_back(it);")
    TB();TB();TB();TB();LN("for (auto& commPtr : *br) {")
    TB();TB();TB();TB();TB();LN("(*commPtr)(state, varPtr);")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("virtual void print(size_t indent) {")
    TB();TB();TB();TB();LN("for (int i=0; i<indent; i++) std::cout << ' ';")
    TB();TB();TB();TB();LN("std::cout << \"CommBranch\" << std::endl;")
    TB();TB();TB();TB();LN("for (auto& commPtr : *br) {")
    TB();TB();TB();TB();TB();LN("(*commPtr).print(indent+1);")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")
    # CommBranchWithVar
    TB();TB();LN("struct CommBranchWithVar : public ParserCommand {")
    TB();TB();TB();LN("ParserCommandBranch* br;")
    TB();TB();TB();LN("std::string name;")
    TB();TB();TB();LN("CommBranchWithVar(ParserCommandBranch* br, std::string name) : br(br), name(name) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("(*varPtr)->nodeLists[name].push_back(nullptr);")
    TB();TB();TB();TB();LN("for (auto& commPtr : *br) {")
    TB();TB();TB();TB();TB();LN("(*commPtr)(state, &((*varPtr)->nodeLists[name].back()));")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("virtual void print(size_t indent) {")
    TB();TB();TB();TB();LN("for (int i=0; i<indent; i++) std::cout << ' ';")
    TB();TB();TB();TB();LN("std::cout << \"CommBranchWithVar - \" << name << std::endl;")
    TB();TB();TB();TB();LN("for (auto& commPtr : *br) {")
    TB();TB();TB();TB();TB();LN("(*commPtr).print(indent+1);")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")
    # CommBranchWithList
    TB();TB();LN("struct CommBranchWithList : public ParserCommand {")
    TB();TB();TB();LN("ParserCommandBranch* br;")
    TB();TB();TB();LN("std::string name;")
    TB();TB();TB();LN("CommBranchWithList(ParserCommandBranch* br, std::string name) : br(br), name(name) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("(*varPtr)->nodeLists[name].push_back(nullptr);")
    TB();TB();TB();TB();LN("for (auto& commPtr : *br) {")
    TB();TB();TB();TB();TB();LN("(*commPtr)(state, &((*varPtr)->nodeLists[name].back()));")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("virtual void print(size_t indent) {")
    TB();TB();TB();TB();LN("for (int i=0; i<indent; i++) std::cout << ' ';")
    TB();TB();TB();TB();LN("std::cout << \"CommBranchWithList - \" << name << std::endl;")
    TB();TB();TB();TB();LN("for (auto& commPtr : *br) {")
    TB();TB();TB();TB();TB();LN("(*commPtr).print(indent+1);")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")
    # CommBranchWithNoVar
    TB();TB();LN("struct CommBranchWithNoVar : public ParserCommand {")
    TB();TB();TB();LN("ParserCommandBranch* br;")
    TB();TB();TB();LN("CommBranchWithNoVar(ParserCommandBranch* br) : br(br) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("SemanticNodePtr tmpPtr;")
    TB();TB();TB();TB();LN("for (auto& commPtr : *br) {")
    TB();TB();TB();TB();TB();LN("(*commPtr)(state, &tmpPtr);")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("virtual void print(size_t indent) {")
    TB();TB();TB();TB();LN("for (int i=0; i<indent; i++) std::cout << ' ';")
    TB();TB();TB();TB();LN("std::cout << \"CommBranchWithNoVar - \" << std::endl;")
    TB();TB();TB();TB();LN("for (auto& commPtr : *br) {")
    TB();TB();TB();TB();TB();LN("(*commPtr).print(indent+1);")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")
    # CommError
    TB();TB();LN("struct CommError : public ParserCommand {")
    TB();TB();TB();LN("std::wstring str; TokenInd tokInd;")
    TB();TB();TB();LN("CommError(std::wstring str, TokenInd tokInd) : str(str), tokInd(tokInd) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("(*varPtr)->errors.push_back(ParserError(state->tokens.at(std::min((size_t)tokInd, state->tokens.size()-1)), str));")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("virtual void print(size_t indent) {")
    TB();TB();TB();TB();LN("for (int i=0; i<indent; i++) std::cout << ' ';")
    TB();TB();TB();TB();LN("std::wcout << L\"CommError - \" << str << std::endl;")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")
    '''TB();TB();LN("struct CommPushNodeEmptyVar : public ParserCommand {")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("state->nodeVarStack.push_back(nullptr);")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")'''
    '''TB();TB();LN("struct CommPushNodeVar : public ParserCommand {")
    TB();TB();TB();LN("std::string name;")
    TB();TB();TB();LN("CommPushNodeVar(std::string name) : name(name) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("state->nodeStack.back()->nodeLists[name].push_back(nullptr);")
    TB();TB();TB();TB();LN("state->nodeVarStack.push_back(&(state->nodeStack.back()->nodeLists[name].back()));")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")'''
    '''TB();TB();LN("struct CommPushNodeList : public ParserCommand {")
    TB();TB();TB();LN("std::string name;")
    TB();TB();TB();LN("CommPushNodeList(std::string name) : name(name) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("state->nodeStack.back()->nodeLists[name].push_back(nullptr);")
    TB();TB();TB();TB();LN("state->nodeVarStack.push_back(&(state->nodeStack.back()->nodeLists[name].back()));")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")'''
    # CommSaveTokenVar
    TB();TB();LN("struct CommSaveTokenVar : public ParserCommand {")
    TB();TB();TB();LN("std::string name; TokenInd tokInd;")
    TB();TB();TB();LN("CommSaveTokenVar(std::string name, TokenInd tokInd) : name(name), tokInd(tokInd) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("(*varPtr)->tokenLists[name].push_back(state->tokens.at(tokInd));")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("virtual void print(size_t indent) {")
    TB();TB();TB();TB();LN("for (int i=0; i<indent; i++) std::cout << ' ';")
    TB();TB();TB();TB();LN("std::cout << \"CommSaveTokenVar - \" << name << std::endl;")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")
    # CommSaveTokenList
    TB();TB();LN("struct CommSaveTokenList : public ParserCommand {")
    TB();TB();TB();LN("std::string name; TokenInd tokInd;")
    TB();TB();TB();LN("CommSaveTokenList(std::string name, TokenInd tokInd) : name(name), tokInd(tokInd) {}")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("(*varPtr)->tokenLists[name].push_back(state->tokens.at(tokInd));")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("virtual void print(size_t indent) {")
    TB();TB();TB();TB();LN("for (int i=0; i<indent; i++) std::cout << ' ';")
    TB();TB();TB();TB();LN("std::cout << \"CommSaveTokenVar - \" << name << std::endl;")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")
    '''TB();TB();LN("struct CommPopBranch : public ParserCommand {")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("state->commStack.pop_back();")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")'''
    '''TB();TB();LN("struct CommPopNode : public ParserCommand {")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("if (state->nodeVarStack.back()) {")
    TB();TB();TB();TB();TB();LN("(*state->nodeVarStack.back()) = state->nodeStack.back();")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();TB();LN("else {")
    TB();TB();TB();TB();TB();LN("//delete state->nodeStack.back();// the ptr is shared ptr")
    TB();TB();TB();TB();LN("}")
    TB();TB();TB();TB();LN("state->nodeStack.pop_back();")
    TB();TB();TB();TB();LN("state->nodeVarStack.pop_back();")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")
    TB();TB();LN("struct CommPopNodeVar : public ParserCommand {")
    TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
    TB();TB();TB();TB();LN("state->nodeVarStack.pop_back();")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")'''
    for name, semNode in parser.semNodes.items():
        TB();TB();LN(f"struct CommPushNode_{semNodeName} : public ParserCommand {{")
        TB();TB();TB();LN("virtual void operator()(ParserState* state, SemanticNodePtr* varPtr) {")
        TB();TB();TB();TB();LN(f"(*varPtr) = std::make_shared<SemanticNode_{semNodeName}>();")
        TB();TB();TB();LN("}")
        TB();TB();TB();LN("virtual void print(size_t indent) {")
        TB();TB();TB();TB();LN("for (int i=0; i<indent; i++) std::cout << ' ';")
        TB();TB();TB();TB();LN(f"std::cout << \"CommPushNode_{semNodeName}\" << std::endl;")
        TB();TB();TB();LN("}")
        TB();TB();LN("};")


    '''TB();TB();LN("struct ParserIterator {")
    TB();TB();TB();LN("std::list<Token>::iterator tokIt;")
    TB();TB();TB();LN("std::vector<TokenAssignedData>::iterator dataIt;")
    TB();TB();TB();LN("inline void operator++() {")
    TB();TB();TB();TB();LN("++tokIt;")
    TB();TB();TB();TB();LN("++dataIt;")
    TB();TB();TB();LN("}")
    TB();TB();TB();LN("inline Token& operator*() {")
    TB();TB();TB();TB();LN("return *tokIt;")
    TB();TB();TB();LN("}")
    TB();TB();LN("};")'''
    
    # Declarations
    for part in parser.productionParts:
        if part.type == ProductionType.SubProd:
            TB();TB();LN("TokenInd check_" + part.idName + "(size_t tokenNum, std::vector<Token>& tokens, std::vector<TokenAssignedData>& data, TokenInd startInd);")
    TB();LN("")
    
    # Definitions
    for part in parser.productionParts:
        if part.type == ProductionType.SubProd:
            semNodeName = parser.productions[part.prodName].semNodeName

            TB();TB();LN(f"// {(part.hint)}")
            TB();TB();LN("TokenInd check_" + part.idName + "(size_t tokenNum, std::vector<Token>& tokens, std::vector<TokenAssignedData>& data, TokenInd startInd) { //"+part.hint)
            
            if part.isMainPart:
                TB();TB();TB();LN("// Check for cached results")
                TB();TB();TB();LN("if (data.at(startInd).checked_" + part.idName + ") {")
                TB();TB();TB();TB();LN(f"if (data.at(startInd).is_{part.idName}) return data.at(startInd).endInds[ProductionInd::{part.idName}];")
                TB();TB();TB();TB();LN("else return FAIL_IND;")
                TB();TB();TB();LN("}")
                TB();TB();TB();LN("data.at(startInd).checked_" + part.idName + " = true;")
                TB();TB();TB();LN("")
            TB();TB();TB();LN(f"ParserCommandBranch& commands = data.at(startInd).commands[ProductionInd::{part.idName}];")
            TB();TB();TB();LN("size_t ogCommandNumber = commands.size();")

            # Check all possibilities
            ctr = 0
            needsGotos = (len(part.possibilities) > 1)
            for poss in part.possibilities:
                ctr += 1
                assertiveMode = False

                # Possibility start 
                if needsGotos or True:# Always add gotos for readability
                    TB();TB();TB();LN("")
                    if len(poss) > 0:
                        TB();TB();TB();LN(f"// {poss[0].hint}")
                    else:
                        print("ERROR: ", ctr, part.hint)
                    TB();TB();TB();LN(f"tryPoss{ctr}:")

                # Possibility block
                TB();TB();TB();LN("{")
                TB();TB();TB();TB();LN("TokenInd ind = startInd;")
                TB();TB();TB();TB();LN("TokenInd testInd;")

                # reset command list and create node
                if part.isMainPart and semNodeName != FALTHRU_OUTPUT_PRODUCTION_STR and semNodeName != NO_OUTPUT_PRODUCTION_STR:
                    TB();TB();TB();TB();LN(f"commands.emplace_back(new CommPushNode_{semNodeName}());")


                for subpartIndex in range(0, len(poss)):
                    subpart = poss[subpartIndex]

                    # Process error helpers
                    for errhelper in subpart.errorHelpers:
                        if errhelper == ERROR_HELPER_STR_ASSERTIVE:
                            assertiveMode = True
                    
                    # Set failure snippet depending on the mode
                    
                    if assertiveMode:
                        # skip until synchronization part/token

                        # extract sync parts
                        syncParts : List[ProductionPart] = []
                        for syncpartIndex in range(subpartIndex+1, len(poss)):
                            possSyncParts : List[ProductionPart] = [poss[syncpartIndex]]
                            extractParts(poss[syncpartIndex], possSyncParts)

                            for possSyncPart in possSyncParts:
                                if ERROR_HELPER_STR_SYNC in possSyncPart.errorHelpers:
                                    syncParts.append(possSyncPart)

                        loopBody = ""
                        for syncPart in syncParts:
                            initializerCodeStr, checkerCodeStr, executorCodeStr = getIterationSnippets(parser, syncPart, part)
                            loopBody += f" {initializerCodeStr}; if ({checkerCodeStr}) break; "
                        
                        nextPossSnippet = f"{{std::wstringstream ss; ss << \"Unexpected \" << ((ind < tokenNum)? WTokenNames[(int)tokens.at(ind).type] : L\"end of file\") << \", expected a {subpart.symbol if len(subpart.symbol)>0 else subpart.idName}\"; commands.emplace_back(new CommError(ss.str(), ind));"
                        
                        if len(syncParts) > 0:
                            nextPossSnippet += f" for (ind++;ind < tokenNum; ind++) {{ {loopBody} }} }}"
                        else:
                            nextPossSnippet += f" return ind+1; }}"

                    else:
                        # Cancel the possibility and either check the next one, or return if the current is the last one
                        if ctr < len(part.possibilities):
                            nextPossSnippet = f"{{commands.resize(ogCommandNumber); goto tryPoss{ctr+1};}}"
                        else:
                            nextPossSnippet = "{commands.resize(ogCommandNumber); return FAIL_IND;}"

                    
                    
                    TB();TB();TB();TB();LN(f"")
                    
                    # Set code snippets depending on the type of the subpart

                    initializerCodeStr, checkerCodeStr, executorCodeStr = getIterationSnippets(parser, subpart, part)

                    # Output code depending on the repeat count of the subpart

                    TB();TB();TB();TB();LN(f"// {subpart.hint}")
                    # Optional ?
                    if subpart.repeatCount ==RepeatType.Optional:
                        TB();TB();TB();TB();LN(f"{initializerCodeStr};")
                        TB();TB();TB();TB();LN(f"if ({checkerCodeStr}) {{")
                        for ex in executorCodeStr:
                            TB();TB();TB();TB();TB();LN(f"{ex}")
                        TB();TB();TB();TB();LN(f"}}")
                    # Single
                    elif subpart.repeatCount ==RepeatType.Single:
                        TB();TB();TB();TB();LN(f"{initializerCodeStr};")
                        TB();TB();TB();TB();LN(f"if ({checkerCodeStr}) {{")
                        for ex in executorCodeStr:
                            TB();TB();TB();TB();TB();LN(f"{ex}")
                        TB();TB();TB();TB();LN(f"}}")
                        TB();TB();TB();TB();LN(f"else {nextPossSnippet};")
                    # SingleOrMore +
                    elif subpart.repeatCount ==RepeatType.SingleOrMore:
                        TB();TB();TB();TB();LN(f"{initializerCodeStr};")
                        TB();TB();TB();TB();LN(f"if ({checkerCodeStr}) {{")
                        for ex in executorCodeStr:
                            TB();TB();TB();TB();TB();LN(f"{ex}")
                        TB();TB();TB();TB();LN(f"}}")
                        TB();TB();TB();TB();LN(f"else {nextPossSnippet};")
                        TB();TB();TB();TB();LN(f"for ({initializerCodeStr}; {checkerCodeStr}; {initializerCodeStr}) {{")
                        for ex in executorCodeStr:
                            TB();TB();TB();TB();TB();LN(f"{ex}")
                        TB();TB();TB();TB();LN(f"}}")
                    # ZeroOrMore *
                    elif subpart.repeatCount ==RepeatType.ZeroOrMore:
                        TB();TB();TB();TB();LN(f"for ({initializerCodeStr}; {checkerCodeStr}; {initializerCodeStr}) {{")
                        for ex in executorCodeStr:
                            TB();TB();TB();TB();TB();LN(f"{ex}")
                        TB();TB();TB();TB();LN(f"}}")
                        
                TB();TB();TB();TB();LN("")
                if part.isMainPart:
                    TB();TB();TB();TB();LN("data.at(startInd).is_" + part.idName + " = true;")
                    TB();TB();TB();TB();LN("data.at(startInd).endInds[ProductionInd::" + part.idName + "] = ind;")

                '''if semNodeName != FALTHRU_OUTPUT_PRODUCTION_STR and semNodeName != NO_OUTPUT_PRODUCTION_STR:
                    TB();TB();TB();TB();LN(f"commands.emplace_back(new CommPopNode());")'''

                #TB();TB();TB();TB();LN(f"commands.emplace_back(new CommPopBranch());")
                TB();TB();TB();TB();LN("return ind;")
                TB();TB();TB();LN("}")

            TB();TB();LN("}")
    TB();LN("}")

    LN("")

    for name, semNode in parser.semNodes.items():
        TB();LN("SemanticNode_" + name + "::~SemanticNode_" + name + "() {}")
        TB();LN("std::string_view SemanticNode_" + name + "::name() const { return \"" + name + "\"; }")

    LN("")

    TB();LN("SemanticNodePtr parse(const std::list<Token> &input, std::list<ParserError>& outErrors)")
    TB();LN("{")
    TB();TB();LN("SemanticNodePtr res = nullptr;")
    TB();TB();LN("ParserState state;")
    TB();TB();LN("state.tokens = std::vector<Token>(input.begin(), input.end());")
    TB();TB();LN("state.data = std::vector<TokenAssignedData>(input.size());")
    TB();TB();LN("")
    TB();TB();LN("if (check_" + parser.startProduction + "(state.tokens.size(), state.tokens, state.data, 0) != FAIL_IND) {")
    #TB();TB();TB();LN("state.nodeVarStack.push_back(&res);")
    TB();TB();TB();LN("")
    TB();TB();TB();LN(f"for (auto& commPtr : state.data.at(0).commands[ProductionInd::{parser.startProduction}]) {{")
    TB();TB();TB();TB();LN("(*commPtr)(&state, &res);")
    #TB();TB();TB();TB();LN("(*commPtr).print(0);")
    TB();TB();TB();LN("}")
    TB();TB();LN("}")
    TB();TB();LN("")
    TB();TB();LN("extractErrors(res, outErrors);")
    TB();TB();LN("return res;")
    TB();LN("}")
    LN("")
    LN("}")

    f.close()