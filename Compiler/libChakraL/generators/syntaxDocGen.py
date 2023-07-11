from unicodeUtil import superscript_translate
from lexerGen import *
from parserGenShared import *
import time
import os

NOTE_SEPARATOR = " "
NOTE_OPEN = "("
NOTE_CLOSE = ")"
NOTE_OPTION_SEPARATOR = "( or )"
NOTE_REPEAT_OPTIONAL = "(optional)"
NOTE_REPEAT_ONEORMORE = "(1 or more)"
NOTE_REPEAT_ZEROORMORE = "(0 or more)"

def note(hint: str) -> str:
    return hint.translate(superscript_translate)

def maybeExpandProductionPart(part: ProductionPart, lexer: Lexer, parser: Parser, expand: list[str], skipsymbols: list[str] = []) -> str:
    expansion = ""
    suffix = ""

    print(part.symbol, skipsymbols, "//"+part.hint)

    if part.type == ProductionType.Token:
        if "keywords" in expand and part.symbol in lexer.keywordsPerTokenType.keys():
            expansion = lexer.keywordsPerTokenType[part.symbol]
        else:
            expansion = part.symbol
    elif part.type == ProductionType.Node:
        if "productions" in expand:
            if part.symbol in skipsymbols:
                expansion = part.idName
            else:
                expansion = maybeExpandProductionPart(
                    parser.productions[part.symbol].mainPart,
                    lexer, parser, expand,
                    skipsymbols + [part.symbol]
                )
        else:
            expansion = part.symbol
    elif part.type == ProductionType.SubProd:
        if ("options" in expand and len(part.possibilities) > 1) or \
            ("subproductions" in expand and len(part.possibilities) == 1):

            expansion = note(NOTE_OPTION_SEPARATOR).join([
                NOTE_SEPARATOR.join([
                    maybeExpandProductionPart(subpart, lexer, parser, expand, skipsymbols)
                    for subpart in poss
                ])
                for poss in part.possibilities
            ])

            if len(part.possibilities) > 1 or part.repeatCount != RepeatType.Single:
                expansion = NOTE_OPEN + NOTE_CLOSE
        else:
            expansion = part.idName

    if part.repeatCount == RepeatType.Single:
        suffix = ""
    elif part.repeatCount == RepeatType.Optional:
        suffix = NOTE_REPEAT_OPTIONAL
    elif part.repeatCount == RepeatType.SingleOrMore:
        suffix = NOTE_REPEAT_ONEORMORE
    elif part.repeatCount == RepeatType.ZeroOrMore:
        suffix = NOTE_REPEAT_ZEROORMORE

    return expansion + note(suffix)


def outputSyntaxDoc(filePrefix: str, lexer: Lexer, parser: Parser, expand: list[str]):
    '''
    Outputs files containing syntax specified in a human-friendly notation
    '''
    os.makedirs(os.path.dirname(f"{filePrefix}dummy.txt"), exist_ok=True)
    with open(f"{filePrefix}docslist.txt", "+w") as listfile:
        for name, production in parser.productions.items():
            filename = f"{filePrefix}{production.name}.txt"

            listfile.write(filename)

            with open(filename, "+w") as file:
                file.write(
                    maybeExpandProductionPart(production.mainPart,lexer, parser, expand)
                )