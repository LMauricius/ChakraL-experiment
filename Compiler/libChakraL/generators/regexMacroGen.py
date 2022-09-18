import sys
import unicodedata as ucd
from genUtil import *

class RegexRange:
    def __init__(self) -> None:
        self.ranges: list[range] = []

    def add(self, index: int):
        if len(self.ranges) > 0 and self.ranges[-1].stop == index-1:
            self.ranges[-1] = range(self.ranges[-1].start, index)
        else:
            self.ranges.append(range(index, index))

    def regexstring(self) -> str:
        s = ""
        for r in self.ranges:
            if r.start == r.stop:
                s += chr(r.start)
            else:
                s += f"{chr(r.start)}-{chr(r.stop)}"
        return s

def outputUnicodeMacros(filename: str):
    #with open(filename, 'w') as file:
    #    file.write()

    catRanges: dict[str, RegexRange] = {}
    
    for i in range(sys.maxunicode):
        c = chr(i)
        #n = ucd.name(c, "<Err>")
        cat = ucd.category(c)

        if not cat in catRanges.keys():
            catRanges[cat] = RegexRange()
        if not cat[0] in catRanges.keys():
            catRanges[cat[0]] = RegexRange()

        catRanges[cat].add(i)
        catRanges[cat[0]].add(i)

    # named cats
    catNames = {
        "Lu" : 	"Uppercase_Letter",
        "Ll" : 	"Lowercase_Letter",
        "Lt" : 	"Titlecase_Letter",
        "LC" : 	"Cased_Letter",
        "Lm" : 	"Modifier_Letter",
        "Lo" : 	"Other_Letter",
        "L"  : 	"Letter",
        "Mn" : 	"Nonspacing_Mark",
        "Mc" : 	"Spacing_Mark",
        "Me" : 	"Enclosing_Mark",
        "M"  : 	"Mark",
        "Nd" : 	"Decimal_Number",
        "Nl" : 	"Letter_Number",
        "No" : 	"Other_Number",
        "N"  : 	"Number",
        "Pc" : 	"Connector_Punctuation",
        "Pd" : 	"Dash_Punctuation",
        "Ps" : 	"Open_Punctuation",
        "Pe" : 	"Close_Punctuation",
        "Pi" : 	"Initial_Punctuation",
        "Pf" : 	"Final_Punctuation",
        "Po" : 	"Other_Punctuation",
        "P"  : 	"Punctuation",
        "Sm" : 	"Math_Symbol",
        "Sc" : 	"Currency_Symbol",
        "Sk" : 	"Modifier_Symbol",
        "So" : 	"Other_Symbol",
        "S"  : 	"Symbol",
        "Zs" : 	"Space_Separator",
        "Zl" : 	"Line_Separator",
        "Zp" : 	"Paragraph_Separator",
        "Z"  : 	"Separator",
        "Cc" : 	"Control",
        "Cf" : 	"Format",
        "Cs" : 	"Surrogate",
        "Co" : 	"Private_Use",
        "Cn" : 	"Unassigned",
        "C"  : 	"Other"
    }
    catOrder = [
        "Letter",
        "Uppercase_Letter",
        "Lowercase_Letter",
        "Titlecase_Letter",
        "Cased_Letter",
        "Modifier_Letter",
        "Other_Letter",
        "Mark",
        "Nonspacing_Mark",
        "Spacing_Mark",
        "Enclosing_Mark",
        "Number",
        "Decimal_Number",
        "Letter_Number",
        "Other_Number",
        "Punctuation",
        "Connector_Punctuation",
        "Dash_Punctuation",
        "Open_Punctuation",
        "Close_Punctuation",
        "Initial_Punctuation",
        "Final_Punctuation",
        "Other_Punctuation",
        "Symbol",
        "Math_Symbol",
        "Currency_Symbol",
        "Modifier_Symbol",
        "Other_Symbol",
        "Separator",
        "Space_Separator",
        "Line_Separator",
        "Paragraph_Separator",
        "Other",
        "Control",
        "Format",
        "Surrogate",
        "Private_Use",
        "Unassigned",
        "L", 
        "Lu",
        "Ll",
        "Lt",
        "LC",
        "Lm",
        "Lo",
        "M", 
        "Mn",
        "Mc",
        "Me",
        "N", 
        "Nd",
        "Nl",
        "No",
        "P", 
        "Pc",
        "Pd",
        "Ps",
        "Pe",
        "Pi",
        "Pf",
        "Po",
        "S", 
        "Sm",
        "Sc",
        "Sk",
        "So",
        "Z", 
        "Zs",
        "Zl",
        "Zp",
        "C", 
        "Cc",
        "Cf",
        "Cs",
        "Co",
        "Cn"
    ]

    catRangesExt: dict[str, RegexRange] = {}
    for cat, r in catRanges.items():
        catRangesExt[cat] = r
        catRangesExt[catNames[cat]] = r

    with open(filename, 'w') as file:
        for cat in catOrder:
            r = catRangesExt[cat] if cat in catRangesExt.keys() else RegexRange()
            file.write(f"[:{cat}:]"+"\n")
            file.write(escapeStringNonGraph(r.regexstring())+"\n")