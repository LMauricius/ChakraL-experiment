from __future__ import annotations
from hashlib import sha3_224
import os
import sys
from typing import Iterator
import unicodedata as ucd
import copy

class Location:
    def __init__(self, path: str | None = None, lineInd: int | None = None):
        self.path = path
        self.lineInd = lineInd

    def __str__(self) -> str:
        s = "in "
        if self.path is not None:
            s += f"\"{self.path}\""
        if self.lineInd is not None:
            s += f", line {self.lineInd}"
        return s

def meaningfulLines(filename: str) -> Iterator[(str, Location)]:
    with open(filename, "rt") as f:
        location = Location(filename, 0)
        for line in f:
            location.lineInd += 1
            l = line.lstrip()
            if len(l) > 0:
                if l[0] != '#':
                    if l[0:2] == '>>':
                        includeFilename = l[2:].strip()
                        nameNoPath = os.path.splitext(includeFilename)[0]
                        for l2, location2 in meaningfulLines(os.path.dirname(filename)+'/'+includeFilename):
                            yield l2, location2
                    else:
                        yield l.rstrip('\n'), location

class FormatError(Exception):
    def __init__(self, message, location: Location):
        self.message = message
        self.location = copy.copy(location)

class SemanticError(Exception):
    def __init__(self, message, location: Location):
        self.message = message
        self.location = copy.copy(location)

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

def escapeStringNonGraph(s: str):
    ret = ""
    for c in s:
        if ucd.category(c)[0] == 'Z' or ucd.category(c)[0] == 'C':
            ret += c.encode("unicode_escape").decode("ascii")
        else:
            ret += c
    return ret