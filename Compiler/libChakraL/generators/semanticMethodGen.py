from __future__ import annotations
import os
from typing import OrderedDict
from genUtil import *
from parserGenShared import *

class Member:

    def __init__(self, name:str, type:str, val:str = "") -> None:
        self.name = name
        self.type = type
        self.val = val

    @classmethod
    def fromDefinition(self, line:str, location:int) -> Member:
        typeMarkInd = line.find("->")
        if typeMarkInd == -1:
            raise FormatError("'->' type mark not found but required", location)

        name = line[0:typeMarkInd].strip()
        
        defaultValMarkInd = line.find("=", typeMarkInd+2)
        if defaultValMarkInd == -1:
            type = line[typeMarkInd+2:].strip()
            val = ""
        else:
            type = line[typeMarkInd+2:defaultValMarkInd].strip()
            val = line[defaultValMarkInd+1:].strip()
        
        return Member(name, type, val)

NAME_METHOD_DECL = "className() const"
PRINT_METHOD_DECL = "print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const"
SUBNODES_METHOD_DECL = "getSubNodes() const"

class SemanticNode:
    def __init__(self) -> None:
        self.parentNode : str = "SemanticNode"
        self.parentClassName : str = "SemanticNode"
        self.privateMembers : OrderedDict[str, Member] = OrderedDict()
        self.protectedMembers : OrderedDict[str, Member] = OrderedDict()
        self.publicMembers : OrderedDict[str, Member] = OrderedDict()
        self.methods : OrderedDict[str, Member] = OrderedDict()
        self.cachingMethodIDs : OrderedDict[str, str] = OrderedDict()

        mem = Member(NAME_METHOD_DECL, "std::string_view")
        self.publicMembers[mem.name] = mem
        self.methods[mem.name] = mem
        mem = Member(PRINT_METHOD_DECL, "void")
        self.publicMembers[mem.name] = mem
        self.methods[mem.name] = mem
        mem = Member(SUBNODES_METHOD_DECL, "std::vector<const SemanticNode*>")
        self.publicMembers[mem.name] = mem
        self.methods[mem.name] = mem

def loadSemanticNodes(filename: str):
    print("Loading semantic nodes ", filename)

    lines = meaningfulLines(filename)
    semNodes : OrderedDict[str, SemanticNode] = OrderedDict()
    curNodeName = ""
    curNode = None

    try:
        l, location = next(lines, ("", Location()))


        while len(l):
            if l[0] == "@":
                curNodeName = l[1:]
                curNode = semNodes.setdefault(curNodeName, SemanticNode())
            else:
                spaceInd = l.find(" ")
                mark = l[0:spaceInd].strip()
                memberDef = l[spaceInd:].strip()
                
                if mark == "parent":
                    curNode.parentNode = memberDef
                    curNode.parentClassName = "SemanticNode_" + memberDef
                elif (mark[0] == "f" or mark[0] == "v" or mark[0] == "c") and (mark[1:] == "pub" or mark[1:] == "prot" or mark[1:] == "priv"):

                    # select the member list depending on access modifier
                    selMemberList: OrderedDict[str, Member] | None = None
                    if mark[1:] == "pub":
                        selMemberList = curNode.publicMembers
                    elif mark[1:] == "prot":
                        selMemberList = curNode.protectedMembers
                    elif mark[1:] == "priv":
                        selMemberList = curNode.privateMembers

                    # add member depending on kind
                    if mark[0] == "f":
                        newM = Member.fromDefinition(memberDef, location)
                        selMemberList.setdefault(newM.name, newM)
                        curNode.methods.setdefault(newM.name, newM)
                    elif mark[0] == "v":
                        newM = Member.fromDefinition(memberDef, location)
                        selMemberList.setdefault(newM.name, newM)
                    elif mark[0] == "c":
                        newM = Member.fromDefinition(memberDef, location)
                        newFuncMem = Member(newM.name, newM.type, "")
                        cachingID = newM.name[0:newM.name.find("(")].strip()
                        print("CACHE: "+cachingID)
                        newCacheMem = Member("mCached_"+cachingID, f"std::optional<{newM.type}>", f"std::optional<{newM.type}>{{{newM.val}}}")
                        newGetterMem = Member("get_"+newM.name, newM.type, "")

                        selMemberList.setdefault(newFuncMem.name, newFuncMem)
                        curNode.methods.setdefault(newFuncMem.name, newFuncMem)
                        curNode.cachingMethodIDs.setdefault(newFuncMem.name, cachingID)

                        curNode.privateMembers.setdefault(newCacheMem.name, newCacheMem)
                        curNode.privateMembers.setdefault(newGetterMem.name, newGetterMem)
                        curNode.methods.setdefault(newGetterMem.name, newGetterMem)
                else:
                    raise FormatError(f"Unknown node mark '{mark}'", location)

            l, location = next(lines, ("", Location()))

    except FormatError as e:
        print("ERROR " + str(e.location) + ": " + e.message)
        sys.exit(1)
    except StopIteration:
        pass
        
    return semNodes

