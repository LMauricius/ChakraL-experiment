from __future__ import annotations
import os
import sys
from typing import Iterator

def meaningfulLines(filename: str) -> Iterator[str]:
    with open(filename, "rt") as f:
        lineInd = 0
        for line in f:
            lineInd += 1
            l = line.lstrip()
            if len(l) > 0:
                if l[0] != '#':
                    if l[0:2] == '>>':
                        includeFilename = l[2:].strip()
                        nameNoPath = os.path.splitext(includeFilename)[0]
                        for l2, lineInd2 in meaningfulLines(os.path.dirname(filename)+'/'+includeFilename):
                            yield l2, (lineInd, nameNoPath+":"+str(lineInd2))
                    else:
                        yield l.rstrip('\n'), lineInd

class FormatError(Exception):
    def __init__(self, message, lineInd: int):
        self.message = message
        self.lineInd = lineInd

def safeStrConvert(s: str):
    return s.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)


def escapeRegexToC(regex: str) -> str:
    ret = ""
    for c in regex:
        if c == '\"':
            ret += "\\\""
        elif c == '\'':
            ret += "\\\'"
        elif c == '\\':
            ret += "\\\\"
        elif c == '\n':
            ret += "\\n"
        else:
            ret += c
    return ret

def escapeRegexToCComment(regex: str) -> str:
    ret = ""
    for c in regex:
        if c == '\n':
            ret += "\\n"
        else:
            ret += c
    return ret

def unescapeString(s: str):
    return s.encode("raw_unicode_escape").decode("unicode_escape")
    return bytes(s, "utf-8").decode("unicode_escape")