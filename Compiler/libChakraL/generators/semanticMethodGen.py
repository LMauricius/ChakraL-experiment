from __future__ import annotations
import os
from genUtil import *
from parserGenShared import *

def writeSemanticNodesMethodsCPP(parser: Parser, filename: str, headerfile: str, extraheaderfiles: list[str]):
    definitions: dict[str, str] = {}
    for name in parser.semNodeNames:
        #declarations[name] = "    SemanticNode_" + name + "::process("
        definitions[name] = ""

    print("Reading old parser nodes process definitions ", filename)
    try:
        with open(filename, "rt") as f:
            curDef = ""
            for line in f:
                if line.startswith("    void SemanticNode_"):
                    curDef = line[len("    void SemanticNode_"):line.find("::")]
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

        LN("// This file is autogenerated. Edit only function bodies!")
        LN("")
        for hf in extraheaderfiles+[headerfile]:
            LN(f'#include "{os.path.relpath(hf, start=os.path.dirname(filename))}"')
        
        #LN('#include <vector>')
        #LN('#include <string_view>')
        #LN('#include <regex>')
        LN("")
        LN("namespace ChakraL")
        LN("{")
        TB();LN("")
        for name, definition in definitions.items():
            LN("    void SemanticNode_" + name + "::process() {")
            f.write(definition)
            LN("    }")
            TB();LN("")
        LN("}")