def writeSemanticNodesMethodsH(semNodes: OrderedDict[str, SemanticNode], filename: str, lexerHeaderfile: str, extraheaderfiles: list[str]):

    print("Writing new parser nodes process definitions ", filename)
    with open(filename, "wt") as f:

        def TB():
            f.write('    ')
        def LN(s: str):
            f.write(s)
            f.write('\n')

        LN("// This file is autogenerated. Do not edit!")
        LN("")
        for hf in extraheaderfiles+[lexerHeaderfile]:
            LN(f'#include "{os.path.relpath(hf, start=os.path.dirname(filename))}"')
        
        #LN('#include <vector>')
        #LN('#include <string_view>')
        #LN('#include <regex>')
        LN("")
        LN("namespace ChakraL")
        LN("{")
        TB();LN("")
        
        for name, semNode in semNodes.items():
            TB();LN(f"class SemanticNode_{name};")
        TB();LN("")

        for name, semNode in semNodes.items():
            TB();LN(f"class SemanticNode_{name} : public {semNode.parentClassName}")
            TB();LN(f"{{")
            TB();LN(f"public:")
            TB();TB();LN(f"SemanticNode_{name}() = default;")
            TB();TB();LN(f"~SemanticNode_{name}() = default;")

            for visMark, members in [
                ("public", semNode.publicMembers.values()),
                ("protected", semNode.protectedMembers.values()),
                ("private", semNode.privateMembers.values())
            ]:
                if len(members) > 0:
                    TB();LN(f"{visMark}:")
                    for mem in members:
                        if len(mem.val) > 0:
                            TB();TB();LN(f"{mem.type} {mem.name} = {mem.val};")
                        else:
                            TB();TB();LN(f"{mem.type} {mem.name};")

            TB();LN(f"}};")
            TB();LN("")
        LN("}")

def extractTypeArgList(params: str)->List[Tuple[str, str]]:
    argList = [("", "")]

    parCount = 0
    subInd = 0
    for c in params:
        if c == "(" or c == "[" or c == "{" or c == "<":
            parCount += 1
        elif c == ")" or c == "]" or c == "}" or c == ">":
            parCount -= 1

        if c == "," and parCount == 0:
            argList += [("", "")]
            subInd = 0
        elif c == " " and parCount == 0 and argList[-1][subInd] != "":
            subInd += 1
        else:
            if subInd == 0:
                argList[-1] = (argList[-1][0] + c, argList[-1][1])
            elif subInd == 1:
                argList[-1] = (argList[-1][0], argList[-1][1] + c)

    return argList
        

def writeSemanticNodesMethodsCPP(semNodes: OrderedDict[str, SemanticNode], filename: str, headerfile: str, extraheaderfiles: list[str]):
    definitions: dict[str, str] = {}
    definitionsPerClass: dict[str, dict[str, str]] = {}

    print("Reading old parser nodes process definitions ", filename)
    try:
        with open(filename, "rt") as f:
            curDefName = ""
            curDef = ""
            for line in f:
                if "SemanticNode_" in line:
                    curDefName = line[0:line.find("{")].strip()
                    curDef = ""
                elif line.startswith("    }"):
                    if len(curDef) > 0 and not (curDefName.endswith(NAME_METHOD_DECL) or curDefName.endswith(PRINT_METHOD_DECL) or curDefName.endswith(SUBNODES_METHOD_DECL)):
                        definitions[curDefName] = curDef
                    curDefName = ""
                elif len(curDefName) > 0:
                    curDef += line
    except FileNotFoundError:
        print("No old parser nodes process definitions found")
 
    TAB = "    "

    for className, semNode in semNodes.items():

        # Existing methods
        definitionsPerClass[className] = {}
        for methName, meth in semNode.methods.items():
            curDefName = f"{meth.type} SemanticNode_{className}::{methName}"

            if curDefName in definitions.keys():
                definitionsPerClass[className][curDefName] = definitions[curDefName]
                definitions.pop(curDefName)
            else:
                definitionsPerClass[className][curDefName] = ""

        # Caching methods
        for methName, cacheID in semNode.cachingMethodIDs.items():
            funcMem = semNode.methods[methName]
            cacheMem = semNode.privateMembers["mCached_"+cacheID]
            getterMem = semNode.privateMembers["get_"+funcMem.name]
            params = methName[methName.find("(")+1:methName.rfind(")")]
            args = ", ".join([argname for t, argname in extractTypeArgList(params)])
            print("ARGUMENTS: "+str(extractTypeArgList(params)))

            meth = funcMem
            code = ""
            code += f"{TAB}{TAB}" + fr'if (!mCached_{cacheID}.has_value()) {{' + "\n"
            code += f"{TAB}{TAB}{TAB}" + fr'mCached_{cacheID} = std::optional<{funcMem.type}>{{get_{cacheID}({args})}};' + "\n"
            code += f"{TAB}{TAB}" + fr'}}' + "\n"
            code += f"{TAB}{TAB}" + fr'return mCached_{cacheID}.value();' + "\n"

            definitionsPerClass[className][f"{meth.type} SemanticNode_{className}::{meth.name}"] = code
        
        # NAME method
        meth = semNode.methods[NAME_METHOD_DECL]
        definitionsPerClass[className][f"{meth.type} SemanticNode_{className}::{meth.name}"] = f"{TAB}{TAB}return \"{className}\";\n"
        
        # PRINT method
        meth = semNode.methods[PRINT_METHOD_DECL]
        code = ""
        code += f"{TAB}{TAB}" + fr'out << "{{" << std::endl; ' + "\n"
        code += f"{TAB}{TAB}" + fr'for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "NODE_TYPE: \"{className}\"," << std::endl; ' + "\n"
        code += f"{TAB}{TAB}\n"
        for memName, mem in semNode.publicMembers.items():
            if mem.type.startswith("Ptr<SemanticNode_"):
                code += f"{TAB}{TAB}" + fr'for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "{mem.name}: "; ' + "\n"
                code += f"{TAB}{TAB}" + fr'if ({mem.name}) {mem.name}->print(out, tabs+1, tabstr); else out << "null";' + "\n"
                code += f"{TAB}{TAB}" + fr'out << "," << std::endl; ' + "\n"
                code += f"{TAB}{TAB}\n"
            elif mem.type.startswith("std::list<Ptr<SemanticNode_"):
                code += f"{TAB}{TAB}" + fr'{{for (size_t i = 0; i<tabs+1; i++) out << tabstr;}} out << "{mem.name}: [" << std::endl;' + "\n"
                code += f"{TAB}{TAB}" + fr'for (auto& ptr : {mem.name}) {{for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }}' + "\n"
                code += f"{TAB}{TAB}" + fr'{{for (size_t i = 0; i<tabs+1; i++) out << tabstr;}} out << "]," << std::endl;' + "\n"
                code += f"{TAB}{TAB}\n"
            elif mem.type.startswith("Token"):
                code += f"{TAB}{TAB}" + fr'for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "{mem.name}: "; ' + "\n"
                code += f"{TAB}{TAB}" + fr'out<< "\"" << {mem.name}.fullname() << "\"";' + "\n"
                code += f"{TAB}{TAB}" + fr'out << "," << std::endl; ' + "\n"
                code += f"{TAB}{TAB}\n"
            elif mem.type.startswith("std::list<Token"):
                code += f"{TAB}{TAB}" + fr'{{for (size_t i = 0; i<tabs+1; i++) out << tabstr;}} out << "{mem.name}: [" << std::endl;' + "\n"
                code += f"{TAB}{TAB}" + fr'for (auto& tok : {mem.name}) {{for (size_t i = 0; i<tabs+2; i++) out << tabstr; out << "\"" << tok.fullname() << "\"," << std::endl; }}' + "\n"
                code += f"{TAB}{TAB}" + fr'{{for (size_t i = 0; i<tabs+1; i++) out << tabstr;}} out << "]," << std::endl;' + "\n"
                code += f"{TAB}{TAB}\n"
            
        code += f"{TAB}{TAB}" + fr'for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}}"; ' + "\n"
        definitionsPerClass[className][f"{meth.type} SemanticNode_{className}::{meth.name}"] = code
        
        # SUBNODES method
        meth = semNode.methods[SUBNODES_METHOD_DECL]
        code = ""
        code += f"{TAB}{TAB}" + fr'std::vector<const SemanticNode*> ret {{' + "\n"
        for memName, mem in semNode.publicMembers.items():
            if mem.type.startswith("Ptr<SemanticNode_"):
                code += f"{TAB}{TAB}{TAB}" + fr'{mem.name}.get(),' + "\n"
        code += f"{TAB}{TAB}" + fr'}};' + "\n"

        code += f"{TAB}{TAB}" + fr'ret.reserve(ret.size() + '
        for memName, mem in semNode.publicMembers.items():
            if mem.type.startswith("std::list<Ptr<SemanticNode_"):
                code += fr'{mem.name}.size() + '
        code += fr'0);' + "\n"

        for memName, mem in semNode.publicMembers.items():
            if mem.type.startswith("std::list<Ptr<SemanticNode_"):
                code += f"{TAB}{TAB}" + fr'for (const auto& ptr : {mem.name}) {{ret.push_back(ptr.get());}}' + "\n"

        code += f"{TAB}{TAB}" + fr'return ret;' + "\n"
        definitionsPerClass[className][f"{meth.type} SemanticNode_{className}::{meth.name}"] = code

        # END of methods
        


    print("Writing new parser nodes process definitions ", filename)
    with open(filename, "wt") as f:

        def TB():
            f.write('    ')
        def LN(s: str):
            f.write(s)
            f.write('\n')

        LN("// This file is autogenerated. Edit only function bodies!")
        LN("")
        for hf in extraheaderfiles+[headerfile]:
            LN(f'#include "{os.path.relpath(hf, start=os.path.dirname(filename))}"')
        LN(f'#include <ostream>')
        
        #LN('#include <vector>')
        #LN('#include <string_view>')
        #LN('#include <regex>')
        LN("")
        LN("namespace ChakraL")
        LN("{")
        TB();LN("")
        for className, classDefinitions in definitionsPerClass.items():
            TB();LN("// === *** " + className + " *** ===")
            TB();LN("")
            for name, definition in classDefinitions.items():
                TB();LN(name + " {")
                f.write(definition)
                TB();LN("}")
                TB();LN("")
        for name, definition in definitions.items():
            TB();LN(name + " {")
            f.write(definition)
            TB();LN("}")
            TB();LN("")
        LN("}")

def semNodeExtends(child:str, parent:str, semNodes: OrderedDict[str, SemanticNode]) -> bool:
    cur = child
    while cur in semNodes:
        if cur == parent:
            return True
        cur = semNodes[cur].parentNode
    return False